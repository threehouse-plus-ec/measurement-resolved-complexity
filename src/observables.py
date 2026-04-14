"""Observables on propagated states.

Stage 1: spin-up population, norm.
Stage 2: reduced-state diagonalisation, von Neumann entropy, n_eff.
Later stages: ensemble variance and QPN comparison (Stage 3).

Conventions match ``src/hamiltonian.py``: state vectors live in the
``kron(spin, mode)`` basis, with the spin-up sector indexed first.
"""

from __future__ import annotations

import numpy as np


# ---------- Stage 1 ----------

def spin_up_population(states: np.ndarray, n_max: int) -> np.ndarray:
    """Return p(t) = <up|rho_spin(t)|up> summed over mode indices.

    ``states`` has shape ``(n_times, 2 * (n_max + 1))`` in ``kron(spin, mode)``
    ordering; the spin-up sector is the first ``n_max + 1`` columns.
    """
    mode_dim = n_max + 1
    up_amplitudes = states[:, :mode_dim]
    return np.sum(np.abs(up_amplitudes) ** 2, axis=1).real


def norm_squared(states: np.ndarray) -> np.ndarray:
    """Return ||psi(t)||^2 at each time step. Should be 1 for unitary evolution."""
    return np.sum(np.abs(states) ** 2, axis=1).real


# ---------- Stage 2 ----------

def _reshape_n1(state_vec: np.ndarray, n_max: int) -> np.ndarray:
    """Reshape a single-mode (N=1) state vector into an amplitude matrix M[s, n]."""
    mode_dim = n_max + 1
    return state_vec.reshape(2, mode_dim)


def reduced_spin_matrix_n1(state_vec: np.ndarray, n_max: int) -> np.ndarray:
    """Spin-reduced density matrix Tr_mode |psi><psi| for N=1. Shape (2, 2)."""
    M = _reshape_n1(state_vec, n_max)
    return M @ M.conj().T


def reduced_mode_matrix_n1(state_vec: np.ndarray, n_max: int) -> np.ndarray:
    """Mode-reduced density matrix Tr_spin |psi><psi| for N=1.

    Shape is (n_max+1, n_max+1). Rank is at most 2 (Schmidt bound from the
    2-dim spin partner), so n_eff from either reduced matrix agrees on
    non-zero eigenvalues.
    """
    M = _reshape_n1(state_vec, n_max)
    return M.conj().T @ M


def schmidt_eigenvalues_n1(state_vec: np.ndarray, n_max: int) -> np.ndarray:
    """Non-zero eigenvalues of the reduced density matrix at N=1.

    Returns a length-2 array in descending order, computed from the 2x2
    spin-reduced matrix for speed. These are the squared Schmidt
    coefficients and agree with the non-zero eigenvalues of the mode-
    reduced matrix.
    """
    rho_s = reduced_spin_matrix_n1(state_vec, n_max)
    w = np.linalg.eigvalsh(rho_s)
    return np.sort(w)[::-1]


def n_eff_from_eigenvalues(lambdas: np.ndarray, floor: float = 1e-16) -> float:
    """n_eff = exp(S_vN) = exp(-sum lambda log lambda).

    Uses 0 log 0 := 0 by masking values at or below ``floor``. Numerically-
    negative eigenvalues from round-off are clipped to zero.
    """
    w = np.clip(np.asarray(lambdas, dtype=float), 0.0, 1.0)
    mask = w > floor
    entropy = float(-np.sum(w[mask] * np.log(w[mask])))
    return float(np.exp(entropy))


def n_eff_series_n1(states: np.ndarray, n_max: int) -> np.ndarray:
    """Per-time n_eff^{(1)}(t) for an N=1 run. Shape (n_times,)."""
    n_times = states.shape[0]
    out = np.empty(n_times, dtype=float)
    for i in range(n_times):
        lambdas = schmidt_eigenvalues_n1(states[i], n_max)
        out[i] = n_eff_from_eigenvalues(lambdas)
    return out


def mode_spectrum_at_time(state_vec: np.ndarray, n_max: int) -> np.ndarray:
    """Full eigenvalue spectrum of the mode-reduced density matrix at one time.

    Returned in descending order. For N=1 at most two entries are non-zero
    up to round-off; the remainder sit at the numerical floor.
    """
    rho_m = reduced_mode_matrix_n1(state_vec, n_max)
    w = np.linalg.eigvalsh(rho_m)
    return np.sort(w)[::-1]


def n_eff_analytic_Delta0(times: np.ndarray, g: float) -> np.ndarray:
    """Closed-form n_eff^{(1)}(t) for the voyage §2.1 Hamiltonian at Delta=0.

    At Delta=0, Schmidt decomposition of |Psi(t)> gives eigenvalues
    lambda_{1,2}(t) = (1 +/- exp(-2 g^2 t^2)) / 2. Returns exp(S_vN) of
    that 2-eigenvalue spectrum, element-wise in ``times``.
    """
    overlap = np.exp(-2.0 * g**2 * times**2)
    lam1 = 0.5 * (1.0 + overlap)
    lam2 = 0.5 * (1.0 - overlap)

    def safe_xlogx(x: np.ndarray) -> np.ndarray:
        out = np.zeros_like(x)
        mask = x > 0
        out[mask] = x[mask] * np.log(x[mask])
        return out

    S = -(safe_xlogx(lam1) + safe_xlogx(lam2))
    return np.exp(S)
