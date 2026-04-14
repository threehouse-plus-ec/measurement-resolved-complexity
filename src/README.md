# src/

**Endorsement Marker:** T(h)reehouse +EC voyage, Infrastructure layer. No external endorsement implied.

**Licence:** MIT (see repository `LICENCE`).

Propagation and analysis code.

Planned modules (to be filled in as stages proceed):

- `hamiltonian.py` — build $H = \sum_k \Delta_k a_k^\dagger a_k + \sum_k g_k \sigma_x (a_k + a_k^\dagger)$ in truncated Fock × spin basis, no RWA.
- `propagate.py` — exact sparse propagation via scipy or qutip.
- `observables.py` — $p(t)$, reduced density matrix, single-mode von Neumann entropy, $n_{\text{eff}}^{(k)}(t)$, aggregate $\mathcal{C}(t)$.
- `ensemble.py` — ensemble runs with Gaussian $\Delta$-noise, variance computation, $T_{\text{det}}(M)$ extraction.
- `plots.py` — per-stage figure generation.

Style: functions over classes where reasonable; explicit parameter passing; no hidden state.
