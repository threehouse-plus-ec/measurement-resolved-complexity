"""Stage 6 -- Cut B (two-mode configurations, N=2).

Per VOYAGE_PLAN v0.2 §4 and §6. Four structured (Delta_1, Delta_2)
configurations at N=2, R=100 ensemble per point.

Gates:
  Gate 11-N2 -- per-point sigma^2 convergence, n_max=12 vs 18, target 1e-5.
  Gate 12    -- IPR test at the first Cut B point (C3.4 semantic-overclaim
                concern). Compute IPR * n_eff for each mode; value ~= 1
                supports the literal "uniform over n_eff modes" reading;
                departure activates Scout C3.4. Logged as a ratio diagnostic
                rather than pass/fail since there is no a-priori threshold
                for "clean peakedness"; Stage 6 notes record the reading.
  Gate 13    -- Full H2 test at N=2. Schmidt rank bound loosens to
                min(n_max+1, 2*(n_max+1)) = 13 at n_max=12; C(t) has
                dynamical range beyond the log-2 bound that capped
                Stage 4's N=1 series-direct test. Test both series-direct
                and growth-framing at each Cut B point.

Guardian middle-path items (pinned at Stage 6 clearance):
- Log both f_resolved (bare) and f_resolved_per_cycle (window-normalised
  by the slowest mode period 2 pi / min(|Delta_1|, |Delta_2|)). Stage 8
  chooses between the two without re-running.
- Window-effect control: explicit ratio f_res / f_res_per_cycle reported
  per-point to surface whether the Stage 5 Finding 2 (non-monotonicity
  as window-normalisation artefact) persists or breaks at N=2.
- IPR / Gate 12 weighted: ratio IPR * n_eff reported for each mode at
  each Cut B point.

Seeding: parent SeedSequence(20260416).spawn(4), one per Cut B point.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SRC = REPO / "src"
FIGURES = REPO / "figures"
sys.path.insert(0, str(SRC))

from ensemble import (
    ensemble_mean,
    ensemble_variance,
    finite_difference_dpdDelta_n2,
    qpn_floor,
    resolved_fraction,
    resolved_per_cycle,
    run_ensemble_two_mode,
    sample_detunings,
    t_det,
    t_rise,
)
from observables import (
    aggregate_complexity_series,
    ipr_per_mode_at_time,
    n_eff_from_eigenvalues,
    n_eff_per_mode_series_n2,
    reduced_mode_matrices_n2,
    spin_up_population_n2,
)


PARENT_SEED = 2026_04_16


CONFIGS = [
    ("B1", +0.15, +0.15, "symmetric near-resonance (innermost each)"),
    ("B2", +0.15, +0.30, "mild asymmetry, both near-ish resonance"),
    ("B3", -0.15, +0.15, "symmetric straddling of resonance"),
    ("B4", +0.15, +0.50, "strong asymmetry (inner + outer)"),
]


def slowest_period(Delta_1, Delta_2):
    """2 pi / min(|Delta_1|, |Delta_2|): conservative characteristic period."""
    md = min(abs(Delta_1), abs(Delta_2))
    if md <= 0:
        return float("inf")
    return 2.0 * np.pi / md


def beat_period(Delta_1, Delta_2):
    """2 pi / |Delta_1 - Delta_2| if modes differ, else inf."""
    diff = abs(Delta_1 - Delta_2)
    if diff <= 0:
        return float("inf")
    return 2.0 * np.pi / diff


def run_config(Delta_1, Delta_2, sigma_Delta, g, R, n_max, times, rng):
    d1 = sample_detunings(Delta_1, sigma_Delta, R, rng=rng)
    rng2 = np.random.default_rng(rng.bit_generator.random_raw())
    d2 = sample_detunings(Delta_2, sigma_Delta, R, rng=rng2)
    ens = run_ensemble_two_mode(d1, d2, g=g, n_max=n_max, times=times)
    return ens, d1, d2


def per_config_metrics(ens, times, Delta_1, Delta_2, g, sigma_Delta, M_values,
                       n_max):
    p_mean = ensemble_mean(ens["p"])
    p_var = ensemble_variance(ens["p"])
    n_eff_1_mean = ensemble_mean(ens["n_eff_1"])
    n_eff_2_mean = ensemble_mean(ens["n_eff_2"])
    C = ensemble_mean(ens["C"])
    dCdt = np.gradient(C, times)
    abs_dCdt = np.abs(dCdt)

    mask = p_var > 1e-8
    if np.any(mask):
        t_m = times[mask]
        C_m = C[mask]
        sigma2_m = p_var[mask]
        abs_dCdt_m = abs_dCdt[mask]
        C_bar = float(np.trapezoid(C_m, t_m) / (t_m[-1] - t_m[0]))
        pearson_growth = float(np.corrcoef(sigma2_m, abs_dCdt_m)[0, 1])
        pearson_series = float(np.corrcoef(sigma2_m, C_m)[0, 1])
    else:
        C_bar = float("nan")
        pearson_growth = pearson_series = float("nan")

    period_slow = slowest_period(Delta_1, Delta_2)
    period_beat = beat_period(Delta_1, Delta_2)
    n_cycles_slow = float(times[-1] / period_slow) if period_slow > 0 else float("inf")
    n_cycles_beat = float(times[-1] / period_beat) if period_beat > 0 else float("inf")

    timing = {}
    for M in M_values:
        qpn_M = qpn_floor(p_mean, M)
        frac = resolved_fraction(p_var, qpn_M)
        per_cycle_slow = resolved_per_cycle(p_var, qpn_M, times, period_slow)
        per_cycle_beat = resolved_per_cycle(p_var, qpn_M, times, period_beat)
        timing[M] = {
            "t_rise": t_rise(p_var, qpn_M, times),
            "T_det": t_det(p_var, qpn_M, times),
            "f_resolved": frac,
            "f_per_cycle_slow": per_cycle_slow,
            "f_per_cycle_beat": per_cycle_beat,
        }

    # QFI reduction with independent Gaussian noises:
    # sigma^2_intrinsic ~ sigma_Delta^2 [(dp/dD1)^2 + (dp/dD2)^2]
    dpdD1, dpdD2 = finite_difference_dpdDelta_n2(
        Delta_1=Delta_1, Delta_2=Delta_2, g=g, n_max=n_max, times=times,
        eps=1e-3,
    )
    sigma2_qfi = sigma_Delta ** 2 * (dpdD1 ** 2 + dpdD2 ** 2)
    mask_q = p_var > 1e-8
    if np.any(mask_q):
        rel = np.abs(sigma2_qfi[mask_q] - p_var[mask_q]) / p_var[mask_q]
        qfi_median = float(np.median(rel))
        qfi_max = float(np.max(rel))
    else:
        qfi_median = qfi_max = float("nan")

    return {
        "p_mean": p_mean, "sigma2": p_var,
        "n_eff_1_mean": n_eff_1_mean, "n_eff_2_mean": n_eff_2_mean,
        "C": C, "abs_dCdt": abs_dCdt, "C_bar": C_bar,
        "pearson_growth": pearson_growth, "pearson_series": pearson_series,
        "timing": timing,
        "period_slow": period_slow, "period_beat": period_beat,
        "n_cycles_slow": n_cycles_slow, "n_cycles_beat": n_cycles_beat,
        "qfi_median_rel_dev": qfi_median, "qfi_max_rel_dev": qfi_max,
        "dpdD1": dpdD1, "dpdD2": dpdD2,
    }


def ipr_diagnostic_at_peak(ens_trajectory_states_noiseless, n_max,
                           times, C_series):
    """IPR and n_eff at the time of peak-C, on a noiseless trajectory."""
    i_peak = int(np.argmax(C_series))
    psi = ens_trajectory_states_noiseless[i_peak]
    rho_m1, rho_m2 = reduced_mode_matrices_n2(psi, n_max)
    w1 = np.linalg.eigvalsh(rho_m1)
    w2 = np.linalg.eigvalsh(rho_m2)
    n_eff_1 = n_eff_from_eigenvalues(w1)
    n_eff_2 = n_eff_from_eigenvalues(w2)
    ipr_1, ipr_2 = ipr_per_mode_at_time(psi, n_max)
    return {
        "t_peak": float(times[i_peak]),
        "i_peak": i_peak,
        "n_eff_1": n_eff_1, "ipr_1": ipr_1,
        "ratio_1_times": float(ipr_1 * n_eff_1),
        "ratio_1_squared": float(ipr_1 * n_eff_1 ** 2),
        "n_eff_2": n_eff_2, "ipr_2": ipr_2,
        "ratio_2_times": float(ipr_2 * n_eff_2),
        "ratio_2_squared": float(ipr_2 * n_eff_2 ** 2),
        "top_5_eigs_m1": sorted(w1, reverse=True)[:5],
        "top_5_eigs_m2": sorted(w2, reverse=True)[:5],
    }


def main():
    g = 0.1
    sigma_Delta = 0.01
    R = 100
    t_max = 50.0
    n_times = 500
    times = np.linspace(0.0, t_max, n_times)
    M_values = [100, 1000, 10_000]

    parent_ss = np.random.SeedSequence(PARENT_SEED)
    child_ss = parent_ss.spawn(len(CONFIGS))

    sep = "=" * 84
    print(sep)
    print("Stage 6 -- Cut B (N=2) configurations, v0.2 §4")
    print(sep)
    print(f"Parent seed: {PARENT_SEED}   (SeedSequence.spawn({len(CONFIGS)}))")
    print(f"sigma_Delta = {sigma_Delta}, R = {R}, n_max in (12, 18)")
    print(sep)

    all_metrics = {}

    for (label, D1, D2, description), ss in zip(CONFIGS, child_ss):
        print(f"\n--- {label}: (Delta_1, Delta_2) = ({D1:+.2f}, {D2:+.2f})  "
              f"[{description}] ---")

        # Both n_max values use the same seeded draws for the ensemble.
        rng12 = np.random.default_rng(ss)
        # Reconstruct the same rng state by using the same seed for draws:
        rng18 = np.random.default_rng(ss)

        ens_12, d1_12, d2_12 = run_config(D1, D2, sigma_Delta, g, R, 12, times, rng12)
        ens_18, d1_18, d2_18 = run_config(D1, D2, sigma_Delta, g, R, 18, times, rng18)

        # Verify the same draws (deterministic seed reuse):
        assert np.allclose(d1_12, d1_18) and np.allclose(d2_12, d2_18), \
            "draws diverged between n_max runs"

        m12 = per_config_metrics(ens_12, times, D1, D2, g, sigma_Delta,
                                  M_values, 12)
        m18 = per_config_metrics(ens_18, times, D1, D2, g, sigma_Delta,
                                  M_values, 18)
        err_conv = float(np.max(np.abs(m12["sigma2"] - m18["sigma2"])))
        gate11 = err_conv <= 1e-5

        # IPR diagnostic at the noiseless C-peak (use ensemble-mean C at n_max=18).
        from hamiltonian import initial_state_up_vacuum_n2, two_mode_hamiltonian
        from propagate import propagate_eigendecomp
        H_nom = two_mode_hamiltonian(Delta_1=D1, Delta_2=D2, g=g, n_max=18)
        psi0 = initial_state_up_vacuum_n2(18)
        states_nom = propagate_eigendecomp(H_nom, psi0, times)
        p_nom = spin_up_population_n2(states_nom, 18)
        n_eff_nom = n_eff_per_mode_series_n2(states_nom, 18)
        C_nom = aggregate_complexity_series(n_eff_nom)
        ipr_info = ipr_diagnostic_at_peak(states_nom, 18, times, C_nom)

        all_metrics[label] = {
            "Delta_1": D1, "Delta_2": D2, "description": description,
            "m18": m18, "gate11_err": err_conv, "gate11_pass": gate11,
            "ipr_diagnostic": ipr_info,
            "C_nom_range": [float(C_nom.min()), float(C_nom.max())],
            "n_eff_nom_at_peak_1": float(n_eff_nom[ipr_info["i_peak"], 0]),
            "n_eff_nom_at_peak_2": float(n_eff_nom[ipr_info["i_peak"], 1]),
        }

        # Report
        print(f"  Gate 11-N2 convergence err = {err_conv:.3e}   "
              f"target 1e-5   {'PASS' if gate11 else 'FAIL'}")
        print(f"  C_bar (ensemble)           = {m18['C_bar']:.3f}")
        print(f"  slowest period / n_cycles  = {m18['period_slow']:.2f} / "
              f"{m18['n_cycles_slow']:.2f}")
        print(f"  beat   period / n_cycles   = {m18['period_beat']:.2f} / "
              f"{m18['n_cycles_beat']:.2f}")
        for M in M_values:
            t = m18["timing"][M]
            print(f"  M = {M:>6}  t_rise = {t['t_rise']:>6.2f}   "
                  f"f_res = {t['f_resolved']:.3f}   "
                  f"f/cycle(slow) = {t['f_per_cycle_slow']:.3f}   "
                  f"f/cycle(beat) = {t['f_per_cycle_beat']:.3f}")
        print(f"  Pearson r(sigma^2, |dC/dt|) = {m18['pearson_growth']:+.3f}  "
              f"(growth-framing, H2)")
        print(f"  Pearson r(sigma^2, C)       = {m18['pearson_series']:+.3f}  "
              f"(series-direct, H2 literal)")
        print(f"  QFI median rel dev          = {m18['qfi_median_rel_dev']:.2%}")
        print(f"  IPR at C-peak (t = {ipr_info['t_peak']:.2f}):")
        print(f"     mode 1: n_eff = {ipr_info['n_eff_1']:.3f}  "
              f"IPR = {ipr_info['ipr_1']:.3f}  "
              f"IPR * n_eff = {ipr_info['ratio_1_times']:.3f}  "
              f"(= 1 for uniform-on-n_eff; IPR * n_eff^2 = "
              f"{ipr_info['ratio_1_squared']:.3f})")
        print(f"     mode 2: n_eff = {ipr_info['n_eff_2']:.3f}  "
              f"IPR = {ipr_info['ipr_2']:.3f}  "
              f"IPR * n_eff = {ipr_info['ratio_2_times']:.3f}  "
              f"(IPR * n_eff^2 = {ipr_info['ratio_2_squared']:.3f})")

    print(sep)
    all_gate11 = all(m["gate11_pass"] for m in all_metrics.values())
    print(f"Gate 11-N2 overall: {'ALL PASS' if all_gate11 else 'FAIL on >=1 point'}")
    print(sep)

    # ---------- Figures ----------
    FIGURES.mkdir(exist_ok=True)

    # Figure: per-config summary panels plus aggregate trends.
    fig = plt.figure(figsize=(13.5, 9.5))
    gs = fig.add_gridspec(3, 4, height_ratios=[1.0, 1.0, 1.2], hspace=0.55,
                          wspace=0.45)

    for i, (label, D1, D2, _desc) in enumerate(CONFIGS):
        m = all_metrics[label]["m18"]
        ax = fig.add_subplot(gs[0, i])
        qpn1000 = qpn_floor(m["p_mean"], 1000)
        ax.semilogy(times, m["sigma2"] + 1e-20, "C3-", lw=1.2,
                    label=r"$\sigma^2$")
        ax.semilogy(times, qpn1000 + 1e-20, "k--", lw=0.8,
                    label=r"$\sigma^2_{\mathrm{QPN}}$")
        ax.set_title(rf"{label}: $\Delta=({D1:+.2f}, {D2:+.2f})$", fontsize=9)
        ax.tick_params(labelsize=8)
        if i == 0:
            ax.legend(loc="lower right", frameon=False, fontsize=7)

    for i, (label, D1, D2, _desc) in enumerate(CONFIGS):
        m = all_metrics[label]["m18"]
        ax = fig.add_subplot(gs[1, i])
        ax.plot(times, m["C"], "C0-", lw=1.2, label=r"$\mathcal{C}(t)$")
        ax.plot(times, m["n_eff_1_mean"], "C2--", lw=0.9,
                label=r"$n_{\mathrm{eff}}^{(1)}$")
        ax.plot(times, m["n_eff_2_mean"], "C4:", lw=0.9,
                label=r"$n_{\mathrm{eff}}^{(2)}$")
        ax.axhline(np.log(2), color="k", ls=":", alpha=0.3)
        ax.set_title(rf"{label}: $\bar{{\mathcal{{C}}}}={m['C_bar']:.3f}$, "
                     rf"$r_{{growth}}={m['pearson_growth']:+.2f}$", fontsize=9)
        ax.tick_params(labelsize=8)
        if i == 0:
            ax.legend(loc="best", frameon=False, fontsize=7)

    # Bottom row: two summary panels
    # (left) f_resolved vs C_bar across four points
    ax_h3 = fig.add_subplot(gs[2, 0:2])
    f_res = [all_metrics[l]["m18"]["timing"][1000]["f_resolved"]
             for l, *_ in CONFIGS]
    f_res_pc = [all_metrics[l]["m18"]["timing"][1000]["f_per_cycle_slow"]
                for l, *_ in CONFIGS]
    C_bar = [all_metrics[l]["m18"]["C_bar"] for l, *_ in CONFIGS]
    labels_list = [l for l, *_ in CONFIGS]
    ax_h3.scatter(f_res, C_bar, c="C3", s=100, alpha=0.8, edgecolors="k",
                  label=r"$f_{\mathrm{resolved}}$ vs $\bar{\mathcal{C}}$")
    for lab, x, y in zip(labels_list, f_res, C_bar):
        ax_h3.annotate(lab, (x, y), textcoords="offset points", xytext=(8, 0),
                       fontsize=9)
    # Secondary axis for f_per_cycle_slow scatter
    ax_h3b = ax_h3.twiny()
    ax_h3b.scatter(f_res_pc, C_bar, c="C0", s=60, marker="s", alpha=0.7,
                   edgecolors="k",
                   label=r"$f_{\mathrm{per\_cycle}}$ vs $\bar{\mathcal{C}}$")
    ax_h3.set_xlabel(r"$f_{\mathrm{resolved}}(M=10^3)$ (bare)", color="C3")
    ax_h3b.set_xlabel(r"$f_{\mathrm{per\_cycle}}(M=10^3)$ (slow-period norm)",
                     color="C0")
    ax_h3.set_ylabel(r"$\bar{\mathcal{C}}$")
    ax_h3.set_title(
        r"(H3 headline at N=2) $\bar{\mathcal{C}}$ vs bare $f_{\mathrm{resolved}}$ "
        r"and window-normalised $f_{\mathrm{per\_cycle}}$"
    )
    ax_h3.grid(alpha=0.3)

    # (right) IPR ratio diagnostic
    ax_ipr = fig.add_subplot(gs[2, 2:])
    ipr_ratios_1 = [all_metrics[l]["ipr_diagnostic"]["ratio_1_times"]
                     for l, *_ in CONFIGS]
    ipr_ratios_2 = [all_metrics[l]["ipr_diagnostic"]["ratio_2_times"]
                     for l, *_ in CONFIGS]
    x = np.arange(len(CONFIGS))
    ax_ipr.bar(x - 0.18, ipr_ratios_1, width=0.35, label=r"mode 1",
               color="C2", alpha=0.8)
    ax_ipr.bar(x + 0.18, ipr_ratios_2, width=0.35, label=r"mode 2",
               color="C4", alpha=0.8)
    ax_ipr.axhline(1.0, color="k", ls="--", alpha=0.6,
                   label=r"$\mathrm{IPR}\cdot n_{\mathrm{eff}} = 1$ (uniform)")
    ax_ipr.set_xticks(x)
    ax_ipr.set_xticklabels(labels_list)
    ax_ipr.set_ylabel(r"$\mathrm{IPR}\cdot n_{\mathrm{eff}}$ at $\mathcal{C}$ peak")
    ax_ipr.set_title(r"Gate 12: peakedness diagnostic (IPR $\cdot$ $n_{\mathrm{eff}}$)")
    ax_ipr.legend(loc="best", frameon=False, fontsize=8)
    ax_ipr.grid(alpha=0.3)

    fig.suptitle("Stage 6 -- Cut B (N=2) four-configuration summary",
                 fontsize=12)
    fig.savefig(FIGURES / "stage6_cutB_sweep.pdf", bbox_inches="tight")
    print(f"Figure: figures/stage6_cutB_sweep.pdf")

    # ---------- metrics.json ----------
    def serialise(label):
        rec = all_metrics[label]
        m = rec["m18"]
        return {
            "Delta_1": rec["Delta_1"], "Delta_2": rec["Delta_2"],
            "description": rec["description"],
            "C_bar": m["C_bar"],
            "pearson_growth_framing": m["pearson_growth"],
            "pearson_series_direct": m["pearson_series"],
            "timing_by_M": {str(M): m["timing"][M] for M in M_values},
            "period_slow": m["period_slow"],
            "period_beat": m["period_beat"],
            "n_cycles_slow": m["n_cycles_slow"],
            "n_cycles_beat": m["n_cycles_beat"],
            "qfi_median_rel_dev": m["qfi_median_rel_dev"],
            "qfi_max_rel_dev": m["qfi_max_rel_dev"],
            "gate11_err": rec["gate11_err"],
            "gate11_pass": rec["gate11_pass"],
            "ipr_diagnostic": {
                **rec["ipr_diagnostic"],
                "top_5_eigs_m1": [float(x) for x in rec["ipr_diagnostic"]["top_5_eigs_m1"]],
                "top_5_eigs_m2": [float(x) for x in rec["ipr_diagnostic"]["top_5_eigs_m2"]],
            },
        }

    metrics = {
        "parameters": {
            "g": g, "sigma_Delta": sigma_Delta, "R": R,
            "n_max_default": 12, "n_max_convergence": 18,
            "t_max": t_max, "n_times": n_times, "M_values": M_values,
            "parent_seed": PARENT_SEED,
            "seeding": "np.random.SeedSequence(parent).spawn(len(CONFIGS))",
        },
        "configs": {lab: serialise(lab) for lab, *_ in CONFIGS},
        "gate11_summary": {
            "target": 1e-5,
            "max_err_across_configs": max(
                all_metrics[l]["gate11_err"] for l, *_ in CONFIGS
            ),
            "all_pass": all_gate11,
        },
    }
    (HERE / "metrics.json").write_text(json.dumps(metrics, indent=2))
    return metrics


if __name__ == "__main__":
    main()
