"""Hamiltonian builders for the measurement-resolved-complexity voyage.

Conventions (see VOYAGE_PLAN.md §2.1):
- Basis ordering: ``kron(spin, mode)``. State vectors are indexed as
  ``[spin=0, n=0], [spin=0, n=1], ..., [spin=1, n=0], ...``.
- Spin convention: ``|up>`` is the first basis state, represented as [1, 0].
- Gauge: dipole-gauge form in the rotating frame at the drive frequency;
  counter-rotating terms retained explicitly via the static ``sigma_x``
  coupling (see stage-1 notes for the full gauge statement).
"""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp


def annihilation(n_max: int) -> sp.csr_matrix:
    """Truncated single-mode annihilation operator.

    Hilbert-space dimension is ``n_max + 1`` (Fock states ``n = 0..n_max``).
    """
    dim = n_max + 1
    diag = np.sqrt(np.arange(1, dim))
    return sp.diags(diag, offsets=1, shape=(dim, dim), format="csr", dtype=complex)


def single_mode_hamiltonian(Delta: float, g: float, n_max: int) -> sp.csr_matrix:
    """Voyage §2.1 Hamiltonian for a single mode.

    H = Delta * a^dag a + g * sigma_x (a + a^dag)

    Unbiased Rabi model: no sigma_z term (absorbed by the spin rotating
    frame at the drive frequency). Counter-rotating terms are present
    implicitly in the static sigma_x factor.
    """
    mode_dim = n_max + 1
    a = annihilation(n_max)
    a_dag = a.conj().T.tocsr()
    num = (a_dag @ a).tocsr()
    x_m = (a + a_dag).tocsr()

    id_spin = sp.eye(2, format="csr", dtype=complex)
    sigma_x = sp.csr_matrix(np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex))

    H_mode = Delta * sp.kron(id_spin, num, format="csr")
    H_coup = g * sp.kron(sigma_x, x_m, format="csr")
    return (H_mode + H_coup).tocsr()


def jc_hamiltonian(omega_0: float, omega: float, g: float, n_max: int) -> sp.csr_matrix:
    """Standard Jaynes-Cummings Hamiltonian (lab-frame, RWA applied).

    H_JC = (omega_0 / 2) sigma_z + omega * a^dag a + g (sigma_+ a + sigma_- a^dag)

    Used only as a code-machinery sanity check against the cos^2(g t)
    analytic result at resonance (omega_0 = omega). Not the voyage's
    target Hamiltonian.
    """
    mode_dim = n_max + 1
    a = annihilation(n_max)
    a_dag = a.conj().T.tocsr()
    num = (a_dag @ a).tocsr()

    id_spin = sp.eye(2, format="csr", dtype=complex)
    sigma_z = sp.csr_matrix(np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex))
    sigma_plus = sp.csr_matrix(np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex))
    sigma_minus = sp.csr_matrix(np.array([[0.0, 0.0], [1.0, 0.0]], dtype=complex))

    H_spin = (omega_0 / 2.0) * sp.kron(sigma_z, sp.eye(mode_dim, format="csr"), format="csr")
    H_mode = omega * sp.kron(id_spin, num, format="csr")
    H_coup = g * (sp.kron(sigma_plus, a, format="csr") + sp.kron(sigma_minus, a_dag, format="csr"))
    return (H_spin + H_mode + H_coup).tocsr()


def initial_state_up_vacuum(n_max: int) -> np.ndarray:
    """Voyage initial state ``|up> (x) |0>`` in the kron(spin, mode) basis."""
    psi = np.zeros(2 * (n_max + 1), dtype=complex)
    psi[0] = 1.0
    return psi
