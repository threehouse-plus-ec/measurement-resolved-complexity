# Measurement-Resolved Complexity Voyage

**Endorsement Marker:** T(h)reehouse +EC voyage plan — internal numerical exploration. Local candidate framework under T(h)reehouse +EC stewardship. No external endorsement implied.

**Licence:** Coastline layer, CC BY-SA 4.0 (see repository `LICENCE`).

**Version:** v0.2 (2026-04-14). Supersedes v0.1 (archived at [`archive/VOYAGE_PLAN-v0.1.md`](archive/VOYAGE_PLAN-v0.1.md); deprecation note at [`archive/2026-04-14-VOYAGE_PLAN-v0.1-deprecated.md`](archive/2026-04-14-VOYAGE_PLAN-v0.1-deprecated.md)). Amendment-level audit trail: [`PLAN_AMENDMENTS.md`](PLAN_AMENDMENTS.md). Source legend used in-place below: **PA-01..04** refer to the four amendments v0.2 absorbs from v0.1; **C3.n**, **P#**, **HM** refer to pitfall, Verifier, and Harbourmaster-derived items from the literature reconciliation §R3.

**A bounded numerical exploration: spin coupled to few radial motional modes under detuning sweep.**

---

## Metadata

- **Working title:** Measurement-resolved complexity in a spin coupled to few radial motional modes.
- **Started:** 2026-04-14.
- **Stance:** Exploratory, self-contained, Harbourmaster discipline.
- **Status at v0.2 issue:** Stages 1–4 complete and committed; Stage 5 (Cut A) cleared to begin against this plan.
- **Not:** a replacement for parallel MCTDH work by a numerics collaborator; a validation of Ordinans; a publication-ready study.

---

## 1. Purpose

Test whether two time-resolved complexity measures exhibit correlated dynamics in a spin coupled to a small number of *radial* motional modes, across a detuning sweep at fixed intermediate coupling:

- **Intrinsic (theorist-visible):** $n_{\text{eff}}^{(k)}(t)$, the effective orbital count per mode, derived from single-mode reduced-density-matrix eigenvalues; aggregate $\mathcal{C}(t) = \sum_k \log n_{\text{eff}}^{(k)}(t)$.
- **Operational (experiment-visible):** $\sigma^2_{\text{intrinsic}}(t)$, the shot-to-shot spin-population variance under realistic parameter noise, compared against the quantum-projection-noise floor $\sigma^2_{\text{QPN}}(t; M) = p(t)[1-p(t)]/M$ via the resolvable-fraction scalar $f_{\text{resolved}}(M)$ — the duty-cycle of $\sigma^2_{\text{intrinsic}} > \sigma^2_{\text{QPN}}$ over the simulation window.

If these track each other, the Ordinans-plus-QPN proposal has empirical footing worth bringing to the MCTDH-numerics collaborator and the open-systems collaborator. If not, the framework's theoretical spine does not map cleanly onto the variance signal, and the framing needs revision before committing group resources. Both outcomes are useful.

---

## 2. Physical setup

### 2.1 Hamiltonian

Rotating frame, Lamb–Dicke approximation retained, **no RWA imposed** (full $\sigma_x$ coupling preserves counter-rotating terms, which matter at $g/\omega = 0.1$):

$$H = \sum_{k=1}^{N} \Delta_k \, a_k^\dagger a_k \;+\; \sum_{k=1}^{N} g_k \, \sigma_x (a_k + a_k^\dagger)$$

with $\Delta_k = \omega_k - \omega_{\text{drive}}$ the spin–mode detuning.

**Gauge convention.** The form above is the **dipole gauge** in the rotating frame at the drive frequency; the spin's bare-frequency term is absorbed by the rotating-frame transformation, and counter-rotating terms are retained explicitly through the static $\sigma_x$ factor. Stokes & Nazir (2019; Verifier P1/A6) establish that the appearance of counter-rotating terms is gauge-dependent in this class of Hamiltonians. Runs that call `single_mode_hamiltonian` in `src/hamiltonian.py` are uniformly dipole-gauge, no-RWA, with the $\sigma_x$ factor used as a full $2\times 2$ matrix (not decomposed into $\sigma_\pm$ with a co-rotating subset). Stage 1 [notes](stages/stage1_single_mode_propagator/notes.md) §2 documents this in detail and closes Standing item 5. *(Source: reconciliation §R3 item 8; Stage 1 Gate 3.)*

### 2.2 Reference units

$\omega_{\text{ref}}$ sets the frequency unit; all times in units of $\omega_{\text{ref}}^{-1}$. Dimensional mapping to ²⁵Mg⁺ radial-mode frequencies (MHz range) deferred to writeup.

### 2.3 Initial state

$|\Psi(0)\rangle = |\uparrow\rangle \otimes |0\rangle^{\otimes N}$ — spin excited, all modes in vacuum. Held fixed across all observable-computation stages (Standing item 7 / C3.7). The antipodal partner $|\downarrow\rangle|0\rangle$ appears only as the BLP trace-distance pair in Stage 3 and is a cross-check, not a voyage initial state.

### 2.4 Locked parameter choices

| Parameter | Value | Rationale |
|---|---|---|
| Coupling $g_k / \omega_{\text{ref}}$ | $0.1$ (all modes, fixed) | Intermediate regime, approaching ultrastrong boundary; counter-rotating terms non-negligible. |
| **Detuning set (Cut A)** | $\Delta / \omega_{\text{ref}} \in \{-0.5, -0.3, -0.15, +0.15, +0.3, +0.5\}$ | Six points, symmetric, three per sign, roughly log-spaced toward resonance. $\Delta = 0$ is **excluded**: the §2.1 Hamiltonian with $|\uparrow\rangle|0\rangle$ drives unbounded coherent-amplitude growth at exactly zero detuning (see §2.5), so no finite Fock budget saturates the numerical error there. Inner sampling at $|\Delta|/\omega_{\text{ref}} = 0.15$ is the closest approach at which a homogeneous $n_{\max} = 12$ default meets the Stage-1 error target (see §2.5 convergence table). H3 is accordingly a *limit* claim, fit across the three per-sign points and extrapolated toward zero, not a *point* claim at $\Delta = 0$ (see §5 and Standing Question 12). *(Source: PA-02; Stage 1 prep convergence scan; Guardian option III-b.)* |
| Mode type | Radial | Contribute more equally than axial (no COM hierarchy); detuning sweep samples symmetric coupling landscape. |
| Fock truncation $n_{\max}$ | $12$ per mode (default); $18$ for the Stage-1 convergence check | See §2.5 for the measured convergence data justifying this choice; no folklore estimate. *(Source: PA-02; Stage 1 prep.)* |
| Noise model | Gaussian noise on $\Delta_k$, $\sigma_\Delta / \omega_{\text{ref}} = 0.01$ | **Deliberate stress-test level**, not a realistic operating-point prediction. Verifier P4/D3 reports active-feedback trapped-ion platforms at $\sim 5 \times 10^{-6}$ short-term; clock-grade systems at $\sim 10^{-18}$. The 1% RMS value is chosen to force visible ensemble variance at modest $M$. Stage 3 writeup reframes accordingly. *(Source: reconciliation §R3 item 9 / Standing item 6.)* |
| Coupling noise | None (fixed $g_k$) | Simplifies noise structure; follow-up voyage can relax. |
| Ensemble size $R$ | 100 trajectories per parameter point | Balances statistical power vs. compute. Finite-ensemble statistical noise in $\sigma^2$ at this $R$ is $\sim 0.14\,\sigma^2$; convergence targets for observables derived from $\sigma^2$ are set below that floor. |
| Shot budgets $M$ | $\{100, 1000, 10\,000\}$ | Spans realistic experimental range. |
| Simulation window | $t \in [0, 50\,\omega_{\text{ref}}^{-1}]$, 500 uniform timesteps | Stage 3 finding: in the bounded recurrent regime, $\sigma^2_{\text{intrinsic}}$ does not monotonically decay within this window; extending $t_{\max}$ does not change the qualitative picture. This is why the plan reports $f_{\text{resolved}}$ rather than a monotone-decay horizon (see §3 and §5). |

### 2.5 Fock truncation justification

**Analytic bound.** At non-zero detuning with the voyage initial state $|\uparrow\rangle|0\rangle$, each $\sigma_x$-eigensector sees $H_\pm = \Delta\, a^\dagger a \pm g\,(a + a^\dagger)$ — a harmonic oscillator with a constant linear force. The Heisenberg equation $\dot a = -i\Delta a \mp i g$ with $a(0) = 0$ integrates to

$$\alpha_\pm(t) = \mp \frac{g}{\Delta}\bigl(1 - e^{-i\Delta t}\bigr), \qquad |\alpha_\pm(t)|^2 = \frac{4 g^2}{\Delta^2}\sin^2\!\tfrac{\Delta t}{2},$$

so the mode occupation in each branch is bounded by $\langle n \rangle_{\max} = 4 g^2 / \Delta^2$, reached at $\Delta t = \pi$. The factor of 4 is the interference between the drive and the free-oscillation phase; naive estimates that drop the interference underestimate the Fock requirement fourfold. At exactly $\Delta = 0$ the linear-force term is unopposed, $|\alpha(t)| = g t$, and $\langle n \rangle = (g t)^2$ is unbounded in $t$ — no finite Fock budget saturates. This is why $\Delta = 0$ is excluded from Cut A (§2.4). It is not a property of the model alone; a $\sigma_x$-eigenstate tensor a matched coherent state would give bounded dynamics. See Standing Question 12.

**Measured convergence data** (against a reference at $n_{\max} + 20$; simulation window $t \in [0, 50\,\omega_{\text{ref}}^{-1}]$; $g/\omega_{\text{ref}} = 0.1$; $p(t)$-observable error):

| $\|\Delta\|/\omega_{\text{ref}}$ | $\langle n\rangle_{\max}$ | $n_{\max}=12$ | $n_{\max}=18$ | $n_{\max}=30$ | Floor for $10^{-4}$ |
|---:|---:|---:|---:|---:|:---|
| 0.05 | 16.00 | $4.4\times 10^{-3}$ | $2.8\times 10^{-4}$ | $1.4\times 10^{-7}$ | $n_{\max} \geq 30$ |
| 0.07 | 8.16 | $4.3\times 10^{-3}$ | $1.6\times 10^{-4}$ | $4.7\times 10^{-10}$ | $n_{\max} \geq 30$ |
| 0.10 | 4.00 | $2.4\times 10^{-3}$ | $1.9\times 10^{-6}$ | $5.4\times 10^{-15}$ | $n_{\max} \geq 18$ |
| 0.12 | 2.78 | $1.2\times 10^{-4}$ | $9.5\times 10^{-9}$ | $1.6\times 10^{-15}$ | $n_{\max} \geq 18$ |
| **0.15** | **1.78** | $\mathbf{1.4\times 10^{-6}}$ | $8.0\times 10^{-12}$ | $2.7\times 10^{-15}$ | $\mathbf{n_{\max} = 12}$ |
| 0.20 | 1.00 | $8.9\times 10^{-9}$ | $2.6\times 10^{-15}$ | $2.2\times 10^{-15}$ | $n_{\max} = 12$ |
| 0.50 | 0.16 | $8.9\times 10^{-16}$ | $4.4\times 10^{-16}$ | $1.6\times 10^{-15}$ | $n_{\max} = 12$ |

The innermost Cut A point (bold row) is the closest approach at which the homogeneous $n_{\max} = 12$ default clears the $10^{-4}$ target with margin. All other Cut A points clear it further. The table is the voyage's Fock justification; it replaces folklore.

**Code-anchor validation** at $\Delta = 0$ uses $n_{\max} = 60$ specifically for the analytic-Gaussian comparison (Stage 1 Gate 1; dim $= 122$, still trivial). This is a propagator-correctness test, not a sweep point.

**Hilbert-space dimensions for the sweep** (bounded-amplitude cuts, $n_{\max} = 12$):

- $N = 1$: dim $= 2 \times 13 = 26$ (trivial).
- $N = 2$: dim $= 2 \times 169 = 338$ (trivial).
- $N = 3$: dim $= 2 \times 2197 = 4394$ (easy for sparse propagation).

*(Source: PA-02; Stage 1 prep convergence scan; Guardian option III-b; Standing Q 12.)*

---

## 3. Observables

Computed at each output timestep.

### 3.1 Per-trajectory

1. **Spin excitation probability:** $p(t) = \langle\Psi(t)|P_\uparrow|\Psi(t)\rangle$.
2. **Reduced-state eigenvalue spectrum:** $\{\lambda_j^{(k)}(t)\}$ from $\rho^{(k)}(t) = \mathrm{Tr}_{\bar k}|\Psi(t)\rangle\langle\Psi(t)|$.
3. **Effective orbital count:** $n_{\text{eff}}^{(k)}(t) = \exp\!\bigl(-\sum_j \lambda_j^{(k)}\log \lambda_j^{(k)}\bigr)$.
4. **Aggregate complexity (primary invariant):** $\mathcal{C}(t) = \sum_k \log n_{\text{eff}}^{(k)}(t)$. Report this, not per-mode curves, as the main complexity quantity. Per-mode curves are a *decomposition*, recorded but not headline. At $N=1$, $\mathcal{C}(t) = \log n_{\text{eff}}^{(1)}(t)$ trivially; the discipline matters at $N \geq 2$ under the mode-labelling ambiguity near degeneracy. *(Source: C3.2; Stage 2 forward item 2.)*

### 3.2 Ensemble and QPN observables

5. **Intrinsic variance:** $\sigma^2_{\text{intrinsic}}(t) = \mathrm{Var}_{\text{ensemble}}[p(t)]$ across $R$ trajectories with perturbed $\Delta_k$.
6. **QPN floor:** $\sigma^2_{\text{QPN}}(t; M) = p(t)[1-p(t)]/M$, computed on the ensemble mean $p(t)$.
7. **Detectability timing triple:** the voyage reports
   - $t_{\text{rise}}(M)$ — first time $\sigma^2_{\text{intrinsic}} > \sigma^2_{\text{QPN}}(M)$ (excluding $t = 0$ where round-off gives $\sigma^2$ a spurious positive floor).
   - $T_{\text{det}}(M)$ — last time $\sigma^2_{\text{intrinsic}} > \sigma^2_{\text{QPN}}(M)$ within the simulation window. Window-saturated in bounded recurrent regimes.
   - $f_{\text{resolved}}(M)$ — fraction of timesteps at which $\sigma^2_{\text{intrinsic}} > \sigma^2_{\text{QPN}}(M)$. **This is the headline scalar** used by the H3 scatter.

   Stage 3 finding: $T_{\text{det}}$-as-"last-exceedance" is dissipative-environment intuition that does not apply here. In the closed-system bounded-environment regime, $\sigma^2_{\text{intrinsic}}$ oscillates rather than decaying monotonically, and $T_{\text{det}}$ saturates at $t_{\max}$ at all $M$. The triple $(t_{\text{rise}}, T_{\text{det}}, f_{\text{resolved}})$ is the right characterisation; $f_{\text{resolved}}$ is the single scalar for cross-point comparison. *(Source: PA-03; Stage 3 §3.)*

### 3.3 Derived H2-relevant observables

8. **Rapid-growth quantity:** $|\dot{\mathcal{C}}(t)|$ — used for the H2 peak-alignment test (see §5). At N=1, the Schmidt-rank-2 bound caps $\mathcal{C}$ at $\log 2$, so the series peaks in $\mathcal{C}$ are sparse; $|\dot{\mathcal{C}}|$ is the informative quantity. *(Source: PA-04; Stage 4 §3.)*
9. **Time-averaged complexity:** $\bar{\mathcal{C}}$ over the resolvable window (where $\sigma^2_{\text{intrinsic}} > 10^{-8}$). Used as the scalar summary paired with $f_{\text{resolved}}(M)$ in the Stage 8 H3 scatter. *(Source: PA-03; Stage 3 §6 forward.)*

### 3.4 Discipline items for every stage

- **Short-time coefficient fits.** At each detuning point, fit $\lambda_2(t) = c_2 t^2 + c_4 t^4$ on the first $\sim 1$% of the window and record $(c_2, c_4)$. Stage 3 finding: $c_2$ is $\Delta$-independent at leading order ($c_2 = g^2$ to machine precision), $c_4$ carries the $\Delta$-dependence. *(Source: Guardian Stage 2 → 3 forward note; Stage 3 §4.)*
- **Spectrum-shape (IPR) test at $N \geq 2$.** At the first non-trivial multi-mode point (Stage 6 / Cut B), compute the inverse participation ratio $\mathrm{IPR} = \sum_j \lambda_j^2$ and compare to $1 / n_{\text{eff}}^2$. Equality supports the literal "effective orbital count" reading; inequality activates Scout C3.4 (entropy-is-not-complexity semantic concern) and requires the reading to be re-framed as a summary scalar rather than a count. At $N = 1$ the Schmidt-rank-2 structural bound makes the test trivial; it becomes meaningful at $N \geq 2$. *(Source: Guardian Stage 2 closing note; C3.4.)*
- **Normalisation logging.** Log $\|\psi(t)\|^2$ at every inspection point; reject runs above stated tolerance. *(Source: C3.6.)*
- **Convergence re-verification at each new observable.** $p(t)$-converged is not $n_{\text{eff}}$-converged; $n_{\text{eff}}$-converged is not $\sigma^2$-converged. Each stage that introduces a new observable runs its own $n_{\max}$-convergence check at $|\Delta| = 0.15$. *(Source: C3.5; Stages 2, 3 gates.)*

---

## 4. Sweep structure

### Cut A — Single mode ($N=1$)

Six-point detuning sweep per §2.4. 6 parameter points × 100 realisations = **600 trajectories**. *(PA-02: one more parameter point than v0.1's five.)*

### Cut B — Two modes ($N=2$)

Structured configurations, not full grid. Amended to exclude on-resonant points (both modes at $\Delta = 0$ would trigger the same runaway-amplitude issue as Cut A's excluded point):

- $(+0.15, +0.15)$ — symmetric near-resonance, innermost accessible point for each mode.
- $(+0.15, +0.3)$ — mild asymmetry with both modes near resonance.
- $(-0.15, +0.15)$ — symmetric straddling of resonance.
- $(+0.15, +0.5)$ — strong asymmetry.

4 parameter points × 100 realisations = **400 trajectories**. *(Source: PA-02 extension to multi-mode: no mode at $\Delta = 0$.)*

**Stage 6 additional gate:** IPR test at the first Cut B point (§3.4).

### Cut C — Three modes ($N=3$), commensurability comparison

Three structured configurations comparing commensurability regimes. All at baseline $\omega_1 = \omega_{\text{ref}}$:

| Config | $(\omega_1 : \omega_2 : \omega_3)$ | Type |
|---|---|---|
| C-Ra | $1 : \varphi : \varphi^2$ with $\varphi = 1.618\ldots$ | Golden-ratio incommensurate |
| C-Rb | $1 : \sqrt{2} : \sqrt{3}$ | Irrational incommensurate (alternative) |
| C-Rc | $3 : 5 : 7$ (scaled to unit reference) | Rational commensurate |

Detuning $\Delta_k$ swept uniformly at the Cut-A-compatible inner and outer points ($\pm 0.15, \pm 0.3$) per config; $\Delta_k = 0$ for any mode excluded per §2.4.

3 configs × 4 detuning sets × 100 realisations = **1200 trajectories**.

### Total compute

~2200 trajectories. Each at most $\sim 4400$-dim sparse propagation over 500 timesteps. Estimated runtime: a few hours on a standard machine. *(v0.1 estimate of ~1800 was based on the pre-amendment five-point Cut A and three detuning-sets on Cut C.)*

---

## 5. Hypotheses

- **H1 (weak, trivially expected).** Both $n_{\text{eff}}^{(k)}(t)$ and $\sigma^2_{\text{intrinsic}}(t)$ rise from their $t = 0$ values. Sanity check, not a real test.

- **H2 (moderate; growth-framing).** Peaks of $|\dot{\mathcal{C}}(t)|$ — the *moments of rapid complexity growth* — align temporally with peaks of $\sigma^2_{\text{intrinsic}}(t)$. Specifically, nearest-neighbour peak lag is small relative to the mean peak spacing, and Pearson $r\bigl(\sigma^2_{\text{intrinsic}},\,|\dot{\mathcal{C}}|\bigr) > 0$.

  **N=1 caveat (load-bearing).** At $N = 1$ the Schmidt-rank-2 bound caps $\mathcal{C}(t)$ at $\log 2$; $\mathcal{C}$ is structurally near-monotone, and the series-direct test (peaks in $\mathcal{C}$ vs peaks in $\sigma^2$) is *under-determined*. The growth-framing is the only H2 test that works at $N=1$. H2 becomes genuinely testable at $N \geq 2$ (Stage 6 onward), where the bound loosens and $\mathcal{C}$ has dynamical range. Stage 4 verified the growth-framing at the Cut A innermost point ($r = 0.497$, lag/spacing $= 0.15$): this is *pre-sweep confirmation*, not a full H2 verdict. The full test is pattern-consistency across Cut A (sweep-wide $r$ trend) plus the $N \geq 2$ picture. *(Source: PA-04; Stage 4 §3.)*

- **H3 (strong, Ordinans-adjacent).** Across the detuning sweep, $f_{\text{resolved}}(M)$ and $\bar{\mathcal{C}}$ co-vary monotonically: at the sweep's outer, far-from-resonance points, both are *low* (dynamics offers little to resolve; spin-mode entanglement stays close to product); at the inner, near-resonance points (the $|\Delta|/\omega_{\text{ref}} = 0.15$ edge of the accessible region), both are *high*. The claim is a *limit* claim, probed by fitting a trend across the three per-sign points $|\Delta|/\omega_{\text{ref}} \in \{0.15, 0.3, 0.5\}$ and extrapolating toward zero — not a point-claim at $\Delta = 0$ exactly (which is inaccessible in this voyage, §2.4 and Standing Q 12).

  The Stage 8 scatter plots $f_{\text{resolved}}(M = 1000)$ against $\bar{\mathcal{C}}$ across every Cut A / B / C parameter point. $T_{\text{det}}(M)$ and $t_{\text{rise}}(M)$ are recorded as diagnostics but are not the headline scalar: $T_{\text{det}}$ window-saturates in this bounded recurrent regime and $t_{\text{rise}}$ carries the same information as $f_{\text{resolved}}$ via a different projection. *(Source: PA-03; Stage 3 §6; Stage 4 §5 amendment flag A.)*

**H3 is the voyage's real target.** H1 is sanity, H2 is suggestive (with the N=1 caveat), H3 is the signature worth bringing to the MCTDH-numerics and open-systems collaborators.

---

## 6. Staged execution

Each stage produces an inspectable artifact; no stage begins without sign-off on the previous one. Stages 1–4 are complete at v0.2 issue; their gate structures are recorded here for reference rather than specification.

### Stage 1 — Single-mode propagator (complete)

Build the $N=1$ propagator in `src/hamiltonian.py`, `src/propagate.py`. Three anchors:

- (A) Analytic anchor at $\Delta = 0$, $n_{\max} = 60$. Target: $p(t) = \tfrac{1}{2}(1 + e^{-2 g^2 t^2})$, derived from the $\sigma_x$-eigenbasis factorisation into conditional displacements. *(PA-01: replaces v0.1's "$2g$ Rabi oscillations" phrasing, which was JC-folklore inapplicable to the unbiased Rabi model.)*
- (B) Convergence at $\Delta = 0.15$, $n_{\max} = 12$ vs $18$.
- (C) JC code-machinery sanity check: $p(t) = \cos^2(g t)$ on $H_{\text{JC}} = (\omega_0/2)\sigma_z + \omega a^\dagger a + g(\sigma_+ a + \sigma_- a^\dagger)$ at resonance (RWA). Independent anchor; not voyage physics.

**Go/no-go gates (all three must pass):**
1. max $|p_{\text{num}} - p_{\text{analytic}}| \leq 10^{-4}$ at anchor A.
2. max $|p_{n_{\max}=12} - p_{n_{\max}=18}| \leq 10^{-4}$ at anchor B.
3. Gauge-convention statement present in the stage's `notes.md`.

Stage 1 [commit `e3bb8ad`](stages/stage1_single_mode_propagator/) cleared all three at 4.23e-9, 1.36e-6, and structural.

### Stage 2 — Observables layer (complete)

Add reduced-state diagonalisation, $n_{\text{eff}}(t)$, $\mathcal{C}(t)$.

**Go/no-go gates:**
4. max $|n_{\text{eff}}^{n_{\max}=12} - n_{\text{eff}}^{n_{\max}=18}| \leq 10^{-4}$ at $\Delta = 0.15$.
4a. max $|n_{\text{eff}} - n_{\text{eff}}^{\text{analytic}}| \leq 10^{-4}$ at $\Delta = 0$, against the closed-form Schmidt eigenvalues $\lambda_{1,2}(t) = \tfrac{1}{2}(1 \pm e^{-2 g^2 t^2})$.
5. Rank of $\rho^{(1)}$ above $10^{-10}$ tolerance equals $2$ (Schmidt-rank-2 bound at $N = 1$; structural).
6. Early-time fit $\lambda_2(t) = c_2 t^2 + c_4 t^4$ on $t \in (0.1, 0.5]$, $|c_2 - g^2| \leq 10^{-6}$.

Stage 2 [commit `1008eee`](stages/stage2_observables/) cleared all at 8.88e-16, 1.74e-6, rank $=2$, 1.81e-8.

### Stage 3 — Ensemble and QPN layer (complete)

Add the 100-realisation $\Delta$-noise ensemble at the innermost Cut A point ($\Delta = 0.15$). Primary artifact: three-panel figure. Extended scope:

- **QFI-reduction check:** compare $\sigma^2_{\text{intrinsic}}$ to $(\partial_\Delta p)^2 \sigma_\Delta^2$ (Scout C2 small-noise reduction). *(Source: reconciliation Standing item 1.)*
- **BLP cross-check:** trace distance on an antipodal initial-state pair; test the reconciliation R2 divergence. *(Source: Standing item 11.)*
- **1%-RMS reframing:** stage writeup makes explicit that the noise level is a stress test, not a realistic operating point. *(Source: reconciliation Standing item 6.)*

**Go/no-go gates:**
7. max $|\sigma^2_{n_{\max}=12} - \sigma^2_{n_{\max}=18}| \leq 10^{-5}$ (statistical-noise-aware target).
8. Median $|\sigma^2_{\text{intrinsic}} - (\partial_\Delta p)^2 \sigma_\Delta^2| / \sigma^2_{\text{intrinsic}} \leq 0.10$ on the mask $\sigma^2 > 10^{-8}$.
9. BLP trace-distance non-monotone (sign changes in $\dot D(t) > 0$).
10. 1%-RMS stress-test language present in stage `notes.md`.

Stage 3 [commit `cc1bf5e`](stages/stage3_ensemble_qpn/) cleared all at 1.99e-6, 6.98%, 2 sign changes, structural. Resolutions: **QFI reduction confirmed** at $\Delta = 0.15$ (Scout C5 reduction-path 3 live); **R2 divergence resolved in Verifier's favour** (BLP well-defined and recurrence-sensitive; Scout C5 "under-applicable" clause struck from Stage 8).

### Stage 4 — H2 checkpoint (complete)

Inspect alignment of $|\dot{\mathcal{C}}(t)|$ peaks and $\sigma^2_{\text{intrinsic}}(t)$ peaks on the Stage 3 data. *(Amended from v0.1's "peaks in $\mathcal{C}(t)$ align with peaks in $\sigma^2$" to match the plan's own "moments of rapid complexity growth" text.)*

**Verdict structure:** if the growth-framing alignment is visible *and* $\mathcal{C}$ does not saturate to the Schmidt bound, H2 is supported and the voyage proceeds. If $\mathcal{C}$ saturates (as at $N = 1$ — 99.93% of $\log 2$ in Stage 4 data), H2 is *under-tested* rather than failed: the test reduces to checking the growth-framing alone, and full H2 is deferred to $N \geq 2$. Stage 4 commit `1e8d4a0` confirmed growth-framing at $r = 0.497$, lag/spacing $= 0.15$; verdict: proceed to Stage 5 with the full H2 test deferred to Stage 6 / Cut B.

### Stage 5 — Cut A (single-mode detuning sweep)

Run the 6-point Cut A. For each parameter point, produce:

- $p(t)$ trajectory (ensemble mean and band), $n_{\text{eff}}(t)$, $\mathcal{C}(t)$, $|\dot{\mathcal{C}}(t)|$, $\sigma^2_{\text{intrinsic}}(t)$;
- $(t_{\text{rise}}(M), T_{\text{det}}(M), f_{\text{resolved}}(M))$ for $M \in \{100, 1000, 10^4\}$;
- Pearson $r(\sigma^2, |\dot{\mathcal{C}}|)$ over the resolvable window;
- $\bar{\mathcal{C}}$ (time-average over the resolvable window);
- $(c_2(\Delta), c_4(\Delta))$ short-time fit.

**Gate 11:** for each Cut A point, the $n_{\max} = 12$ default converges to $10^{-5}$ against $n_{\max} = 18$ on the $\sigma^2$ observable (the tightest-converging observable per Stages 1–3). Documented per detuning point.

**Artifact:** Cut A summary figure showing the $f_{\text{resolved}}$-vs-$\bar{\mathcal{C}}$ trend across the six detuning points, plus per-point trajectory overlays.

### Stage 6 — Cut B (two modes)

Add a second mode (§2.1 extended to $N = 2$), verify convergence, run Cut B.

**Gate 12 — IPR at first multi-mode point.** At the first Cut B point, compute $\mathrm{IPR} = \sum_j \lambda_j^2$ on the reduced $\rho^{(1)}$ and $\rho^{(2)}$ spectra and compare to $1/n_{\text{eff}}^2$. Equality supports the literal effective-orbital-count reading; large deviation activates Scout C3.4 semantic caveat. Report the test whichever way it comes out. *(Source: Guardian Stage 2 forward note.)*

**Gate 13 — Full H2 test** (as opposed to the Stage 4 growth-framing fragment). At $N = 2$ the Schmidt bound is $\log \min\bigl(n_{\max}+1,\, 2(n_{\max}+1)\bigr) = \log 13 \approx 2.57$ — plenty of dynamical range for $\mathcal{C}$. Test both series-direct and growth-framing H2 at each Cut B point, report both.

**Artifact:** Cut B summary plus Gate 12 / 13 verdicts.

### Stage 7 — Cut C (three modes, commensurability)

Run Cut C. Produce comparison across commensurability regimes, report the H3 scatter contribution per config.

### Stage 8 — Synthesis

- **H3 scatter plot (headline figure):** $f_{\text{resolved}}(M = 1000)$ vs $\bar{\mathcal{C}}$ across all Cut A / B / C parameter points. $T_{\text{det}}$ and $t_{\text{rise}}$ as diagnostic side panels. *(Source: PA-03; the H3 redefinition displaces v0.1's $T_{\text{det}}$-vs-saturation-$\mathcal{C}$ plot.)*
- **One-page writeup:** which hypotheses survived, parameter values, outcomes. The writeup must:
  - Use the Scout C5 novelty paragraph as the backbone, with the "under-applicable" clause struck (Stage 3 Gate 9 resolution);
  - Contract along C5 reduction-path 3 *unless* Stage 5 sweep data contradicts the Stage 3 Gate 8 QFI-reduction confirmation;
  - State H2's $N = 1$ under-testing explicitly and report the Stage 6 full-H2 result;
  - Report the Stage 6 Gate 12 IPR verdict alongside the $n_{\text{eff}}$ claim;
  - Report the Stage 7 commensurability comparison as the voyage's most Ordinans-adjacent finding.
- **Collaborator-handoff notes:** one for MCTDH-numerics (bounded MCTDH scenario), one for open-systems (non-Markovianity witness question, now framed against the Stage 3 BLP result).

---

## 7. Scope limits (Guardian restraint)

Explicitly *not* in this voyage:

- Ultrastrong-coupling sweep (fixed $g/\omega = 0.1$).
- Coupling-strength noise (fixed $g_k$).
- Axial mode structure.
- Realistic technical noise budget beyond trap-frequency drift (1% RMS is the stress-test level, not a realism claim).
- Decoherence channels (closed-system dynamics throughout).
- Beyond-Lamb–Dicke corrections.
- MCTDH comparison (exact propagation only; MCTDH is a parallel collaborator's domain).
- On-resonance point $\Delta = 0$ (inaccessible with the voyage initial state under any finite Fock budget; see Standing Q 12).
- Krylov-propagator infrastructure (out of scope; raised at Stage 1 prep as a deferred option; belongs in a follow-up voyage).

Any of these can motivate a follow-up voyage. In this one, they stay fixed.

---

## 8. Failure modes and honest outcomes

| Mode | Interpretation |
|---|---|
| $n_{\text{eff}}$ and $\sigma^2_{\text{intrinsic}}$ grow on disjoint timescales | Theoretical complexity and measurement variance probe different things; framework needs revision. |
| H2 growth-framing holds at $N = 1$ (Stage 4) but Stage 6 full H2 test fails at $N = 2$ | Single-mode growth-alignment is an artefact of the Schmidt-rank-2 cap; H2 does not extend. Useful scoping bound on the voyage's central claim. |
| $f_{\text{resolved}}$ and $\bar{\mathcal{C}}$ do not co-vary across Cut A | H3 fails at $N = 1$; continue Cut B / C only if a structural reason to expect the co-variation to emerge at higher $N$. |
| Convergence failure at $n_{\max} = 12$ on any Cut A point | Exact-propagation proxy fails at that point; document and raise $n_{\max}$ at that point (adaptive by necessity at the innermost, not by default). |
| 1% $\Delta$-noise too small to generate signal | Noise model insufficient; escalate to realistic ²⁵Mg⁺ levels or re-examine the stress-test framing. |
| IPR $\ne 1/n_{\text{eff}}^2$ at Cut B | Scout C3.4 bites: $n_{\text{eff}}$ reads as a summary scalar rather than a literal count. Writeup re-frames accordingly; no voyage-invalidating conclusion. |
| QFI-reduction (Gate 8) confirmed sweep-wide | C5 reduction-path 3 fires; Stage 8 novelty contracts to "trapped-ion-parameterised implementation of a QFI-flow witness". Still a legitimate finding. |
| H3 holds cleanly | Bring to MCTDH-numerics collaborator (bounded MCTDH follow-up) and open-systems collaborator (non-Markovianity witness formalisation). |

All outcomes, including nulls, get recorded.

---

## 9. Deliverables

1. Propagation and analysis code (Python: numpy, scipy, qutip available).
2. Per-stage inspection figures (Stages 1–4 committed; 5–7 to come; 8 synthesis).
3. Synthesis figure (Stage 8): the H3 scatter of $f_{\text{resolved}}(M=1000)$ vs $\bar{\mathcal{C}}$.
4. One-page writeup: parameters, outcomes, next steps.
5. This document (v0.2), version-controlled; amendment trail in `PLAN_AMENDMENTS.md`.

---

## 10. Standing questions

*Source legend retained from v0.1 §10: C3.n = Scout C3 pitfall; P# = Verifier Pn return; HM = Harbourmaster-derived. Status annotations added 2026-04-14 at v0.2 issue.*

### Cleared by Stages 1–4

1. **Fock-truncation entropy ceiling** (C3.1). **Cleared**: convergence scans at Stage 1 Gate 2 and Stage 2 Gate 4 confirm $n_{\max} = 12$ default suffices at all Cut A points down to $|\Delta| = 0.15$.
5. **MCTDH-adjacent lessons** (C3.5). **Cleared as a general discipline**: §3.4 requires per-observable convergence re-verification. Specific case ($n_{\text{eff}}$-convergence distinct from $p$-convergence) verified at Stage 2; ($\sigma^2$-convergence distinct from $n_{\text{eff}}$-convergence) verified at Stage 3.
6. **Normalisation drift** (C3.6). **Cleared**: $\|\psi\|^2 - 1 \leq 1.4 \times 10^{-15}$ across all Stage 1–3 runs with the dense-eigh propagator.
7. **Initial-state invariance** (C3.7). **Cleared**: $|\uparrow\rangle|0\rangle$ is held across Stages 1–3; the BLP pair $|\downarrow\rangle|0\rangle$ is supplement-only.
8. **Gauge convention** (P1). **Cleared**: §2.1 documented, Stage 1 Gate 3 confirmed, code assembly uniform.
11. **Canonical-measure applicability — R2 divergence**. **Cleared in Verifier's favour** at $\Delta = 0.15$: BLP non-monotonicity with 2 sign changes, $N_{\text{BLP}} = 0.97$ (Stage 3 Gate 9). Scout's "under-applicable" clause is struck from the Stage 8 novelty writeup.
12. **Resonance-point accessibility**. **Cleared-as-scoping**: §2.4 excludes $\Delta = 0$; H3 is a limit claim fit from $|\Delta| \geq 0.15$.

### Live for Stage 5 onward

2. **Mode-labelling ambiguity near degeneracy** (C3.2). **Live at Stage 6/7**: report aggregate $\mathcal{C}(t)$ as the primary invariant (already encoded in §3.1 item 4). Trivial at $N = 1$.
3. **Early-time $t^2$ universal growth** (C3.3). **Live as discipline**: §3.4 requires per-detuning $(c_2, c_4)$ fits. Stage 3 confirmed $c_2 \approx g^2$ is $\Delta$-independent at leading order; Stage 5 tracks $c_4(\Delta)$ across the sweep.
4. **Entropy is not complexity** (C3.4). **Live at Stage 6**: IPR test specified as Gate 12 in §6.
9. **Noise spectrum, not only variance** (P4 / D9). **Live, optional**: at least one Stage 5 cut should include a coherent-modulation noise component (AC-line analogue). Not a hard gate.
10. **Non-Markovianity formalism choice** (P5). **Live**: if Stage 8 invokes non-Markovianity quantitatively (e.g. reports $\mathcal{N}_{\text{BLP}}$ beyond the fixed-pair Stage 3 value), compute at least two formalisms for cross-check.

### Live as scoping / parameter questions

- Simulation window of $50\,\omega_{\text{ref}}^{-1}$: **reformulated at v0.2**. Stage 3 finding is that extending the window does not change the qualitative picture in bounded recurrent regimes (σ² keeps oscillating); the window is scientifically adequate for the $f_{\text{resolved}}$ reading. Extension would be needed only for a monotone-decay-style $T_{\text{det}}$, which is not the voyage's reporting choice.
- Cut C commensurability configs: execute all three, or drop one if Cut A + B already settle H3? **Decision deferred to Stage 7 preamble.**
- QFI-reduction sweep-wide confirmation: Stage 3 confirmed at $\Delta = 0.15$; Stage 5 can show uniform holding, degradation at innermost points, or a clean crossover. **Live; Stage 5 reports.**

### Deferred beyond this voyage (follow-up TASK_CARD v3 / future work)

- **Krylov / spread-complexity identity check** for $n_{\text{eff}}^{(k)}$. Pending `TASK_CARD` v3 literature expansion; Stage 8 writeup cannot claim novelty on this component until addressed. *(Source: reconciliation §R6 item 1.)*
- **On-resonance dynamics with a matched initial state.** Standing Q 12 enumerates three follow-up paths (coherent-state initial, Krylov propagator with adaptive cutoff, explicit analytic limit). Out of scope for this voyage.
- **Full BLP pair optimisation.** Stage 3 used a fixed antipodal pair; quantitative $\mathcal{N}_{\text{BLP}}$ requires pair optimisation if Stage 8 claims a definite value. *(Source: Stage 3 §6 forward item 3.)*

---

*End of VOYAGE_PLAN.md v0.2. Ready for Stage 5 / Cut A launch.*
