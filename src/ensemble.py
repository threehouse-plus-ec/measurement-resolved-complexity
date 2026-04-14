"""Ensemble-layer utilities for Stage 3 onwards.

Builds a detuning-noisy ensemble of single-mode trajectories, computes
ensemble-averaged observables, the quantum-projection-noise floor, and
the detectability horizon T_det(M).

Conventions:
- Noise model follows VOYAGE_PLAN §2.4 (as amended 2026-04-14): Gaussian
  noise on Delta_k with 1% RMS of omega_ref. This is a deliberate
  stress-test level, not a realistic operating point (reconciliation
  §R3 item 9 / Standing item 6).
- sigma_Delta is in the same units as Delta itself, i.e. units of
  omega_ref. Default sigma_Delta = 0.01.
"""

from __future__ import annotations

from typing import Optional

import numpy as np

from hamiltonian import initial_state_up_vacuum, single_mode_hamiltonian
from observables import n_eff_series_n1, spin_up_population
from propagate import propagate_eigendecomp


def sample_detunings(
    Delta_nominal: float,
    sigma_Delta: float,
    R: int,
    rng: Optional[np.random.Generator] = None,
) -> np.ndarray:
    """Draw R detuning values from N(Delta_nominal, sigma_Delta^2)."""
    if rng is None:
        rng = np.random.default_rng()
    return rng.normal(loc=Delta_nominal, scale=sigma_Delta, size=R)


def run_ensemble_two_mode(
    Delta1_values: np.ndarray,
    Delta2_values: np.ndarray,
    g: float,
    n_max: int,
    times: np.ndarray,
) -> dict:
    """Propagate an ensemble of N=2 trajectories, one per (Delta_1, Delta_2) pair.

    Returns a dict with shape-(R, n_times) arrays for ``p``, ``n_eff_1``,
    ``n_eff_2``, ``C`` (aggregate = log n_eff_1 + log n_eff_2), ``norm``.
    """
    from hamiltonian import initial_state_up_vacuum_n2, two_mode_hamiltonian
    from observables import (
        aggregate_complexity_series,
        n_eff_per_mode_series_n2,
        spin_up_population_n2,
    )

    assert len(Delta1_values) == len(Delta2_values)
    R = len(Delta1_values)
    n_times = len(times)
    p_traj = np.empty((R, n_times))
    n_eff_1_traj = np.empty((R, n_times))
    n_eff_2_traj = np.empty((R, n_times))
    C_traj = np.empty((R, n_times))
    norm_traj = np.empty((R, n_times))
    psi0 = initial_state_up_vacuum_n2(n_max)

    for i in range(R):
        H = two_mode_hamiltonian(
            Delta_1=float(Delta1_values[i]),
            Delta_2=float(Delta2_values[i]),
            g=g, n_max=n_max,
        )
        states = propagate_eigendecomp(H, psi0, times)
        p_traj[i] = spin_up_population_n2(states, n_max)
        n_eff_per_mode = n_eff_per_mode_series_n2(states, n_max)
        n_eff_1_traj[i] = n_eff_per_mode[:, 0]
        n_eff_2_traj[i] = n_eff_per_mode[:, 1]
        C_traj[i] = aggregate_complexity_series(n_eff_per_mode)
        norm_traj[i] = np.sum(np.abs(states) ** 2, axis=1).real

    return {
        "p": p_traj,
        "n_eff_1": n_eff_1_traj,
        "n_eff_2": n_eff_2_traj,
        "C": C_traj,
        "norm": norm_traj,
    }


def finite_difference_dpdDelta_n2(
    Delta_1: float, Delta_2: float, g: float, n_max: int,
    times: np.ndarray, eps: float = 1e-3,
) -> tuple[np.ndarray, np.ndarray]:
    """Central FD derivatives ``dp/dDelta_1`` and ``dp/dDelta_2`` at N=2."""
    from hamiltonian import initial_state_up_vacuum_n2, two_mode_hamiltonian
    from observables import spin_up_population_n2

    psi0 = initial_state_up_vacuum_n2(n_max)

    def _p(D1, D2):
        H = two_mode_hamiltonian(Delta_1=D1, Delta_2=D2, g=g, n_max=n_max)
        states = propagate_eigendecomp(H, psi0, times)
        return spin_up_population_n2(states, n_max)

    p_1p = _p(Delta_1 + eps, Delta_2)
    p_1m = _p(Delta_1 - eps, Delta_2)
    p_2p = _p(Delta_1, Delta_2 + eps)
    p_2m = _p(Delta_1, Delta_2 - eps)
    dpdD1 = (p_1p - p_1m) / (2.0 * eps)
    dpdD2 = (p_2p - p_2m) / (2.0 * eps)
    return dpdD1, dpdD2


def run_ensemble_single_mode(
    Delta_values: np.ndarray,
    g: float,
    n_max: int,
    times: np.ndarray,
) -> dict:
    """Propagate each member of a detuning ensemble and collect observables.

    Returns a dict with shape-``(R, n_times)`` arrays for ``p``, ``n_eff``,
    ``norm``. Each row is one realisation.
    """
    R = len(Delta_values)
    n_times = len(times)
    p_traj = np.empty((R, n_times))
    n_eff_traj = np.empty((R, n_times))
    norm_traj = np.empty((R, n_times))
    psi0 = initial_state_up_vacuum(n_max)

    for i, Delta in enumerate(Delta_values):
        H = single_mode_hamiltonian(Delta=float(Delta), g=g, n_max=n_max)
        states = propagate_eigendecomp(H, psi0, times)
        p_traj[i] = spin_up_population(states, n_max)
        n_eff_traj[i] = n_eff_series_n1(states, n_max)
        norm_traj[i] = np.sum(np.abs(states) ** 2, axis=1).real

    return {"p": p_traj, "n_eff": n_eff_traj, "norm": norm_traj}


def ensemble_variance(trajectories: np.ndarray) -> np.ndarray:
    """Sample variance across R realisations, returned as a length-n_times array."""
    return np.var(trajectories, axis=0, ddof=1)


def ensemble_mean(trajectories: np.ndarray) -> np.ndarray:
    return np.mean(trajectories, axis=0)


def qpn_floor(p_mean: np.ndarray, M: int) -> np.ndarray:
    """Quantum-projection-noise floor sigma^2_QPN(t; M) = p(t)(1 - p(t))/M."""
    return p_mean * (1.0 - p_mean) / M


def t_det(
    sigma2_intrinsic: np.ndarray,
    sigma2_qpn: np.ndarray,
    times: np.ndarray,
) -> float:
    """T_det(M) = last time at which sigma^2_intrinsic > sigma^2_QPN(M).

    Returns 0.0 if the intrinsic variance never exceeds the floor; returns
    ``times[-1]`` if it still exceeds at the window end (implying the true
    horizon lies beyond the simulation window).
    """
    above = sigma2_intrinsic > sigma2_qpn
    if not np.any(above):
        return 0.0
    last = int(np.max(np.where(above)[0]))
    return float(times[last])


def t_rise(
    sigma2_intrinsic: np.ndarray,
    sigma2_qpn: np.ndarray,
    times: np.ndarray,
) -> float:
    """First time at which sigma^2_intrinsic rises above sigma^2_QPN(M).

    Complements ``t_det``: together, ``(t_rise, t_det)`` bound the window
    during which the ongoing dynamics is resolvable against the projection-
    noise floor. In bounded recurrent regimes, ``t_det`` can saturate at
    the simulation window; ``t_rise`` is the more informative quantity in
    that case. Returns ``0.0`` if sigma^2 never exceeds QPN.

    The ``t=0`` entry is skipped: both variances are structurally zero
    there, but eigendecomposition round-off gives sigma^2 an O(1e-30)
    floor that spuriously exceeds sigma^2_QPN(0) = 0 exactly.
    """
    above = sigma2_intrinsic > sigma2_qpn
    above[0] = False
    idxs = np.where(above)[0]
    if len(idxs) == 0:
        return 0.0
    return float(times[int(idxs[0])])


def resolved_fraction(
    sigma2_intrinsic: np.ndarray,
    sigma2_qpn: np.ndarray,
) -> float:
    """Fraction of timesteps at which sigma^2_intrinsic > sigma^2_QPN(M)."""
    return float(np.mean(sigma2_intrinsic > sigma2_qpn))


def resolved_per_cycle(
    sigma2_intrinsic: np.ndarray,
    sigma2_qpn: np.ndarray,
    times: np.ndarray,
    period: float,
) -> float:
    """Window-normalised alternative to ``resolved_fraction``.

    Reports ``resolved_fraction * (t_max / period)`` = mean number of
    resolved-cycle equivalents per characteristic period. Guardian middle
    path for Stage 6: log this alongside the bare ``resolved_fraction``
    so Stage 8 can choose between the two without re-running Cut B.

    Returns ``float('inf')`` if ``period`` is zero or negative.
    """
    if period <= 0:
        return float("inf")
    frac = resolved_fraction(sigma2_intrinsic, sigma2_qpn)
    t_span = float(times[-1] - times[0])
    return frac * t_span / period


def finite_difference_dpdDelta(
    Delta_nominal: float,
    g: float,
    n_max: int,
    times: np.ndarray,
    eps: float = 1e-3,
) -> np.ndarray:
    """Numerical partial derivative d p(t) / d Delta at Delta = Delta_nominal.

    Central finite difference with step ``eps``. Used for the small-noise-
    limit QFI reduction check: sigma^2_intrinsic(t) ~= (dp/dDelta)^2 sigma_Delta^2
    to leading order in sigma_Delta.
    """
    psi0 = initial_state_up_vacuum(n_max)

    H_plus = single_mode_hamiltonian(Delta=Delta_nominal + eps, g=g, n_max=n_max)
    H_minus = single_mode_hamiltonian(Delta=Delta_nominal - eps, g=g, n_max=n_max)

    states_plus = propagate_eigendecomp(H_plus, psi0, times)
    states_minus = propagate_eigendecomp(H_minus, psi0, times)

    p_plus = spin_up_population(states_plus, n_max)
    p_minus = spin_up_population(states_minus, n_max)
    return (p_plus - p_minus) / (2.0 * eps)


def reduced_spin_traces(
    states_a: np.ndarray, states_b: np.ndarray, n_max: int
) -> np.ndarray:
    """BLP trace distance D(t) = (1/2) Tr|rho_spin_a(t) - rho_spin_b(t)| between
    two reduced spin trajectories, N=1.

    Each input has shape (n_times, 2*(n_max+1)). Returns length-n_times array.
    """
    mode_dim = n_max + 1
    n_times = states_a.shape[0]
    D = np.empty(n_times)
    for i in range(n_times):
        Ma = states_a[i].reshape(2, mode_dim)
        Mb = states_b[i].reshape(2, mode_dim)
        rho_a = Ma @ Ma.conj().T
        rho_b = Mb @ Mb.conj().T
        diff = rho_a - rho_b
        # Trace distance = (1/2) * sum of singular values = (1/2) * sum |eigvals|
        # for Hermitian difference; eigvalsh gives real eigenvalues.
        w = np.linalg.eigvalsh(diff)
        D[i] = 0.5 * float(np.sum(np.abs(w)))
    return D


def blp_non_markovianity(D: np.ndarray, times: np.ndarray) -> float:
    """Integral of (dD/dt)_+ over the window. Approximates N_BLP for the
    fixed antipodal pair used to form D(t) (without the max over pairs)."""
    dDdt = np.gradient(D, times)
    pos = np.where(dDdt > 0, dDdt, 0.0)
    return float(np.trapezoid(pos, times))
