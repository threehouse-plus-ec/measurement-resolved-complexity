"""Stage 1 — single-mode propagator validation.

Three independent validation runs, per VOYAGE_PLAN §Stage 1 (amended
2026-04-14, see PLAN_AMENDMENTS.md):

(A) Analytic-anchor run — voyage §2.1 Hamiltonian at Delta = 0, with
    n_max raised (60) specifically so the analytic Gaussian target is
    reachable. This is a propagator-correctness test, not a sweep
    point. Analytic target:
        p(t) = (1 + exp(-2 g^2 t^2)) / 2
    (Unbiased Rabi factorises in the sigma_x eigenbasis into
    conditional displacements of the mode vacuum.)

(B) Convergence run — voyage §2.1 Hamiltonian at Delta = 0.15 (the
    innermost Cut A point after the 2026-04-14 plan amendment),
    at n_max in {12, 18}. No closed-form target; the gate is
    convergence between the two Fock cutoffs.

(C) JC code-machinery sanity check — H_JC at resonance (RWA), analytic
    target cos^2(g t). Independent anchor exercising the same
    propagation infrastructure on a well-known benchmark.

Go/no-go gates:
  Gate 1 — max |p_A(n_max=60) - p_analytic(Gaussian)|  <= 1e-4
  Gate 2 — max |p_B(n_max=12) - p_B(n_max=18)|         <= 1e-4
  Gate 3 — gauge-convention statement present in notes.md
           (structural, checked at commit time)
  Plus: JC anchor (C) agreement to <= 1e-4; norm drift <= 1e-10.
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

from hamiltonian import (
    initial_state_up_vacuum,
    jc_hamiltonian,
    single_mode_hamiltonian,
)
from observables import norm_squared, spin_up_population
from propagate import propagate_eigendecomp


def run_voyage_hamiltonian(Delta: float, g: float, n_max: int, times: np.ndarray):
    H = single_mode_hamiltonian(Delta=Delta, g=g, n_max=n_max)
    psi0 = initial_state_up_vacuum(n_max)
    states = propagate_eigendecomp(H, psi0, times)
    return {
        "p": spin_up_population(states, n_max),
        "norm": norm_squared(states),
    }


def run_jc_resonance(omega: float, g: float, n_max: int, times: np.ndarray):
    H = jc_hamiltonian(omega_0=omega, omega=omega, g=g, n_max=n_max)
    psi0 = initial_state_up_vacuum(n_max)
    states = propagate_eigendecomp(H, psi0, times)
    return {
        "p": spin_up_population(states, n_max),
        "norm": norm_squared(states),
    }


def main() -> dict:
    g = 0.1
    t_max = 50.0
    n_times = 500
    times = np.linspace(0.0, t_max, n_times)
    target = 1e-4

    # ---------- (A) analytic-anchor run at Delta=0, large n_max ----------
    n_max_A = 60
    A = run_voyage_hamiltonian(Delta=0.0, g=g, n_max=n_max_A, times=times)
    p_analytic_A = 0.5 * (1.0 + np.exp(-2.0 * g**2 * times**2))
    err_A = float(np.max(np.abs(A["p"] - p_analytic_A)))
    norm_drift_A = float(np.max(np.abs(A["norm"] - 1.0)))
    gate1 = err_A <= target

    # ---------- (B) convergence run at Delta=0.05, n_max in {12, 18} ----------
    Delta_B = 0.15
    B12 = run_voyage_hamiltonian(Delta=Delta_B, g=g, n_max=12, times=times)
    B18 = run_voyage_hamiltonian(Delta=Delta_B, g=g, n_max=18, times=times)
    err_B = float(np.max(np.abs(B12["p"] - B18["p"])))
    norm_drift_B12 = float(np.max(np.abs(B12["norm"] - 1.0)))
    norm_drift_B18 = float(np.max(np.abs(B18["norm"] - 1.0)))
    gate2 = err_B <= target

    # ---------- (C) JC sanity check ----------
    n_max_C = 18
    C = run_jc_resonance(omega=1.0, g=g, n_max=n_max_C, times=times)
    p_analytic_C = np.cos(g * times) ** 2
    err_C = float(np.max(np.abs(C["p"] - p_analytic_C)))
    norm_drift_C = float(np.max(np.abs(C["norm"] - 1.0)))
    gate_C = err_C <= target

    # ---------- report ----------
    sep = "=" * 70
    print(sep)
    print("Stage 1 — single-mode propagator validation")
    print(sep)
    print(f"(A) analytic anchor, voyage §2.1 Hamiltonian, Delta=0, n_max={n_max_A}")
    print(f"    Gate 1: max |p - p_analytic(Gaussian)|   = {err_A:.3e}"
          f"   target <= {target:.0e}   {'PASS' if gate1 else 'FAIL'}")
    print(f"    norm drift max ||psi||^2 - 1             = {norm_drift_A:.3e}")
    print()
    print(f"(B) convergence, voyage §2.1 Hamiltonian, Delta={Delta_B}, n_max in {{12, 18}}")
    print(f"    Gate 2: max |p(n_max=12) - p(n_max=18)|  = {err_B:.3e}"
          f"   target <= {target:.0e}   {'PASS' if gate2 else 'FAIL'}")
    print(f"    norm drift n_max=12                      = {norm_drift_B12:.3e}")
    print(f"    norm drift n_max=18                      = {norm_drift_B18:.3e}")
    print()
    print(f"(C) JC sanity check, H_JC resonance, n_max={n_max_C}")
    print(f"    max |p - cos^2(g t)|                     = {err_C:.3e}"
          f"   target <= {target:.0e}   {'PASS' if gate_C else 'FAIL'}")
    print(f"    norm drift max ||psi||^2 - 1             = {norm_drift_C:.3e}")
    print(sep)

    # ---------- figure ----------
    FIGURES.mkdir(exist_ok=True)
    fig, axes = plt.subplots(2, 3, figsize=(13.0, 6.8))
    (ax_A, ax_B, ax_C), (ax_eA, ax_eB, ax_eC) = axes

    # (A) state curves
    ax_A.plot(times, p_analytic_A, "k-", lw=1.8,
              label=r"analytic $\frac{1}{2}(1+e^{-2g^2 t^2})$")
    ax_A.plot(times, A["p"], "C0--", lw=1.2, label=rf"numeric ($n_{{\max}}={n_max_A}$)")
    ax_A.set_title(r"(A) §2.1 Hamiltonian, $\Delta=0$" + "\n(analytic anchor)")
    ax_A.set_xlabel(r"$t\,\omega_{\mathrm{ref}}$")
    ax_A.set_ylabel(r"$p(t)$")
    ax_A.set_ylim(0.45, 1.02)
    ax_A.legend(loc="upper right", frameon=False, fontsize=9)

    # (B) state curves
    ax_B.plot(times, B12["p"], "C3-", lw=1.2, label=r"$n_{\max}=12$")
    ax_B.plot(times, B18["p"], "C1:", lw=1.8, label=r"$n_{\max}=18$")
    ax_B.set_title(rf"(B) §2.1 Hamiltonian, $\Delta={Delta_B}$" + "\n(convergence)")
    ax_B.set_xlabel(r"$t\,\omega_{\mathrm{ref}}$")
    ax_B.set_ylabel(r"$p(t)$")
    ax_B.legend(loc="upper right", frameon=False, fontsize=9)

    # (C) state curves
    ax_C.plot(times, p_analytic_C, "k-", lw=1.8, label=r"analytic $\cos^2(g t)$")
    ax_C.plot(times, C["p"], "C2--", lw=1.2, label=rf"JC ($n_{{\max}}={n_max_C}$)")
    ax_C.set_title(r"(C) JC sanity check, $\omega_0=\omega$, RWA")
    ax_C.set_xlabel(r"$t\,\omega_{\mathrm{ref}}$")
    ax_C.set_ylabel(r"$p(t)$")
    ax_C.legend(loc="upper right", frameon=False, fontsize=9)

    # (A) error
    ax_eA.semilogy(times, np.abs(A["p"] - p_analytic_A) + 1e-18, "C0-",
                   label=r"$|p - p_{\mathrm{analytic}}|$ (Gate 1)")
    ax_eA.axhline(target, color="k", ls=":", alpha=0.6, label=r"$10^{-4}$ target")
    ax_eA.set_xlabel(r"$t\,\omega_{\mathrm{ref}}$")
    ax_eA.set_ylabel("error")
    ax_eA.legend(loc="lower right", frameon=False, fontsize=9)

    # (B) error
    ax_eB.semilogy(times, np.abs(B12["p"] - B18["p"]) + 1e-18, "C3-",
                   label=r"$|p_{12}-p_{18}|$ (Gate 2)")
    ax_eB.axhline(target, color="k", ls=":", alpha=0.6, label=r"$10^{-4}$ target")
    ax_eB.set_xlabel(r"$t\,\omega_{\mathrm{ref}}$")
    ax_eB.set_ylabel("error")
    ax_eB.legend(loc="best", frameon=False, fontsize=9)

    # (C) error
    ax_eC.semilogy(times, np.abs(C["p"] - p_analytic_C) + 1e-18, "C2-",
                   label=r"$|p - \cos^2(g t)|$")
    ax_eC.axhline(target, color="k", ls=":", alpha=0.6, label=r"$10^{-4}$ target")
    ax_eC.set_xlabel(r"$t\,\omega_{\mathrm{ref}}$")
    ax_eC.set_ylabel("error")
    ax_eC.legend(loc="best", frameon=False, fontsize=9)

    fig.suptitle(
        "Stage 1 — single-mode propagator validation "
        "(unbiased Rabi anchor + Cut A inner-point convergence + JC sanity check)",
        fontsize=10,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig_path = FIGURES / "stage1_jc_validation.pdf"
    fig.savefig(fig_path)
    print(f"Figure: {fig_path.relative_to(REPO)}")

    metrics = {
        "gates": {
            "gate1_analytic_anchor_Delta0_nmax60": {
                "err": err_A, "target": target, "pass": gate1,
            },
            "gate2_convergence_Delta0p05_nmax12_vs_18": {
                "err": err_B, "target": target, "pass": gate2,
            },
            "jc_sanity_check": {
                "err": err_C, "target": target, "pass": gate_C,
            },
        },
        "norm_drift": {
            "voyage_Delta0_nmax60": norm_drift_A,
            "voyage_Delta0p05_nmax12": norm_drift_B12,
            "voyage_Delta0p05_nmax18": norm_drift_B18,
            "jc_nmax18": norm_drift_C,
        },
        "parameters": {
            "g": g,
            "t_max": t_max,
            "n_times": n_times,
            "Delta_anchor": 0.0,
            "n_max_anchor": n_max_A,
            "Delta_convergence": Delta_B,
            "n_max_convergence": [12, 18],
            "n_max_jc": n_max_C,
        },
    }
    (HERE / "metrics.json").write_text(json.dumps(metrics, indent=2))
    return metrics


if __name__ == "__main__":
    main()
