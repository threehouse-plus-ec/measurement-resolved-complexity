"""Observables on propagated states.

Stage 1 uses only the spin-up population and the norm. Later stages add
reduced-state diagonalisation and n_eff (Stage 2), ensemble variance
and QPN comparison (Stage 3).
"""

from __future__ import annotations

import numpy as np


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
