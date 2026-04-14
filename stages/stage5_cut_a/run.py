"""Stage 5 -- Cut A (single-mode detuning sweep).

Per VOYAGE_PLAN.md v0.2 §6 Stage 5. Six-point detuning sweep at N=1,
|Delta|/omega_ref in {0.15, 0.30, 0.50}, both signs; R=100 realisations
per point with Gaussian Delta-noise sigma_Delta=0.01.

Seeding protocol (per Guardian Stage-5 pre-run pin):
- Parent SeedSequence from a fixed parent_seed.
- Six child SeedSequences, one per Delta point, via ``.spawn(6)`` on the
  parent. Ordering: Delta values sorted ascending.
- Each child seeds a dedicated numpy.random.default_rng() for that
  point's R=100 detuning draws. The same draws feed both n_max=12 and
  n_max=18 propagations, so Gate 11 compares apples-to-apples on the
  observable, not on random structure.

Per-point outputs (recorded to metrics.json):
- Trajectories: p_mean(t), sigma^2_intrinsic(t), n_eff_mean(t), C(t),
  |dC/dt|(t) at n_max=18.
- Detectability timing: t_rise(M), T_det(M), f_resolved(M) for
  M in {100, 1000, 10000}.
- Complexity summary: C_bar (time-average over the resolvable window).
- H2-relevant: Pearson r(sigma^2, |dC/dt|) over the resolvable window.
- QFI-reduction: median relative deviation
  |sigma^2_intrinsic - (d_Delta p)^2 sigma_Delta^2| / sigma^2_intrinsic
  on the mask sigma^2 > 1e-8; watch-item per Guardian reminder 2.
- Short-time fit coefficients: (c_2(Delta), c_4(Delta)).

Sweep-wide:
- Gate 11: for each point, max |sigma^2(n_max=12) - sigma^2(n_max=18)| <= 1e-5.
- H3 headline scatter: f_resolved(M=1000) vs C_bar across the six points.
"""

from __future__ import annotations

import json
import sys
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
    finite_difference_dpdDelta,
    qpn_floor,
    resolved_fraction,
    run_ensemble_single_mode,
    sample_detunings,
    t_det,
    t_rise,
)
from observables import schmidt_eigenvalues_n1


PARENT_SEED = 2026_04_15  # v0.2 Cut A launch seed; PA-05 onwards uses the
                          # SeedSequence spawn pattern locked here.


def run_point(Delta_nom, g, sigma_Delta, R, n_max, times, seed_seq):
    """One parameter-point ensemble at a given n_max."""
    rng = np.random.default_rng(seed_seq)
    Delta_sample = sample_detunings(Delta_nom, sigma_Delta, R, rng=rng)
    ens = run_ensemble_single_mode(Delta_sample, g=g, n_max=n_max, times=times)
    return ens, Delta_sample


def per_point_metrics(ens, times, Delta_nom, sigma_Delta, g, M_values):
    """Compute every Stage-5 per-point diagnostic from one ensemble."""
    p_mean = ensemble_mean(ens["p"])
    p_var = ensemble_variance(ens["p"])
    n_eff_mean = ensemble_mean(ens["n_eff"])
    C = np.log(np.maximum(n_eff_mean, 1e-30))
    dCdt = np.gradient(C, times)
    abs_dCdt = np.abs(dCdt)

    # Resolvable-window mask
    mask = p_var > 1e-8
    if np.any(mask):
        t_m = times[mask]
        sigma2_m = p_var[mask]
        C_m = C[mask]
        abs_dCdt_m = abs_dCdt[mask]
        C_bar = float(np.trapezoid(C_m, t_m) / (t_m[-1] - t_m[0]))
        pearson = float(np.corrcoef(sigma2_m, abs_dCdt_m)[0, 1])
    else:
        C_bar = float("nan")
        pearson = float("nan")

    # Detectability timing per M
    timing = {}
    for M in M_values:
        qpn = qpn_floor(p_mean, M)
        timing[M] = {
            "t_rise": t_rise(p_var, qpn, times),
            "T_det": t_det(p_var, qpn, times),
            "f_resolved": resolved_fraction(p_var, qpn),
        }

    return {
        "p_mean": p_mean,
        "sigma2": p_var,
        "n_eff_mean": n_eff_mean,
        "C": C,
        "abs_dCdt": abs_dCdt,
        "C_bar": C_bar,
        "pearson_sigma2_absDCdt": pearson,
        "timing": timing,
    }


def qfi_reduction_check(Delta_nom, g, sigma_Delta, n_max, times, sigma2):
    """Scout C2 small-noise reduction vs the measured ensemble variance."""
    dp = finite_difference_dpdDelta(
        Delta_nominal=Delta_nom, g=g, n_max=n_max, times=times, eps=1e-3
    )
    sigma2_qfi = dp ** 2 * sigma_Delta ** 2
    mask = sigma2 > 1e-8
    if np.any(mask):
        rel = np.abs(sigma2_qfi[mask] - sigma2[mask]) / sigma2[mask]
        return {
            "median_rel_dev": float(np.median(rel)),
            "max_rel_dev": float(np.max(rel)),
            "sigma2_qfi": sigma2_qfi,
        }
    return {"median_rel_dev": float("nan"),
            "max_rel_dev": float("nan"), "sigma2_qfi": sigma2_qfi}


def short_time_fit(ens, times, n_max):
    """Fit lambda_2(t) = c2*t^2 + c4*t^4 on the first 1% of the window
    using realisation 0 (any single trajectory suffices since lambda_2
    is a deterministic function of Delta at the per-trajectory level)."""
    n_times = len(times)
    states_0 = run_ensemble_single_mode.__wrapped__ if False else None
    # Just use a single clean noiseless run at Delta_nom:
    # Actually we already have the ensemble; take the first trajectory's
    # lambda_2 approximation by running a single clean Delta_nom propagation.
    # For simplicity and correctness, re-propagate at Delta_nom noiseless.
    from hamiltonian import initial_state_up_vacuum, single_mode_hamiltonian
    from propagate import propagate_eigendecomp
    Delta_nom = ens.get("Delta_nom_for_fit") if isinstance(ens, dict) else None
    raise NotImplementedError("wrapper not used; inline in main")


def main():
    g = 0.1
    sigma_Delta = 0.01
    R = 100
    t_max = 50.0
    n_times = 500
    times = np.linspace(0.0, t_max, n_times)
    M_values = [100, 1000, 10_000]

    Delta_set = sorted([-0.5, -0.3, -0.15, +0.15, +0.3, +0.5])
    n_points = len(Delta_set)
    n_max_default = 12
    n_max_conv = 18

    # SeedSequence spawn pattern
    parent_ss = np.random.SeedSequence(PARENT_SEED)
    child_ss = parent_ss.spawn(n_points)

    sep = "=" * 80
    print(sep)
    print("Stage 5 -- Cut A single-mode detuning sweep (VOYAGE_PLAN v0.2 §6)")
    print(sep)
    print(f"Parent seed: {PARENT_SEED}   (SeedSequence.spawn({n_points}) for per-Delta rngs)")
    print(f"Delta set:   {Delta_set}")
    print(f"sigma_Delta = {sigma_Delta}, R = {R}, n_max in ({n_max_default}, {n_max_conv})")
    print(sep)

    per_point = {}
    convergence_errors = []
    gate11_passes = []

    for i, Delta in enumerate(Delta_set):
        # Run both n_max values using the same seeded RNG draws.
        # To use identical draws across n_max, resample from a fresh rng
        # constructed from the same SeedSequence twice (rngs sampled the
        # same way will produce identical numbers; we achieve this by
        # spawning once per n_max from the same child_ss, which keeps
        # point-i deterministic but gives the two n_max values the same
        # Delta_sample).
        ss_for_draws = child_ss[i]
        # Two RNGs seeded identically (equivalent to one draw reused):
        draw_rng = np.random.default_rng(ss_for_draws)
        Delta_sample = sample_detunings(Delta, sigma_Delta, R, rng=draw_rng)

        ens_12 = run_ensemble_single_mode(
            Delta_sample, g=g, n_max=n_max_default, times=times
        )
        ens_18 = run_ensemble_single_mode(
            Delta_sample, g=g, n_max=n_max_conv, times=times
        )
        m12 = per_point_metrics(ens_12, times, Delta, sigma_Delta, g, M_values)
        m18 = per_point_metrics(ens_18, times, Delta, sigma_Delta, g, M_values)

        # Gate 11: sigma^2 convergence
        err_conv = float(np.max(np.abs(m12["sigma2"] - m18["sigma2"])))
        convergence_errors.append(err_conv)
        gate11 = err_conv <= 1e-5
        gate11_passes.append(gate11)

        # QFI reduction at n_max=18
        qfi = qfi_reduction_check(Delta, g, sigma_Delta, n_max_conv, times, m18["sigma2"])

        # Short-time fit: propagate noiselessly at Delta_nom and fit lambda_2
        from hamiltonian import initial_state_up_vacuum, single_mode_hamiltonian
        from propagate import propagate_eigendecomp
        H_nom = single_mode_hamiltonian(Delta=Delta, g=g, n_max=n_max_conv)
        psi0 = initial_state_up_vacuum(n_max_conv)
        states_nom = propagate_eigendecomp(H_nom, psi0, times)
        lambda2 = np.empty(n_times)
        for j in range(n_times):
            lam = schmidt_eigenvalues_n1(states_nom[j], n_max_conv)
            lambda2[j] = lam[1]
        fit_end = int(0.01 * n_times) + 1
        t_fit = times[1:fit_end]
        X = np.column_stack([t_fit ** 2, t_fit ** 4])
        coeffs, *_ = np.linalg.lstsq(X, lambda2[1:fit_end], rcond=None)
        c2_fit, c4_fit = float(coeffs[0]), float(coeffs[1])

        per_point[Delta] = {
            "sigma2_12": m12["sigma2"],
            "sigma2_18": m18["sigma2"],
            "p_mean_18": m18["p_mean"],
            "n_eff_mean_18": m18["n_eff_mean"],
            "C_18": m18["C"],
            "abs_dCdt_18": m18["abs_dCdt"],
            "C_bar": m18["C_bar"],
            "pearson": m18["pearson_sigma2_absDCdt"],
            "timing": m18["timing"],
            "qfi_median_rel_dev": qfi["median_rel_dev"],
            "qfi_max_rel_dev": qfi["max_rel_dev"],
            "sigma2_qfi": qfi["sigma2_qfi"],
            "c2": c2_fit,
            "c4": c4_fit,
            "convergence_err": err_conv,
            "gate11_pass": gate11,
        }

        print(
            f"Delta = {Delta:+.2f}   "
            f"f_res(M=1e3) = {m18['timing'][1000]['f_resolved']:.3f}   "
            f"t_rise(M=1e3) = {m18['timing'][1000]['t_rise']:>5.2f}   "
            f"C_bar = {m18['C_bar']:.3f}   "
            f"r(sig2,|dCdt|) = {m18['pearson_sigma2_absDCdt']:+.3f}   "
            f"QFI med rel dev = {qfi['median_rel_dev']:.2%}   "
            f"|sig2_12 - sig2_18| = {err_conv:.2e}  "
            f"{'PASS' if gate11 else 'FAIL'}"
        )

    all_gate11 = all(gate11_passes)
    max_conv_err = max(convergence_errors)

    print(sep)
    print(f"Gate 11 (sigma^2 convergence, all Cut A points, target 1e-5):")
    print(f"   max across points = {max_conv_err:.3e}   "
          f"{'ALL PASS' if all_gate11 else 'FAIL on at least one point'}")
    print(sep)

    # ---- Figure: H3 scatter + per-point overlays ----
    FIGURES.mkdir(exist_ok=True)
    fig = plt.figure(figsize=(13.5, 9.0))
    gs = fig.add_gridspec(3, 6, height_ratios=[1.0, 1.0, 1.2], hspace=0.55, wspace=0.50)

    # Row 1: sigma^2 vs QPN per-point at M=1000
    for i, Delta in enumerate(Delta_set):
        ax = fig.add_subplot(gs[0, i])
        p = per_point[Delta]
        qpn1000 = qpn_floor(p["p_mean_18"], 1000)
        ax.semilogy(times, p["sigma2_18"] + 1e-20, "C3-", lw=1.2,
                    label=r"$\sigma^2$")
        ax.semilogy(times, qpn1000 + 1e-20, "k--", lw=0.8,
                    label=r"$\sigma^2_{\mathrm{QPN}}$")
        t_r = p["timing"][1000]["t_rise"]
        if 0.0 < t_r < times[-1]:
            ax.axvline(t_r, color="C2", ls=":", alpha=0.7)
        ax.set_title(rf"$\Delta = {Delta:+.2f}$", fontsize=9)
        ax.set_xticks([0, 25, 50])
        if i == 0:
            ax.set_ylabel(r"variance", fontsize=9)
            ax.legend(loc="lower right", frameon=False, fontsize=7)
        ax.tick_params(labelsize=8)

    # Row 2: n_eff envelope per-point
    for i, Delta in enumerate(Delta_set):
        ax = fig.add_subplot(gs[1, i])
        p = per_point[Delta]
        ax.plot(times, p["n_eff_mean_18"], "C0-", lw=1.2)
        ax.axhline(2.0, color="k", ls=":", alpha=0.4)
        ax.axhline(np.exp(p["C_bar"]), color="C3", ls="--", lw=0.8, alpha=0.8,
                   label=rf"$\bar{{\mathcal{{C}}}}={p['C_bar']:.2f}$")
        ax.set_xticks([0, 25, 50])
        ax.set_ylim(0.95, 2.05)
        if i == 0:
            ax.set_ylabel(r"$\bar n_{\mathrm{eff}}^{(1)}(t)$", fontsize=9)
        ax.legend(loc="lower right", frameon=False, fontsize=7)
        ax.tick_params(labelsize=8)

    # Row 3 left: H3 headline scatter
    ax_H3 = fig.add_subplot(gs[2, 0:3])
    f_res_list = [per_point[D]["timing"][1000]["f_resolved"] for D in Delta_set]
    C_bar_list = [per_point[D]["C_bar"] for D in Delta_set]
    colors = ["C0" if D < 0 else "C3" for D in Delta_set]
    ax_H3.scatter(f_res_list, C_bar_list, c=colors, s=100, alpha=0.85,
                  edgecolors="k", linewidths=0.8)
    for D, f, cbar in zip(Delta_set, f_res_list, C_bar_list):
        ax_H3.annotate(f"{D:+.2f}", (f, cbar), textcoords="offset points",
                       xytext=(8, -4), fontsize=9)
    ax_H3.set_xlabel(r"$f_{\mathrm{resolved}}(M=1000)$")
    ax_H3.set_ylabel(r"$\bar{\mathcal{C}}$")
    ax_H3.set_title(r"(H3 headline) $f_{\mathrm{resolved}}$ vs "
                    r"$\bar{\mathcal{C}}$ across Cut A")
    ax_H3.grid(alpha=0.3)

    # Row 3 right: per-point Pearson + QFI trends
    ax_trend = fig.add_subplot(gs[2, 3:])
    abs_Delta_list = [abs(D) for D in Delta_set]
    pearson_list = [per_point[D]["pearson"] for D in Delta_set]
    qfi_med_list = [per_point[D]["qfi_median_rel_dev"] for D in Delta_set]
    # collapse +-Delta into |Delta| for trend display
    abs_Deltas_unique = sorted(set(abs_Delta_list))
    pearson_by_absD = {ad: [] for ad in abs_Deltas_unique}
    qfi_by_absD = {ad: [] for ad in abs_Deltas_unique}
    for D, pear, qmed in zip(Delta_set, pearson_list, qfi_med_list):
        pearson_by_absD[abs(D)].append(pear)
        qfi_by_absD[abs(D)].append(qmed)
    abs_xs = abs_Deltas_unique
    pearson_means = [np.mean(pearson_by_absD[a]) for a in abs_xs]
    qfi_means = [np.mean(qfi_by_absD[a]) for a in abs_xs]
    ax_trend.plot(abs_xs, pearson_means, "C2o-",
                  label=r"mean $r(\sigma^2,|\dot{\mathcal{C}}|)$")
    ax_trend.plot(abs_xs, qfi_means, "C1s--",
                  label=r"mean QFI median rel. dev.")
    ax_trend.axhline(0.10, color="k", ls=":", alpha=0.5,
                     label=r"$10\%$ QFI gate 8 bar")
    ax_trend.set_xlabel(r"$|\Delta|/\omega_{\mathrm{ref}}$")
    ax_trend.set_ylabel("correlation / deviation")
    ax_trend.set_title(r"Sweep-wide: H2 correlation and QFI reduction")
    ax_trend.grid(alpha=0.3)
    ax_trend.legend(loc="best", frameon=False, fontsize=8)

    fig.suptitle(
        "Stage 5 -- Cut A single-mode detuning sweep (N=1; 6 points)",
        fontsize=12,
    )
    fig.savefig(FIGURES / "stage5_cutA_sweep.pdf", bbox_inches="tight")
    print(f"Figure: figures/stage5_cutA_sweep.pdf")

    # ---- metrics.json ----
    def serialise(p):
        return {
            "C_bar": p["C_bar"],
            "pearson_sigma2_absDCdt": p["pearson"],
            "timing_by_M": {
                str(M): {k: (float(v) if not isinstance(v, dict) else v)
                         for k, v in p["timing"][M].items()}
                for M in M_values
            },
            "qfi_median_rel_dev": p["qfi_median_rel_dev"],
            "qfi_max_rel_dev": p["qfi_max_rel_dev"],
            "c2": p["c2"],
            "c4": p["c4"],
            "convergence_err_sigma2_12_vs_18": p["convergence_err"],
            "gate11_pass": p["gate11_pass"],
        }

    metrics = {
        "sweep_parameters": {
            "g": g, "sigma_Delta": sigma_Delta, "R": R, "n_max_default": n_max_default,
            "n_max_convergence": n_max_conv, "t_max": t_max, "n_times": n_times,
            "M_values": M_values, "Delta_set": Delta_set,
            "parent_seed": PARENT_SEED,
            "seeding": "np.random.SeedSequence(parent).spawn(n_points)",
        },
        "per_point": {f"{D:+.2f}": serialise(per_point[D]) for D in Delta_set},
        "gate11_summary": {
            "target": 1e-5,
            "max_conv_err_across_points": max_conv_err,
            "all_pass": all_gate11,
        },
        "h3_headline": {
            "f_resolved_M1000_by_Delta": {
                f"{D:+.2f}": per_point[D]["timing"][1000]["f_resolved"]
                for D in Delta_set
            },
            "C_bar_by_Delta": {f"{D:+.2f}": per_point[D]["C_bar"] for D in Delta_set},
        },
        "qfi_watch": {
            "description": ("Guardian pre-Cut-A reminder 2: watch for QFI "
                            "reduction degradation at innermost points "
                            "(|Delta|=0.15) vs outer (|Delta|=0.5) as "
                            "evidence of crossover toward second-order "
                            "dominance."),
            "median_rel_dev_by_abs_Delta": {
                f"{abs(D):.2f}": per_point[D]["qfi_median_rel_dev"]
                for D in Delta_set
            },
        },
    }
    (HERE / "metrics.json").write_text(json.dumps(metrics, indent=2))
    return metrics


if __name__ == "__main__":
    main()
