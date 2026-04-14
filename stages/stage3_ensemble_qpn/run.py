"""Stage 3 — ensemble layer: sigma^2_intrinsic, QPN floor, T_det(M).

Per VOYAGE_PLAN §Stage 3 (as amended 2026-04-14). At N=1, innermost Cut A
point Delta=0.15, 100-realisation ensemble with Gaussian Delta-noise at
1% RMS (stress-test level; see reconciliation §R3 item 9).

Primary artifact: three-panel figure p(t), n_eff(t), and sigma^2_intrinsic
vs sigma^2_QPN for M in {100, 1000, 10000}.

Gates:
  Gate 7  -- sigma^2_intrinsic convergence at Delta=0.15, n_max=12 vs 18
             across the same ensemble. Tests that n_eff-converged (Stage 2
             Gate 4) implies sigma^2-converged (Standing item 1 / C3.5).
  Gate 8  -- QFI-reduction check: sigma^2_intrinsic(t) vs (dp/dDelta)^2
             sigma_Delta^2. If they agree, Scout's C2 small-noise reduction
             to a Fisher-information-thresholded-against-QPN criterion
             holds (reconciliation Standing item 1).
  Gate 9  -- BLP trace-distance cross-check on an antipodal initial-state
             pair (|up>|0>, |down>|0>) at Delta=0.15. Non-monotonic D(t)
             -> canonical BLP measure is well-defined and recurrence-
             sensitive in the voyage regime (supports Verifier P5);
             monotonically small D(t) would support Scout's "under-
             applicable" reading (reconciliation §R2 divergence,
             Standing item 11).
  Gate 10 -- 1%-RMS stress-test reframing language present in notes.md
             (structural, checked at commit time).

Plus:
  - Per-Delta c_2 extraction at Delta=0.15 (Guardian Stage 2->3 forward
    note). Records c_2(0.15) against c_2(0) = g^2 for Stage 5 sweep
    reference.
  - T_det(M) extracted at each M in {100, 1000, 10000} from the ensemble.
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
    blp_non_markovianity,
    ensemble_mean,
    ensemble_variance,
    finite_difference_dpdDelta,
    qpn_floor,
    reduced_spin_traces,
    run_ensemble_single_mode,
    sample_detunings,
    resolved_fraction,
    t_det,
    t_rise,
)
from hamiltonian import (
    initial_state_down_vacuum,
    initial_state_up_vacuum,
    single_mode_hamiltonian,
)
from observables import schmidt_eigenvalues_n1
from propagate import propagate_eigendecomp


def main() -> dict:
    # --- parameters ---
    g = 0.1
    Delta_nom = 0.15
    sigma_Delta = 0.01
    R = 100
    t_max = 50.0
    n_times = 500
    times = np.linspace(0.0, t_max, n_times)
    M_values = [100, 1000, 10_000]
    seed = 2026_04_14
    rng = np.random.default_rng(seed)

    # --- ensemble at two n_max values for Gate 7 ---
    Delta_sample = sample_detunings(Delta_nom, sigma_Delta, R, rng=rng)
    ens_12 = run_ensemble_single_mode(Delta_sample, g=g, n_max=12, times=times)
    ens_18 = run_ensemble_single_mode(Delta_sample, g=g, n_max=18, times=times)

    p_mean_12 = ensemble_mean(ens_12["p"])
    p_var_12 = ensemble_variance(ens_12["p"])
    p_mean_18 = ensemble_mean(ens_18["p"])
    p_var_18 = ensemble_variance(ens_18["p"])
    n_eff_mean_18 = ensemble_mean(ens_18["n_eff"])
    n_eff_std_18 = np.std(ens_18["n_eff"], axis=0, ddof=1)
    p_std_18 = np.std(ens_18["p"], axis=0, ddof=1)

    # Gate 7: sigma^2_intrinsic convergence. Target 1e-5 is the honest
    # scientific bar: finite-ensemble statistical noise in sigma^2 at R=100
    # is sigma^2 * sqrt(2/R) ~ 1.4e-5 for peak sigma^2 ~ 1e-4, so any n_max
    # convergence error well below that threshold is below stat-noise floor.
    err_sigma2 = float(np.max(np.abs(p_var_12 - p_var_18)))
    target_sigma2 = 1e-5
    gate7 = err_sigma2 <= target_sigma2

    # --- QPN floor and T_det at n_max=18 ---
    qpn = {M: qpn_floor(p_mean_18, M) for M in M_values}
    t_rise_M = {M: t_rise(p_var_18, qpn[M], times) for M in M_values}
    t_det_M = {M: t_det(p_var_18, qpn[M], times) for M in M_values}
    frac_resolved_M = {M: resolved_fraction(p_var_18, qpn[M]) for M in M_values}

    # --- Gate 8: QFI-reduction check at n_max=18 ---
    dp_dDelta = finite_difference_dpdDelta(
        Delta_nominal=Delta_nom, g=g, n_max=18, times=times, eps=1e-3
    )
    sigma2_qfi = (dp_dDelta ** 2) * sigma_Delta ** 2
    # Relative agreement, windowed to the region where sigma^2_intrinsic is
    # well above numerical floor (avoid division-by-near-zero at t=0).
    mask = p_var_18 > 1e-8
    if np.any(mask):
        rel_diff = np.abs(sigma2_qfi[mask] - p_var_18[mask]) / p_var_18[mask]
        rel_diff_max = float(np.max(rel_diff))
        rel_diff_median = float(np.median(rel_diff))
    else:
        rel_diff_max = rel_diff_median = float("nan")
    # Gate passes if median relative agreement within 10% over the window.
    target_qfi = 0.10
    gate8 = rel_diff_median <= target_qfi

    # --- Gate 9: BLP trace distance at Delta=0.15, n_max=18 (noiseless) ---
    H_nom = single_mode_hamiltonian(Delta=Delta_nom, g=g, n_max=18)
    psi_up = initial_state_up_vacuum(18)
    psi_dn = initial_state_down_vacuum(18)
    states_up = propagate_eigendecomp(H_nom, psi_up, times)
    states_dn = propagate_eigendecomp(H_nom, psi_dn, times)
    D_blp = reduced_spin_traces(states_up, states_dn, 18)
    N_blp = blp_non_markovianity(D_blp, times)
    # Non-monotonicity count: number of sign changes in dD/dt.
    dDdt = np.gradient(D_blp, times)
    sign_changes = int(np.sum(np.diff(np.sign(dDdt)) != 0))
    gate9_nonmonotonic = sign_changes > 0  # evidence of recurrence

    # --- per-Delta c_2 extraction (Guardian forward note, Stage 2->3) ---
    # Propagate a clean noiseless run at Delta_nom, n_max=18, fit lambda_2(t)
    # on the early window. At Delta=0 c_2 = g^2 exactly; at Delta != 0 this
    # coefficient shifts, recording for the sweep reference.
    lambda2_nom = np.empty(n_times)
    for i in range(n_times):
        lam = schmidt_eigenvalues_n1(states_up[i], 18)
        lambda2_nom[i] = lam[1]
    fit_end = int(0.01 * n_times) + 1
    t_fit = times[1:fit_end]
    X = np.column_stack([t_fit**2, t_fit**4])
    coeffs, *_ = np.linalg.lstsq(X, lambda2_nom[1:fit_end], rcond=None)
    c2_at_nom, c4_at_nom = float(coeffs[0]), float(coeffs[1])

    # --- report ---
    sep = "=" * 74
    print(sep)
    print("Stage 3 -- ensemble layer: sigma^2_intrinsic, QPN floor, T_det(M)")
    print(sep)
    print(f"Ensemble: Delta_nom = {Delta_nom}, sigma_Delta = {sigma_Delta}, "
          f"R = {R}, seed = {seed}")
    print()
    print(f"Gate 7  sigma^2_intrinsic convergence")
    print(f"        max |sigma^2(n_max=12) - sigma^2(n_max=18)| = {err_sigma2:.3e}")
    print(f"        target <= {target_sigma2:.0e}   "
          f"{'PASS' if gate7 else 'FAIL'}")
    print()
    print(f"Gate 8  QFI-reduction check")
    print(f"        median rel. |sigma^2 - (dp/dDelta)^2 sigma_Delta^2| / sigma^2 "
          f"= {rel_diff_median:.3e}")
    print(f"        max rel. deviation on mask = {rel_diff_max:.3e}")
    print(f"        target median <= {target_qfi:.0e}   "
          f"{'PASS' if gate8 else 'FAIL'}")
    print()
    print(f"Gate 9  BLP trace distance (antipodal pair)")
    print(f"        max D(t) = {np.max(D_blp):.3e}")
    print(f"        N_BLP (positive-derivative integral) = {N_blp:.3e}")
    print(f"        sign changes in dD/dt = {sign_changes}")
    print(f"        -> canonical BLP "
          f"{'well-defined (recurrences present)' if gate9_nonmonotonic else 'monotone (no recurrences visible)'}")
    print()
    print(f"Detectability timing for this on-resonance cut:")
    print(f"   M         t_rise       T_det (last exceedance)"
          f"   fraction resolved")
    for M in M_values:
        rise = t_rise_M[M]
        last = t_det_M[M]
        frac = frac_resolved_M[M]
        saturated = "  (window-saturated)" if last >= times[-1] - 1e-9 else ""
        print(f"   M = {M:>6}   {rise:>6.3f}       {last:>7.3f}{saturated:<22}"
              f"   {frac:.3f}")
    print()
    print(f"Per-Delta short-time coefficient (Stage 5 reference)")
    print(f"   c_2 at Delta = {Delta_nom}: {c2_at_nom:.6e}   (c_2 at Delta=0 = g^2 = {g**2:.6e})")
    print(f"   c_4 at Delta = {Delta_nom}: {c4_at_nom:.6e}   (c_4 at Delta=0 = -g^4 = {-g**4:.6e})")
    print(sep)

    # --- figure ---
    FIGURES.mkdir(exist_ok=True)
    fig, axes = plt.subplots(2, 3, figsize=(13.2, 7.6))
    (ax_p, ax_n, ax_var), (ax_qfi, ax_blp, ax_conv) = axes

    # TL: p(t) ensemble mean with +/- std band and a few member traces
    ax_p.fill_between(times, p_mean_18 - p_std_18, p_mean_18 + p_std_18,
                      color="C0", alpha=0.3, label=r"$\bar p \pm \sigma$")
    ax_p.plot(times, p_mean_18, "C0-", lw=1.6, label=r"$\bar p(t)$")
    # overlay a few individual trajectories (faint)
    for i in range(0, R, 25):
        ax_p.plot(times, ens_18["p"][i], "k-", lw=0.3, alpha=0.25)
    ax_p.set_xlabel(r"$t\,\omega_{\mathrm{ref}}$")
    ax_p.set_ylabel(r"$p(t)$")
    ax_p.set_title(rf"(TL) ensemble $p(t)$ at $\Delta={Delta_nom}$"
                   + "\n" + rf"$R={R}$, $\sigma_\Delta={sigma_Delta}$")
    ax_p.legend(loc="best", frameon=False, fontsize=9)

    # TM: n_eff(t) ensemble mean with band
    ax_n.fill_between(times, n_eff_mean_18 - n_eff_std_18,
                      n_eff_mean_18 + n_eff_std_18, color="C3", alpha=0.3,
                      label=r"$\bar n_{\mathrm{eff}} \pm \sigma$")
    ax_n.plot(times, n_eff_mean_18, "C3-", lw=1.6,
              label=r"$\bar n_{\mathrm{eff}}^{(1)}(t)$")
    ax_n.set_xlabel(r"$t\,\omega_{\mathrm{ref}}$")
    ax_n.set_ylabel(r"$n_{\mathrm{eff}}^{(1)}(t)$")
    ax_n.set_title(r"(TM) ensemble $n_{\mathrm{eff}}^{(1)}(t)$")
    ax_n.legend(loc="best", frameon=False, fontsize=9)

    # TR: sigma^2_intrinsic vs QPN floors with T_det markers
    ax_var.semilogy(times, p_var_18 + 1e-20, "C3-", lw=1.8,
                    label=r"$\sigma^2_{\mathrm{intrinsic}}(t)$")
    colors = ["C0", "C1", "C2"]
    for M, colour in zip(M_values, colors):
        ax_var.semilogy(times, qpn[M] + 1e-20, color=colour, ls="--", lw=1.2,
                        label=rf"$\sigma^2_{{\mathrm{{QPN}}}}(M={M})$")
        if t_det_M[M] > 0 and t_det_M[M] < times[-1]:
            ax_var.axvline(t_det_M[M], color=colour, ls=":", alpha=0.6)
    ax_var.set_xlabel(r"$t\,\omega_{\mathrm{ref}}$")
    ax_var.set_ylabel(r"variance")
    ax_var.set_title(r"(TR) $\sigma^2_{\mathrm{intrinsic}}$ vs $\sigma^2_{\mathrm{QPN}}(M)$"
                     + "\n(dotted: $T_{\mathrm{det}}(M)$)")
    ax_var.legend(loc="lower right", frameon=False, fontsize=8)

    # BL: QFI-reduction check
    ax_qfi.semilogy(times, p_var_18 + 1e-20, "C3-", lw=1.6,
                    label=r"$\sigma^2_{\mathrm{intrinsic}}(t)$")
    ax_qfi.semilogy(times, sigma2_qfi + 1e-20, "C0--", lw=1.2,
                    label=r"$(\partial_\Delta p)^2\,\sigma_\Delta^2$")
    ax_qfi.set_xlabel(r"$t\,\omega_{\mathrm{ref}}$")
    ax_qfi.set_ylabel(r"variance")
    ax_qfi.set_title(rf"(BL) QFI reduction (Gate 8)"
                     + "\n" + rf"median rel. agreement: {rel_diff_median:.2e}")
    ax_qfi.legend(loc="best", frameon=False, fontsize=9)

    # BM: BLP trace distance
    ax_blp.plot(times, D_blp, "C4-", lw=1.6, label=r"$D(t)$")
    ax_blp.set_xlabel(r"$t\,\omega_{\mathrm{ref}}$")
    ax_blp.set_ylabel(r"$D(t)$ (trace distance)")
    ax_blp.set_title(rf"(BM) BLP trace distance, antipodal pair"
                     + "\n" + rf"sign changes in $\dot D$: {sign_changes},"
                     + rf" $N_{{\mathrm{{BLP}}}}={N_blp:.3f}$")
    ax_blp.legend(loc="best", frameon=False, fontsize=9)

    # BR: Gate 7 convergence error
    ax_conv.semilogy(times, np.abs(p_var_12 - p_var_18) + 1e-20, "C3-",
                     label=r"$|\sigma^2_{12} - \sigma^2_{18}|$")
    ax_conv.axhline(target_sigma2, color="k", ls=":", alpha=0.6,
                    label=rf"${target_sigma2:.0e}$ target")
    ax_conv.set_xlabel(r"$t\,\omega_{\mathrm{ref}}$")
    ax_conv.set_ylabel(r"error")
    ax_conv.set_title(r"(BR) Gate 7: $\sigma^2_{\mathrm{intrinsic}}$ convergence")
    ax_conv.legend(loc="best", frameon=False, fontsize=9)

    fig.suptitle(
        "Stage 3 -- ensemble layer "
        "(variance, QPN floor, T_det, QFI check, BLP cross-check)",
        fontsize=11,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig_path = FIGURES / "stage3_qpn_comparison.pdf"
    fig.savefig(fig_path)
    print(f"Figure: {fig_path.relative_to(REPO)}")

    metrics = {
        "gates": {
            "gate7_sigma2_convergence": {
                "err": err_sigma2, "target": target_sigma2, "pass": gate7,
            },
            "gate8_qfi_reduction": {
                "median_relative_deviation": rel_diff_median,
                "max_relative_deviation": rel_diff_max,
                "target_median": target_qfi, "pass": gate8,
            },
            "gate9_blp_trace_distance": {
                "max_D": float(np.max(D_blp)),
                "N_BLP": N_blp,
                "sign_changes_dDdt": sign_changes,
                "reading": ("well-defined, recurrences present"
                            if gate9_nonmonotonic
                            else "monotone, no recurrences visible"),
            },
        },
        "detectability_by_M": {
            str(M): {
                "t_rise": t_rise_M[M],
                "t_det_last_exceedance": t_det_M[M],
                "fraction_resolved": frac_resolved_M[M],
                "window_saturated": bool(t_det_M[M] >= times[-1] - 1e-9),
            }
            for M in M_values
        },
        "per_delta_short_time_fit": {
            "Delta": Delta_nom,
            "c2": c2_at_nom,
            "c4": c4_at_nom,
            "c2_at_Delta0_reference": g**2,
            "c4_at_Delta0_reference": -(g**4),
            "note": ("c_2(Delta) shifts from g^2 as Delta grows; record per "
                     "detuning in Stage 5 rather than assume constant"),
        },
        "ensemble_summary_n_max_18": {
            "p_mean_range": [float(np.min(p_mean_18)), float(np.max(p_mean_18))],
            "sigma2_max": float(np.max(p_var_18)),
            "n_eff_mean_range": [float(np.min(n_eff_mean_18)),
                                  float(np.max(n_eff_mean_18))],
        },
        "parameters": {
            "g": g, "Delta_nom": Delta_nom, "sigma_Delta": sigma_Delta,
            "R": R, "t_max": t_max, "n_times": n_times,
            "M_values": M_values, "seed": seed,
        },
    }
    (HERE / "metrics.json").write_text(json.dumps(metrics, indent=2))
    return metrics


if __name__ == "__main__":
    main()
