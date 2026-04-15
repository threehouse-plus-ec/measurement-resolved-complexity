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


def initial_state_down_vacuum(n_max: int) -> np.ndarray:
    """``|down> (x) |0>``. Used only as the antipodal partner for Stage 3
    BLP trace-distance cross-check (reconciliation §R2 / Standing item 11);
    the voyage's observable runs use ``initial_state_up_vacuum`` throughout.
    """
    mode_dim = n_max + 1
    psi = np.zeros(2 * mode_dim, dtype=complex)
    psi[mode_dim] = 1.0
    return psi


def two_mode_hamiltonian(
    Delta_1: float, Delta_2: float, g: float, n_max: int
) -> sp.csr_matrix:
    """Voyage §2.1 Hamiltonian at N=2, equal coupling on both modes.

    H = Delta_1 a_1^dag a_1 + Delta_2 a_2^dag a_2
        + g sigma_x (a_1 + a_1^dag) + g sigma_x (a_2 + a_2^dag)

    Basis: kron(spin, mode_1, mode_2). State index (s, n1, n2) ->
    s * (n_max+1)^2 + n1 * (n_max+1) + n2.
    """
    mode_dim = n_max + 1
    a = annihilation(n_max)
    a_dag = a.conj().T.tocsr()
    num = (a_dag @ a).tocsr()
    x_m = (a + a_dag).tocsr()
    id_m = sp.eye(mode_dim, format="csr", dtype=complex)
    id_spin = sp.eye(2, format="csr", dtype=complex)
    sigma_x = sp.csr_matrix(np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex))

    # Free-mode terms (act on spin x mode_1 x mode_2).
    H_mode1 = Delta_1 * sp.kron(id_spin, sp.kron(num, id_m, format="csr"),
                                format="csr")
    H_mode2 = Delta_2 * sp.kron(id_spin, sp.kron(id_m, num, format="csr"),
                                format="csr")

    # Coupling terms.
    H_coup1 = g * sp.kron(sigma_x, sp.kron(x_m, id_m, format="csr"),
                          format="csr")
    H_coup2 = g * sp.kron(sigma_x, sp.kron(id_m, x_m, format="csr"),
                          format="csr")

    return (H_mode1 + H_mode2 + H_coup1 + H_coup2).tocsr()


def initial_state_up_vacuum_n2(n_max: int) -> np.ndarray:
    """``|up> (x) |0>_1 (x) |0>_2`` at N=2, in the kron(spin, m1, m2) basis."""
    mode_dim = n_max + 1
    dim = 2 * mode_dim * mode_dim
    psi = np.zeros(dim, dtype=complex)
    psi[0] = 1.0
    return psi


def three_mode_hamiltonian(
    Delta_1: float, Delta_2: float, Delta_3: float, g: float, n_max: int
) -> sp.csr_matrix:
    """Voyage §2.1 Hamiltonian at N=3, equal coupling on all three modes.

    Basis: kron(spin, m1, m2, m3). State index
    (s, n1, n2, n3) -> s * md^3 + n1 * md^2 + n2 * md + n3, md = n_max + 1.
    """
    md = n_max + 1
    a = annihilation(n_max)
    a_dag = a.conj().T.tocsr()
    num = (a_dag @ a).tocsr()
    x_m = (a + a_dag).tocsr()
    id_m = sp.eye(md, format="csr", dtype=complex)
    id_spin = sp.eye(2, format="csr", dtype=complex)
    sigma_x = sp.csr_matrix(np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex))

    def _kk(A, B, C, D):
        return sp.kron(
            A, sp.kron(B, sp.kron(C, D, format="csr"), format="csr"),
            format="csr",
        )

    H_mode1 = Delta_1 * _kk(id_spin, num, id_m, id_m)
    H_mode2 = Delta_2 * _kk(id_spin, id_m, num, id_m)
    H_mode3 = Delta_3 * _kk(id_spin, id_m, id_m, num)

    H_c1 = g * _kk(sigma_x, x_m, id_m, id_m)
    H_c2 = g * _kk(sigma_x, id_m, x_m, id_m)
    H_c3 = g * _kk(sigma_x, id_m, id_m, x_m)

    return (H_mode1 + H_mode2 + H_mode3 + H_c1 + H_c2 + H_c3).tocsr()


def initial_state_up_vacuum_n3(n_max: int) -> np.ndarray:
    """``|up> (x) |0>^⊗3`` at N=3, kron(spin, m1, m2, m3)."""
    md = n_max + 1
    psi = np.zeros(2 * md * md * md, dtype=complex)
    psi[0] = 1.0
    return psi
