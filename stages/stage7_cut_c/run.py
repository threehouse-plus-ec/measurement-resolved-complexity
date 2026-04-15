"""Stage 7 -- Cut C (N=3, commensurability comparison).

Per VOYAGE_PLAN v0.2 §4 Cut C, with a scope reduction documented in
stage notes §Scope: n_max=10 default (adequate per §2.5 table at
|Delta|=0.15; Poisson tail argument for N=3), R=30 per point, two
sweep points (D in {+0.15, +0.30}) rather than the full four.
Reason: runtime budget. At n_max=12, a single N=3 trajectory runs in
~100s; the full v0.2 spec (1200 trajectories at n_max=12) would take
~30+ hours. The reduced-scope run (3 configs x 2 D x 30 R = 180
trajectories at n_max=10, ~22s each) takes ~65 min.

This is a scope reduction, not a physics compromise: the point of Cut C
is the commensurability comparison (golden-incommensurate vs
root-2-incommensurate vs rational 3:5:7), and two sweep points per
config are enough to compare configs.

Commensurability encoding (per v0.2 §4):
- C-Ra (golden): omega ratios (1 : phi : phi^2).
- C-Rb (irrational alt): (1 : sqrt(2) : sqrt(3)).
- C-Rc (rational 3:5:7): (1 : 5/3 : 7/3).

Sweep parameter D = Delta_1; (Delta_2, Delta_3) follow from
ratio * D per config. That keeps all per-mode detunings within Cut A
range (smallest |Delta| is |D| at mode 1).

Analyses per Guardian Stage 7 pin (1) -- Complementarity tests:
- Per-moment offset tau: time lag between nearest peaks of C(t) and
  sigma^2(t). Complementarity predicts this is a smooth function of
  D, not noise.
- Complementarity product C(t) * sigma^2(t): compute the time-average
  and the peak-to-peak ratio. Speculative uncertainty-relation test.
- Per-mode Pearson r(sigma^2, |dC^(k)/dt|) where C^(k) = log n_eff^(k);
  complementarity-per-mode predicts per-mode correlations carry the
  signal even when aggregate C is washed out.

Gates / convergence:
- Noiseless single-trajectory convergence at n_max=12 vs n_max=10 for
  each (config, D) point: max |p_10(t) - p_12(t)|. Target <= 1e-4
  absolute on p(t). Cheaper than full ensemble convergence and
  adequate for Cut C's exploratory purpose.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SRC = REPO / "src"
FIGURES = REPO / "figures"
sys.path.insert(0, str(SRC))

from ensemble import (
    ensemble_mean,
    ensemble_variance,
    qpn_floor,
    resolved_fraction,
    resolved_per_cycle,
    run_ensemble_three_mode,
    sample_detunings,
    t_det,
    t_rise,
)
from hamiltonian import initial_state_up_vacuum_n3, three_mode_hamiltonian
from observables import (
    aggregate_complexity_series,
    ipr_per_mode_at_time_n3,
    n_eff_from_eigenvalues,
    n_eff_per_mode_series_n3,
    reduced_mode_matrices_n3,
    spin_up_population_n3,
)
from propagate import propagate_eigendecomp


PARENT_SEED = 2026_04_17
PHI = (1.0 + np.sqrt(5.0)) / 2.0

CONFIGS = [
    ("C-Ra", "golden (1:phi:phi^2)", 1.0, PHI, PHI * PHI),
    ("C-Rb", "sqrt (1:sqrt2:sqrt3)", 1.0, np.sqrt(2.0), np.sqrt(3.0)),
    ("C-Rc", "rational (1:5/3:7/3)", 1.0, 5.0 / 3.0, 7.0 / 3.0),
]

SWEEP_D = [0.15, 0.30]

N_MAX_DEFAULT = 10
N_MAX_CONVERGENCE = 12
R = 30
T_MAX = 50.0
N_TIMES = 500
G = 0.1
SIGMA_DELTA = 0.01
M_VALUES = [100, 1000, 10_000]


def peak_offset_tau(series_a, series_b, times, prominence_a, prominence_b):
    """Nearest-peak lag from each A-peak to the nearest B-peak."""
    pa, _ = find_peaks(series_a, prominence=prominence_a)
    pb, _ = find_peaks(series_b, prominence=prominence_b)
    if len(pa) == 0 or len(pb) == 0:
        return np.array([]), len(pa), len(pb)
    tA = times[pa]
    tB = times[pb]
    lags = np.array([tB[np.argmin(np.abs(tB - t))] - t for t in tA])
    return lags, len(pa), len(pb)


def analyse_point(label, config_name, D, ratio2, ratio3, seed_seq, times,
                  sigma_Delta, g, n_max, R, M_values):
    D1 = D
    D2 = ratio2 * D
    D3 = ratio3 * D

    # Per-mode detuning ensembles (independent noise per mode).
    parent = np.random.SeedSequence(seed_seq.generate_state(1)[0])
    ss_m1, ss_m2, ss_m3 = parent.spawn(3)
    d1 = sample_detunings(D1, sigma_Delta, R, rng=np.random.default_rng(ss_m1))
    d2 = sample_detunings(D2, sigma_Delta, R, rng=np.random.default_rng(ss_m2))
    d3 = sample_detunings(D3, sigma_Delta, R, rng=np.random.default_rng(ss_m3))

    t0 = time.time()
    ens = run_ensemble_three_mode(d1, d2, d3, g=g, n_max=n_max, times=times)
    ens_time = time.time() - t0

    p_mean = ensemble_mean(ens["p"])
    p_var = ensemble_variance(ens["p"])
    neff_mean = ensemble_mean(ens["n_eff_per_mode"])  # (n_times, 3)
    C_mean = ensemble_mean(ens["C"])
    dCdt = np.gradient(C_mean, times)
    abs_dCdt = np.abs(dCdt)

    mask = p_var > 1e-8
    if np.any(mask):
        t_m = times[mask]
        sigma2_m = p_var[mask]
        C_m = C_mean[mask]
        abs_dCdt_m = abs_dCdt[mask]
        C_bar = float(np.trapezoid(C_m, t_m) / (t_m[-1] - t_m[0]))
        pearson_growth = float(np.corrcoef(sigma2_m, abs_dCdt_m)[0, 1])
        pearson_series = float(np.corrcoef(sigma2_m, C_m)[0, 1])
    else:
        C_bar = pearson_growth = pearson_series = float("nan")

    # Timing per M
    period_slow = 2.0 * np.pi / min(abs(D1), abs(D2), abs(D3))
    timing = {}
    for M in M_values:
        qpn_M = qpn_floor(p_mean, M)
        timing[M] = {
            "t_rise": t_rise(p_var, qpn_M, times),
            "T_det": t_det(p_var, qpn_M, times),
            "f_resolved": resolved_fraction(p_var, qpn_M),
            "f_per_cycle_slow": resolved_per_cycle(p_var, qpn_M, times,
                                                    period_slow),
        }

    # Complementarity: peak-offset between C(t) peaks and sigma^2 peaks
    prom_sigma2 = 0.05 * (sigma2_m.max() - sigma2_m.min()) if np.any(mask) else 1e-12
    prom_C = 0.05 * (C_m.max() - C_m.min()) if np.any(mask) else 1e-12
    lags, n_sigma2_peaks, n_C_peaks = peak_offset_tau(
        sigma2_m if np.any(mask) else p_var,
        C_m if np.any(mask) else C_mean,
        t_m if np.any(mask) else times,
        max(prom_sigma2, 1e-12), max(prom_C, 1e-12),
    )

    # Complementarity product test (speculative)
    cxs_product = sigma2_m * C_m if np.any(mask) else np.array([])
    product_mean = float(np.mean(cxs_product)) if len(cxs_product) else float("nan")
    product_peak = float(np.max(cxs_product)) if len(cxs_product) else float("nan")
    product_min = float(np.min(cxs_product)) if len(cxs_product) else float("nan")

    # Per-mode complementarity: r(sigma^2, |dC^(k)/dt|) for each k
    pearson_per_mode = []
    for k in range(3):
        C_k = np.log(np.maximum(neff_mean[:, k], 1e-30))
        dC_k = np.abs(np.gradient(C_k, times))
        if np.any(mask):
            r_k = float(np.corrcoef(p_var[mask], dC_k[mask])[0, 1])
        else:
            r_k = float("nan")
        pearson_per_mode.append(r_k)

    # Convergence spot-check: noiseless trajectory at n_max=N_MAX_DEFAULT
    # and n_max=N_MAX_CONVERGENCE; compare p(t).
    t0 = time.time()
    H10 = three_mode_hamiltonian(D1, D2, D3, g, n_max)  # default
    psi10 = initial_state_up_vacuum_n3(n_max)
    s10 = propagate_eigendecomp(H10, psi10, times)
    p10 = spin_up_population_n3(s10, n_max)
    conv_time_10 = time.time() - t0

    t0 = time.time()
    H12 = three_mode_hamiltonian(D1, D2, D3, g, N_MAX_CONVERGENCE)
    psi12 = initial_state_up_vacuum_n3(N_MAX_CONVERGENCE)
    s12 = propagate_eigendecomp(H12, psi12, times)
    p12 = spin_up_population_n3(s12, N_MAX_CONVERGENCE)
    conv_time_12 = time.time() - t0

    conv_err = float(np.max(np.abs(p10 - p12)))
    conv_pass = conv_err <= 1e-4

    # IPR diagnostic at peak-C on noiseless trajectory
    C_nom = aggregate_complexity_series(n_eff_per_mode_series_n3(s10, n_max))
    i_peak = int(np.argmax(C_nom))
    psi_peak = s10[i_peak]
    rho_m1, rho_m2, rho_m3 = reduced_mode_matrices_n3(psi_peak, n_max)
    iprs = ipr_per_mode_at_time_n3(psi_peak, n_max)
    neffs_at_peak = tuple(n_eff_from_eigenvalues(np.linalg.eigvalsh(r))
                          for r in (rho_m1, rho_m2, rho_m3))

    return {
        "D": D, "Delta_triplet": (D1, D2, D3),
        "p_mean": p_mean, "sigma2": p_var,
        "n_eff_per_mode_mean": neff_mean, "C_mean": C_mean,
        "abs_dCdt": abs_dCdt, "C_bar": C_bar,
        "pearson_growth": pearson_growth, "pearson_series": pearson_series,
        "pearson_per_mode": pearson_per_mode,
        "timing": timing,
        "peak_offsets": {
            "n_sigma2_peaks": n_sigma2_peaks, "n_C_peaks": n_C_peaks,
            "lags": lags.tolist() if len(lags) else [],
            "mean_abs_lag": float(np.mean(np.abs(lags))) if len(lags) else float("nan"),
        },
        "complementarity_product": {
            "mean": product_mean, "peak": product_peak, "min": product_min,
        },
        "convergence": {
            "n_max_default": n_max, "n_max_check": N_MAX_CONVERGENCE,
            "err": conv_err, "pass": conv_pass,
        },
        "ipr_at_peak": {
            "t_peak": float(times[i_peak]),
            "n_eff": list(neffs_at_peak),
            "ipr": list(iprs),
            "ipr_times_neff": [float(i * n) for i, n in zip(iprs, neffs_at_peak)],
        },
        "timing_budget": {
            "ensemble_s": ens_time,
            "conv_n10_s": conv_time_10, "conv_n12_s": conv_time_12,
        },
    }


def main():
    times = np.linspace(0.0, T_MAX, N_TIMES)

    parent_ss = np.random.SeedSequence(PARENT_SEED)
    # Spawn one child per (config, D) pair (6 total for 3 configs x 2 D).
    child_ss = parent_ss.spawn(len(CONFIGS) * len(SWEEP_D))

    sep = "=" * 84
    print(sep)
    print("Stage 7 -- Cut C (N=3) commensurability comparison")
    print(sep)
    print(f"Scope: R={R}, n_max default={N_MAX_DEFAULT}, "
          f"convergence check n_max={N_MAX_CONVERGENCE}")
    print(f"Sweep parameter D = Delta_1 in {SWEEP_D}")
    print(f"Configs: {[c[0] for c in CONFIGS]}")
    print(f"Parent seed: {PARENT_SEED}")
    print(sep)

    all_records = {}
    ss_idx = 0
    t_start = time.time()
    for cfg_label, cfg_desc, r1, r2, r3 in CONFIGS:
        for D in SWEEP_D:
            ss = child_ss[ss_idx]; ss_idx += 1
            key = f"{cfg_label}_D{D:+.2f}"
            print(f"\n--- {key}: {cfg_desc}, (Delta_1, Delta_2, Delta_3) = "
                  f"({D:+.3f}, {r2*D:+.3f}, {r3*D:+.3f}) ---", flush=True)
            rec = analyse_point(
                cfg_label, cfg_desc, D, r2, r3, ss, times,
                SIGMA_DELTA, G, N_MAX_DEFAULT, R, M_VALUES,
            )
            all_records[key] = {"config": cfg_label, "config_desc": cfg_desc,
                                 **rec}

            t1000 = rec["timing"][1000]
            print(f"  C_bar = {rec['C_bar']:.3f},  "
                  f"f_res(1e3) = {t1000['f_resolved']:.3f},  "
                  f"f/cyc(slow) = {t1000['f_per_cycle_slow']:.3f}", flush=True)
            print(f"  Pearson: growth = {rec['pearson_growth']:+.3f}, "
                  f"series = {rec['pearson_series']:+.3f}, "
                  f"per-mode = {[f'{r:+.2f}' for r in rec['pearson_per_mode']]}",
                  flush=True)
            print(f"  Peak-offset complementarity: "
                  f"n sigma^2 peaks = {rec['peak_offsets']['n_sigma2_peaks']}, "
                  f"n C peaks = {rec['peak_offsets']['n_C_peaks']}, "
                  f"mean |lag| = {rec['peak_offsets']['mean_abs_lag']:.2f}",
                  flush=True)
            print(f"  Product test: C*sigma^2 mean = "
                  f"{rec['complementarity_product']['mean']:.3e}, "
                  f"peak = {rec['complementarity_product']['peak']:.3e}",
                  flush=True)
            ipr = rec["ipr_at_peak"]
            print(f"  IPR*n_eff at peak (t={ipr['t_peak']:.2f}): "
                  f"mode 1 = {ipr['ipr_times_neff'][0]:.3f}, "
                  f"mode 2 = {ipr['ipr_times_neff'][1]:.3f}, "
                  f"mode 3 = {ipr['ipr_times_neff'][2]:.3f}", flush=True)
            conv = rec["convergence"]
            print(f"  Convergence (p_10 vs p_12): {conv['err']:.3e}  "
                  f"{'PASS' if conv['pass'] else 'FAIL'}", flush=True)
            tb = rec["timing_budget"]
            print(f"  Runtime: ensemble={tb['ensemble_s']:.1f}s, "
                  f"conv n=10: {tb['conv_n10_s']:.1f}s, "
                  f"conv n=12: {tb['conv_n12_s']:.1f}s", flush=True)

    t_total = time.time() - t_start
    print(f"\n{sep}\nTotal Cut C runtime: {t_total/60:.2f} min", flush=True)

    # ---- Figure ----
    FIGURES.mkdir(exist_ok=True)
    fig = plt.figure(figsize=(13.5, 10))
    gs = fig.add_gridspec(4, 3, height_ratios=[1, 1, 1, 1.2], hspace=0.55,
                          wspace=0.35)

    # Rows 1-3: one panel per config, sigma^2 + C on twin axis, per D
    for col, (cfg_label, cfg_desc, _, r2, r3) in enumerate(CONFIGS):
        for row, D in enumerate(SWEEP_D):
            key = f"{cfg_label}_D{D:+.2f}"
            rec = all_records[key]
            ax = fig.add_subplot(gs[row, col])
            ax2 = ax.twinx()
            ax.plot(times, rec["sigma2"], "C3-", lw=1.1,
                    label=r"$\sigma^2$")
            ax2.plot(times, rec["C_mean"], "C0-", lw=1.1,
                     label=r"$\mathcal{C}$")
            ax.set_title(
                rf"{key}: $\bar{{\mathcal{{C}}}}={rec['C_bar']:.3f}$, "
                rf"$r_{{growth}}={rec['pearson_growth']:+.2f}$", fontsize=9,
            )
            ax.tick_params(labelsize=7)
            ax2.tick_params(labelsize=7)
            if row == 0 and col == 0:
                ax.legend(loc="upper left", frameon=False, fontsize=7)
                ax2.legend(loc="upper right", frameon=False, fontsize=7)

    # Row 4: aggregate comparison panels
    ax_h3 = fig.add_subplot(gs[3, 0:2])
    for cfg_label, cfg_desc, _, r2, r3 in CONFIGS:
        fres = [all_records[f"{cfg_label}_D{D:+.2f}"]["timing"][1000]["f_resolved"]
                for D in SWEEP_D]
        cbars = [all_records[f"{cfg_label}_D{D:+.2f}"]["C_bar"]
                 for D in SWEEP_D]
        ax_h3.plot(cbars, fres, "o-", label=cfg_label, lw=1.4, markersize=9)
        for D, f, cb in zip(SWEEP_D, fres, cbars):
            ax_h3.annotate(f"D={D:.2f}", (cb, f),
                           textcoords="offset points", xytext=(5, 5),
                           fontsize=8)
    ax_h3.set_xlabel(r"$\bar{\mathcal{C}}$")
    ax_h3.set_ylabel(r"$f_{\mathrm{resolved}}(M=10^3)$")
    ax_h3.set_title(r"H3 cross-config scatter: $\bar{\mathcal{C}}$ vs $f_{\mathrm{resolved}}$")
    ax_h3.legend(loc="best", frameon=False, fontsize=9)
    ax_h3.grid(alpha=0.3)

    # Per-mode Pearson bar chart
    ax_pm = fig.add_subplot(gs[3, 2])
    x = np.arange(3)
    width = 0.25
    for i, (cfg_label, *_rest) in enumerate(CONFIGS):
        rk = all_records[f"{cfg_label}_D+0.15"]["pearson_per_mode"]
        ax_pm.bar(x + (i - 1) * width, rk, width=width, label=cfg_label,
                  alpha=0.8)
    ax_pm.axhline(0, color="k", lw=0.5)
    ax_pm.set_xticks(x)
    ax_pm.set_xticklabels(["mode 1", "mode 2", "mode 3"])
    ax_pm.set_ylabel(r"$r(\sigma^2, |\dot{\mathcal{C}}^{(k)}|)$")
    ax_pm.set_title(r"Per-mode H2 (growth), $D=+0.15$")
    ax_pm.legend(loc="best", frameon=False, fontsize=8)
    ax_pm.grid(alpha=0.3)

    fig.suptitle("Stage 7 -- Cut C commensurability comparison (N=3)",
                 fontsize=12)
    fig.savefig(FIGURES / "stage7_cutC_sweep.pdf", bbox_inches="tight")
    print(f"\nFigure: figures/stage7_cutC_sweep.pdf", flush=True)

    # ---- metrics.json ----
    def serialise(rec):
        return {
            "config": rec["config"],
            "config_desc": rec["config_desc"],
            "D": rec["D"],
            "Delta_triplet": list(rec["Delta_triplet"]),
            "C_bar": rec["C_bar"],
            "pearson_growth_aggregate": rec["pearson_growth"],
            "pearson_series_aggregate": rec["pearson_series"],
            "pearson_growth_per_mode": rec["pearson_per_mode"],
            "timing_by_M": {str(M): rec["timing"][M] for M in M_VALUES},
            "peak_offsets": rec["peak_offsets"],
            "complementarity_product": rec["complementarity_product"],
            "ipr_at_peak": rec["ipr_at_peak"],
            "convergence_vs_n_max_12": rec["convergence"],
            "runtime_s": rec["timing_budget"],
        }

    metrics = {
        "parameters": {
            "g": G, "sigma_Delta": SIGMA_DELTA, "R": R,
            "n_max_default": N_MAX_DEFAULT,
            "n_max_convergence": N_MAX_CONVERGENCE,
            "t_max": T_MAX, "n_times": N_TIMES, "M_values": M_VALUES,
            "sweep_D": SWEEP_D,
            "parent_seed": PARENT_SEED,
            "scope_reduction_note": (
                "v0.2 §4 spec: 3 configs x 4 D x 100 R = 1200 traj at n_max=12. "
                "Runtime infeasible (>30h at dim=4394 eigh). Reduced to "
                "3 configs x 2 D x 30 R = 180 traj at n_max=10 (~65min). "
                "Convergence spot-checked via noiseless p(t) at n_max=10 vs 12 "
                "per point (absolute target <= 1e-4). See notes.md."
            ),
        },
        "results": {k: serialise(v) for k, v in all_records.items()},
        "total_runtime_min": t_total / 60,
    }
    (HERE / "metrics.json").write_text(json.dumps(metrics, indent=2, default=float))
    return metrics


if __name__ == "__main__":
    main()
