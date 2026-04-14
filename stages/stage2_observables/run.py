"""Stage 2 — observables layer: n_eff^{(1)}(t), spectrum, early-time fit.

Adds reduced-state diagonalisation and n_eff(t) computation on top of the
Stage 1 propagator (VOYAGE_PLAN §Stage 2). Three gates beyond Stage 1,
all derived from Guardian items and the forwarded Standing items:

Gate 4  -- n_eff(t) converges between n_max=12 and n_max=18 at the
           innermost Cut A point Delta=0.15 (Standing item 3: p(t)-
           converged does not imply n_eff-converged; re-verify).
Gate 4a -- n_eff(t) matches the closed-form target at the Delta=0
           analytic anchor (independent anchor run; exact n_eff form
           derived from Schmidt eigenvalues (1 +/- exp(-2 g^2 t^2))/2).
Gate 5  -- eigenvalue spectrum of rho^{(1)}(t) at a representative time
           has exactly two non-vanishing eigenvalues (Schmidt-rank-2
           bound at N=1). Structural; documents the "effective orbital
           count" reading as literal rather than rhetorical.
Gate 6  -- early-time fit. lambda_2(t) = (1 - exp(-2 g^2 t^2))/2 at
           Delta=0 expands to g^2 t^2 + O(t^4); fit the small-t
           coefficient numerically. Recorded for Stage 3 subtraction.

Plus Standing items carried from Stage 1:
 - initial state fixed at |up> (x) |0> (same as Stage 1);
 - report aggregate C(t) = sum_k log n_eff^{(k)}(t) as primary invariant
   (trivial at N=1; discipline in place for Stage 6).
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

from hamiltonian import initial_state_up_vacuum, single_mode_hamiltonian
from observables import (
    mode_spectrum_at_time,
    n_eff_analytic_Delta0,
    n_eff_series_n1,
    norm_squared,
    schmidt_eigenvalues_n1,
    spin_up_population,
)
from propagate import propagate_eigendecomp


def run(Delta: float, g: float, n_max: int, times: np.ndarray):
    H = single_mode_hamiltonian(Delta=Delta, g=g, n_max=n_max)
    psi0 = initial_state_up_vacuum(n_max)
    states = propagate_eigendecomp(H, psi0, times)
    return {
        "states": states,
        "p": spin_up_population(states, n_max),
        "n_eff": n_eff_series_n1(states, n_max),
        "norm": norm_squared(states),
    }


def aggregate_complexity(n_eff_per_mode: list[np.ndarray]) -> np.ndarray:
    """C(t) = sum_k log n_eff^{(k)}(t). Reporting invariant (§10 item 2)."""
    return sum(np.log(n) for n in n_eff_per_mode)


def main() -> dict:
    g = 0.1
    t_max = 50.0
    n_times = 500
    times = np.linspace(0.0, t_max, n_times)
    target = 1e-4

    # ---------- (A) Delta=0 analytic anchor, n_max=60 ----------
    n_max_A = 60
    A = run(Delta=0.0, g=g, n_max=n_max_A, times=times)
    n_eff_A_analytic = n_eff_analytic_Delta0(times, g)
    err_A = float(np.max(np.abs(A["n_eff"] - n_eff_A_analytic)))
    norm_drift_A = float(np.max(np.abs(A["norm"] - 1.0)))
    gate4a = err_A <= target

    # ---------- (B) Delta=0.15 convergence, n_max in {12, 18} ----------
    Delta_B = 0.15
    B12 = run(Delta=Delta_B, g=g, n_max=12, times=times)
    B18 = run(Delta=Delta_B, g=g, n_max=18, times=times)
    err_B = float(np.max(np.abs(B12["n_eff"] - B18["n_eff"])))
    gate4 = err_B <= target

    # ---------- (C) Spectrum inspection at a representative time ----------
    t_probe = 25.0
    i_probe = int(np.argmin(np.abs(times - t_probe)))
    spectrum_A = mode_spectrum_at_time(A["states"][i_probe], n_max_A)
    spectrum_B18 = mode_spectrum_at_time(B18["states"][i_probe], 18)
    # Gate 5: two dominant eigenvalues, rest at numerical floor
    tol_schmidt = 1e-10
    rank_A = int(np.sum(spectrum_A > tol_schmidt))
    rank_B18 = int(np.sum(spectrum_B18 > tol_schmidt))
    gate5 = (rank_A == 2) and (rank_B18 == 2)

    # ---------- (D) Early-time fit of lambda_2(t) on Delta=0 anchor ----------
    # lambda_2(t) = (1 - exp(-2 g^2 t^2)) / 2 = g^2 t^2 - g^4 t^4 + O(t^6).
    # Fit both coefficients and record for Stage 3 subtraction reference.
    lambda2_t = np.empty(n_times)
    for i in range(n_times):
        lam = schmidt_eigenvalues_n1(A["states"][i], n_max_A)
        lambda2_t[i] = lam[1] if len(lam) > 1 else 0.0
    # Fit window: first 1% of the simulation (t in (0, 0.5]), keeps t^6 ~ 1e-10.
    fit_end = int(0.01 * n_times) + 1
    t_fit = times[1:fit_end]
    lam2_fit = lambda2_t[1:fit_end]
    # Model: lambda_2 = c2 * t^2 + c4 * t^4. Least squares for (c2, c4).
    X = np.column_stack([t_fit**2, t_fit**4])
    coeffs, *_ = np.linalg.lstsq(X, lam2_fit, rcond=None)
    c2_fit, c4_fit = float(coeffs[0]), float(coeffs[1])
    c2_analytic = g**2
    c4_analytic = -(g**4)
    c2_agreement = float(abs(c2_fit - c2_analytic))
    c4_agreement = float(abs(c4_fit - c4_analytic))
    fit_residual = float(
        np.max(np.abs(lam2_fit - (c2_fit * t_fit**2 + c4_fit * t_fit**4)))
        / max(np.max(np.abs(lam2_fit)), 1e-30)
    )
    gate6 = c2_agreement <= 1e-6

    # ---------- Aggregate complexity ----------
    C_t_B18 = aggregate_complexity([B18["n_eff"]])
    C_t_A = aggregate_complexity([A["n_eff"]])

    # ---------- Report ----------
    sep = "=" * 72
    print(sep)
    print("Stage 2 -- observables layer: n_eff, spectrum, early-time fit")
    print(sep)
    print(f"(A) Delta=0 analytic anchor, n_max={n_max_A}")
    print(f"    Gate 4a: max |n_eff - n_eff_analytic|        = {err_A:.3e}"
          f"    target <= {target:.0e}    {'PASS' if gate4a else 'FAIL'}")
    print(f"    norm drift                                    = {norm_drift_A:.3e}")
    print()
    print(f"(B) Delta={Delta_B} convergence, n_max in (12, 18)")
    print(f"    Gate 4:  max |n_eff(12) - n_eff(18)|          = {err_B:.3e}"
          f"    target <= {target:.0e}    {'PASS' if gate4 else 'FAIL'}")
    print()
    print(f"(C) Spectrum inspection at t = {times[i_probe]:.2f}")
    print(f"    Gate 5:  rank(rho^(1)) above {tol_schmidt:g}")
    print(f"             Delta=0, n_max=60:   rank = {rank_A}")
    print(f"             Delta=0.15, n_max=18: rank = {rank_B18}"
          f"        {'PASS' if gate5 else 'FAIL'}")
    print(f"    top 4 eigenvalues (Delta=0):    "
          + "  ".join(f"{v:.3e}" for v in spectrum_A[:4]))
    print(f"    top 4 eigenvalues (Delta=0.15): "
          + "  ".join(f"{v:.3e}" for v in spectrum_B18[:4]))
    print()
    print(f"(D) Early-time fit lambda_2(t) = c2*t^2 + c4*t^4, Delta=0 anchor")
    print(f"    c2 fit / analytic (= g^2)             = "
          f"{c2_fit:.6e} / {c2_analytic:.6e}")
    print(f"    c4 fit / analytic (= -g^4)            = "
          f"{c4_fit:.6e} / {c4_analytic:.6e}")
    print(f"    Gate 6: |c2_fit - g^2|                 = {c2_agreement:.3e}"
          f"    target <= 1e-6    {'PASS' if gate6 else 'FAIL'}")
    print(f"    |c4_fit + g^4|                          = {c4_agreement:.3e}")
    print(f"    relative fit residual on window        = {fit_residual:.3e}")
    print(f"    fit window: t in ({t_fit[0]:.3f}, {t_fit[-1]:.3f}]")
    print(sep)

    # ---------- Figure ----------
    FIGURES.mkdir(exist_ok=True)
    fig, axes = plt.subplots(2, 2, figsize=(11.0, 7.5))
    (ax_pneff, ax_err), (ax_spec, ax_fit) = axes

    # (TL) voyage-plan canonical artifact: p(t) and n_eff(t) at Delta=0.15
    ax_p = ax_pneff
    ax_n = ax_p.twinx()
    ax_p.plot(times, B18["p"], "C0-", lw=1.4, label=r"$p(t)$")
    ax_n.plot(times, B18["n_eff"], "C3-", lw=1.4, label=r"$n_{\mathrm{eff}}^{(1)}(t)$")
    ax_p.set_xlabel(r"$t\,\omega_{\mathrm{ref}}$")
    ax_p.set_ylabel(r"$p(t)$", color="C0")
    ax_n.set_ylabel(r"$n_{\mathrm{eff}}^{(1)}(t)$", color="C3")
    ax_p.tick_params(axis="y", colors="C0")
    ax_n.tick_params(axis="y", colors="C3")
    ax_p.set_title(rf"(TL) §2.1 Hamiltonian, $\Delta={Delta_B}$, $n_{{\max}}=18$"
                   + "\n" + r"$p(t)$ and $n_{\mathrm{eff}}^{(1)}(t)$")
    ax_p.grid(alpha=0.3)

    # (TR) gate error curves
    ax_err.semilogy(times, np.abs(A["n_eff"] - n_eff_A_analytic) + 1e-18, "C2-",
                    label=r"$|n_{\mathrm{eff}} - n_{\mathrm{eff}}^{\mathrm{an.}}|$"
                          r" (Gate 4a, $\Delta=0$)")
    ax_err.semilogy(times, np.abs(B12["n_eff"] - B18["n_eff"]) + 1e-18, "C3-",
                    label=r"$|n_{\mathrm{eff},12} - n_{\mathrm{eff},18}|$"
                          r" (Gate 4, $\Delta=0.15$)")
    ax_err.axhline(target, color="k", ls=":", alpha=0.6, label=r"$10^{-4}$ target")
    ax_err.set_xlabel(r"$t\,\omega_{\mathrm{ref}}$")
    ax_err.set_ylabel("error")
    ax_err.set_title("(TR) Gate 4 / 4a error curves")
    ax_err.legend(loc="best", frameon=False, fontsize=9)

    # (BL) eigenvalue spectrum at t_probe
    k_show = min(19, len(spectrum_A), len(spectrum_B18))
    ax_spec.semilogy(np.arange(1, len(spectrum_B18) + 1),
                     np.abs(spectrum_B18) + 1e-20, "C3o-",
                     label=r"$\Delta=0.15$, $n_{\max}=18$")
    ax_spec.semilogy(np.arange(1, k_show + 1),
                     np.abs(spectrum_A[:k_show]) + 1e-20, "C2^-",
                     label=rf"$\Delta=0$, $n_{{\max}}=60$ (first {k_show})")
    ax_spec.axhline(tol_schmidt, color="k", ls=":", alpha=0.6,
                    label=rf"rank tol. {tol_schmidt:g}")
    ax_spec.set_xlabel("eigenvalue index (descending)")
    ax_spec.set_ylabel(r"$\lambda_j$ of $\rho^{(1)}$")
    ax_spec.set_title(rf"(BL) Spectrum at $t={times[i_probe]:.1f}\,\omega_{{\mathrm{{ref}}}}^{{-1}}$"
                      "\n(Gate 5: Schmidt-rank-2 bound at $N=1$)")
    ax_spec.legend(loc="best", frameon=False, fontsize=9)

    # (BR) early-time fit
    t_show_end = int(0.1 * n_times)
    t_show = times[:t_show_end]
    ax_fit.plot(t_show, lambda2_t[:t_show_end], "C3-", lw=1.6,
                label=r"$\lambda_2(t)$ numeric")
    ax_fit.plot(t_show, c2_fit * t_show**2 + c4_fit * t_show**4, "C0--", lw=1.2,
                label=rf"fit: $c_2 t^2 + c_4 t^4$, $c_2={c2_fit:.3e}$")
    ax_fit.plot(t_show, c2_analytic * t_show**2 + c4_analytic * t_show**4,
                "k:", lw=1.2,
                label=r"analytic: $g^2 t^2 - g^4 t^4$")
    ax_fit.axvline(times[fit_end], color="C3", ls="--", alpha=0.4,
                   label="fit window end")
    ax_fit.set_xlabel(r"$t\,\omega_{\mathrm{ref}}$")
    ax_fit.set_ylabel(r"$\lambda_2(t)$")
    ax_fit.set_title(r"(BR) Gate 6: $\lambda_2(t) \approx g^2 t^2$ at small $t$"
                     r" ($\Delta=0$)")
    ax_fit.legend(loc="best", frameon=False, fontsize=9)

    fig.suptitle(
        "Stage 2 -- observables layer (n_eff, spectrum, early-time fit)",
        fontsize=11,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig_path = FIGURES / "stage2_p_and_neff.pdf"
    fig.savefig(fig_path)
    print(f"Figure: {fig_path.relative_to(REPO)}")

    metrics = {
        "gates": {
            "gate4_convergence_Delta0p15_n_eff": {
                "err": err_B, "target": target, "pass": gate4,
            },
            "gate4a_analytic_anchor_Delta0_n_eff": {
                "err": err_A, "target": target, "pass": gate4a,
            },
            "gate5_schmidt_rank_at_N1": {
                "t_probe": float(times[i_probe]),
                "rank_Delta0_nmax60": rank_A,
                "rank_Delta0p15_nmax18": rank_B18,
                "tol": tol_schmidt,
                "pass": gate5,
            },
            "gate6_early_time_fit": {
                "model": "lambda_2(t) = c2*t^2 + c4*t^4",
                "c2_fit": c2_fit,
                "c2_analytic_g_squared": c2_analytic,
                "c2_agreement": c2_agreement,
                "c4_fit": c4_fit,
                "c4_analytic_minus_g_to_4": c4_analytic,
                "c4_agreement": c4_agreement,
                "relative_residual_on_window": fit_residual,
                "fit_window_t": [float(t_fit[0]), float(t_fit[-1])],
                "stage3_reference": {
                    "lambda_2_short_t": "c2*t^2 + c4*t^4 (Delta=0 analytic anchor)",
                    "c2": c2_fit,
                    "c4": c4_fit,
                },
                "pass": gate6,
            },
        },
        "n_eff_summary": {
            "Delta_0_nmax60": {
                "initial": float(A["n_eff"][0]),
                "final": float(A["n_eff"][-1]),
                "max": float(np.max(A["n_eff"])),
            },
            "Delta_0p15_nmax18": {
                "initial": float(B18["n_eff"][0]),
                "final": float(B18["n_eff"][-1]),
                "max": float(np.max(B18["n_eff"])),
            },
        },
        "norm_drift": {
            "Delta_0_nmax60": norm_drift_A,
            "Delta_0p15_nmax12": float(np.max(np.abs(B12["norm"] - 1.0))),
            "Delta_0p15_nmax18": float(np.max(np.abs(B18["norm"] - 1.0))),
        },
        "parameters": {
            "g": g, "t_max": t_max, "n_times": n_times,
            "Delta_anchor": 0.0, "n_max_anchor": n_max_A,
            "Delta_convergence": Delta_B, "n_max_convergence": [12, 18],
            "t_probe_spectrum": float(times[i_probe]),
        },
    }
    (HERE / "metrics.json").write_text(json.dumps(metrics, indent=2))
    return metrics


if __name__ == "__main__":
    main()
