"""Exact propagation via Hermitian eigendecomposition.

For the voyage's N=1 and N=2 problem sizes (dim <= ~340), full dense
``eigh`` is machine-precision accurate and fast enough. N=3 at the
full 4394-dim basis may benefit from Krylov-based ``expm_multiply``;
revisit at Stage 7.
"""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp


def propagate_eigendecomp(H, psi0: np.ndarray, times: np.ndarray) -> np.ndarray:
    """Propagate ``psi0`` under Hermitian ``H`` to each time in ``times``.

    Returns array of shape ``(len(times), dim)`` with the state vector at
    each requested time.
    """
    H_dense = H.toarray() if sp.issparse(H) else np.asarray(H)
    eigvals, eigvecs = np.linalg.eigh(H_dense)
    coeffs0 = eigvecs.conj().T @ psi0
    phases = np.exp(-1j * np.outer(times, eigvals))
    coeffs_t = phases * coeffs0[np.newaxis, :]
    return coeffs_t @ eigvecs.T
