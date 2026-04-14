# Stage 1 notes — Single-mode propagator

**Endorsement Marker:** T(h)reehouse +EC voyage, Coastline layer. No external endorsement implied.

**Licence:** CC BY-SA 4.0 for these notes (run script under MIT; see repository `LICENCE`).

**Stage:** 1 — Single-mode propagator validation.
**Run date:** 2026-04-14.
**Run script:** `run.py` (reproduces metrics below; writes `metrics.json`).
**Figure:** `../../figures/stage1_jc_validation.pdf`.

---

## 1. Parameters

Per VOYAGE_PLAN §2.4 (as amended 2026-04-14; see `../../PLAN_AMENDMENTS.md`).

- Single mode, $N = 1$.
- Coupling: $g / \omega_{\text{ref}} = 0.1$.
- Initial state: $|\uparrow\rangle \otimes |0\rangle$.
- Simulation window: $t \in [0, 50\, \omega_{\text{ref}}^{-1}]$, 500 uniform steps.
- Three runs (see §3 below):
  - (A) analytic anchor at $\Delta = 0$, $n_{\max} = 60$;
  - (B) convergence at the Cut A innermost point $\Delta = 0.15$, $n_{\max} \in \{12, 18\}$;
  - (C) JC code-machinery sanity check at $\omega_0 = \omega$ with RWA, $n_{\max} = 18$.

---

## 2. Go/no-go gate 3 — Gauge-convention statement

Required by VOYAGE_PLAN §2.1 (gauge-convention paragraph) and reconciliation §R3 item 8 / Standing item 5. Documenting here so that "no RWA" is unambiguous.

**Gauge adopted.** The §2.1 Hamiltonian is written in the **dipole-gauge** form in the rotating frame at the drive frequency $\omega_{\text{drive}}$, with the spin's bare-frequency term absorbed by the rotating-frame transformation (so no $\sigma_z$ term appears). Single-mode form:

$$H = \Delta\, a^\dagger a \;+\; g\, \sigma_x\, (a + a^\dagger).$$

**What "no RWA" means in this gauge.** The $\sigma_x$ coupling is retained *in full* as a static operator — not split into $\sigma_\pm$ components with a co-rotating subset kept. Expanding $\sigma_x = \sigma_+ + \sigma_-$ under this coupling produces all four combinations $\sigma_+ a$, $\sigma_+ a^\dagger$, $\sigma_- a$, $\sigma_- a^\dagger$ implicitly, with no selection. The counter-rotating terms $\sigma_+ a^\dagger$ and $\sigma_- a$ are present.

**Enforcement in code.** Hamiltonian assembly lives in [`../../src/hamiltonian.py`](../../src/hamiltonian.py), function `single_mode_hamiltonian(Delta, g, n_max)`:

```python
H_mode = Delta * kron(id_spin, num)
H_coup = g     * kron(sigma_x, x_m)   # x_m = a + a_dagger
return (H_mode + H_coup)
```

The `sigma_x` factor is used as a full $2 \times 2$ matrix, not decomposed. This guarantees the gauge is uniformly dipole-gauge, no-RWA, across all downstream stages that call this builder.

**Cross-reference.** Stokes & Nazir (2019), "Gauge Ambiguities in Ultrastrong Coupling QED" (Verifier citation A6 in `../perplexity_return.md`), demonstrates that other choices of gauge rearrange the appearance of counter-rotating terms. This voyage fixes dipole gauge; future voyages that change gauge must document the change explicitly.

---

## 3. Analytic-validation targets

### (A) Voyage §2.1 Hamiltonian at $\Delta = 0$

Factorises in the $\sigma_x$ eigenbasis. Each eigensector evolves as a conditional displacement of the mode vacuum, $|\alpha_\pm(t)\rangle$ with $\alpha_\pm(t) = \mp i g t$. Interference of the two sectors at the spin-up projector gives the closed form

$$p(t) = \tfrac{1}{2}\bigl(1 + e^{-2 g^2 t^2}\bigr),$$

a Gaussian monotonic decay from $1$ to $1/2$. Run at $n_{\max} = 60$ (dim $= 122$) specifically so the mode amplitude $|\alpha(t_{\max})| = g\, t_{\max} = 5$ is comfortably representable; this is a *code-anchor* run, not a sweep point.

### (B) Convergence at $\Delta = 0.15$

At $\Delta \neq 0$ each $\sigma_x$-sector is a harmonic oscillator with a constant linear force: $H_\pm = \Delta\, a^\dagger a \pm g (a + a^\dagger)$. Integrating $\dot a = -i \Delta\, a \mp i g$ from $a(0) = 0$ gives $\alpha_\pm(t) = \mp (g/\Delta)(1 - e^{-i \Delta t})$, so $\langle n \rangle_{\max} = 4 g^2 / \Delta^2$. At $\Delta = 0.15$ this gives $\langle n \rangle_{\max} \approx 1.78$ — comfortably inside $n_{\max} = 12$ and $n_{\max} = 18$. No closed-form target; Gate 2 is agreement between the two cutoffs.

### (C) Jaynes–Cummings code-machinery sanity check

Separate Hamiltonian, not the voyage's target:

$$H_{\text{JC}} = \tfrac{\omega_0}{2} \sigma_z \;+\; \omega\, a^\dagger a \;+\; g (\sigma_+ a + \sigma_- a^\dagger)$$

(RWA applied; no counter-rotating terms). At $\omega_0 = \omega$ and initial state $|\uparrow\rangle|0\rangle$, the spin evolves in the closed $\{|\uparrow, 0\rangle, |\downarrow, 1\rangle\}$ subspace and $p(t) = \cos^2(g t)$ exactly. This run exercises the same propagation pipeline (Hamiltonian build, dense eigendecomposition, spin-up projection) against a well-known benchmark; it is an independent-anchor test, not a voyage physics test.

**Relation to the plan's "$2g$ Rabi" phrasing.** The original VOYAGE_PLAN Stage 1 language referenced "vacuum Rabi oscillations at frequency $2g$" in the §2.1 Hamiltonian at $\Delta = 0$. Those oscillations live in $H_{\text{JC}}$ (through the dressed-state doublet at resonance), not in the unbiased Rabi Hamiltonian of §2.1. The plan's phrasing was superseded on 2026-04-14 (see `../../PLAN_AMENDMENTS.md`); the JC sanity check (C) gives the "$2g$ Rabi" statement a literal home without conflating it with the voyage's target physics.

---

## 4. Results

Numbers from the run executed 2026-04-14; full record in `metrics.json`.

| Gate | Test | Result | Target | Verdict |
|---|---|---:|---:|:---:|
| 1 | max $|p_{\text{num}} - p_{\text{analytic}}|$ at $\Delta = 0$, $n_{\max} = 60$ | $4.23 \times 10^{-9}$ | $\leq 10^{-4}$ | **PASS** |
| 2 | max $|p_{n_{\max}=12} - p_{n_{\max}=18}|$ at $\Delta = 0.15$ | $1.36 \times 10^{-6}$ | $\leq 10^{-4}$ | **PASS** |
| — | max $|p_{\text{JC}} - \cos^2(g t)|$, $n_{\max} = 18$ (anchor C) | $2.19 \times 10^{-15}$ | $\leq 10^{-4}$ | **PASS** |
| 3 | Gauge-convention statement present in this notes.md | §2 above | — | **PASS** |

Norm drift (maximum of $|\|\psi(t)\|^2 - 1|$ across the simulation window):

| Run | norm drift |
|---|---:|
| (A) Voyage, $\Delta = 0$, $n_{\max} = 60$ | $1.44 \times 10^{-15}$ |
| (B) Voyage, $\Delta = 0.15$, $n_{\max} = 12$ | $8.88 \times 10^{-16}$ |
| (B) Voyage, $\Delta = 0.15$, $n_{\max} = 18$ | $9.99 \times 10^{-16}$ |
| (C) JC, $n_{\max} = 18$ | $8.88 \times 10^{-16}$ |

All at machine precision; the dense-`eigh` propagator introduces no measurable unitarity drift on this problem size.

---

## 5. Interpretation

- The §2.1 propagator, Hamiltonian builder, and spin-up projector are correct at machine precision (anchor C) and at four-to-nine decimal places against analytic closed forms (anchors A and B's convergence test).
- Gate 1 margin (five orders of magnitude below target at $\Delta = 0$, $n_{\max} = 60$) is governed by the Fock-truncation residual of the coherent state at $t_{\max}$; the anchor run is numerically unambiguous.
- Gate 2 margin (two orders of magnitude below target at $\Delta = 0.15$, $n_{\max} = 12$ vs $18$) confirms the §2.5 convergence-table reading for the Cut A innermost point: homogeneous $n_{\max} = 12$ default with $n_{\max} = 18$ convergence check is sufficient across the full detuning set $\{\pm 0.15, \pm 0.3, \pm 0.5\}$.
- The JC anchor passing at $\sim 10^{-15}$ is the cleanest independent evidence that the propagation pipeline is not introducing silent errors: the JC doublet analytic and the numeric agree at machine precision.

## 6. Standing items forwarded to Stage 2

1. **Initial-state invariance under stage hand-off.** Stage 2 must use the same $|\uparrow\rangle \otimes |0\rangle$ initial state as Stage 1 for direct comparability of $p(t)$ traces across stages (§10 Standing Question 7). No state-switching between stages without a documented reason.
2. **Aggregate complexity invariant.** When Stage 2 adds the reduced-state diagonalisation, report the aggregate $\mathcal{C}(t) = \sum_k \log n_{\text{eff}}^{(k)}(t)$ as the primary invariant; per-mode $n_{\text{eff}}^{(k)}$ only as a decomposition (§10 Standing Question 2).
3. **Convergence propagation.** The convergence table in VOYAGE_PLAN §2.5 is validated at the $p(t)$ observable. Stage 2 must re-verify convergence at the $n_{\text{eff}}^{(k)}(t)$ observable because reduced-state entropy has its own truncation artefact (§10 Standing Question 1); in general $p(t)$-converged is not $n_{\text{eff}}$-converged.

---

## 7. Go/no-go

All three gates pass. Stage 2 cleared to begin.
