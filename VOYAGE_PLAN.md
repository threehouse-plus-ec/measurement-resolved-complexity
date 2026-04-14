# Measurement-Resolved Complexity Voyage

**Endorsement Marker:** T(h)reehouse +EC voyage plan — internal numerical exploration. Local candidate framework under T(h)reehouse +EC stewardship. No external endorsement implied.

**Licence:** Coastline layer, CC BY-SA 4.0 (see repository `LICENCE`).

**A bounded numerical exploration: spin coupled to few radial motional modes under detuning sweep**

---

## Metadata

- **Working title:** Measurement-resolved complexity in a spin coupled to few radial motional modes
- **Started:** 2026-04-14
- **Stance:** Exploratory, self-contained, Harbourmaster discipline
- **Status:** Pre-execution — parameters locked, staging defined, awaiting repo and go-ahead
- **Not:** a replacement for parallel MCTDH work by a numerics collaborator; a validation of Ordinans; a publication-ready study

---

## 1. Purpose

Test whether two time-resolved complexity measures exhibit correlated dynamics in a spin coupled to a small number of *radial* motional modes, across a detuning sweep at fixed intermediate coupling:

- **Intrinsic (theorist-visible):** $n_{\text{eff}}^{(k)}(t)$, the effective number of natural orbitals per mode, derived from single-mode reduced-density-matrix eigenvalues.
- **Operational (experiment-visible):** $\sigma^2_{\text{intrinsic}}(t)$, the shot-to-shot spin-population variance under realistic parameter noise, thresholded against quantum projection noise $\sigma^2_{\text{QPN}}(t; M)$.

If they track each other, the Ordinans-plus-QPN proposal has empirical footing worth bringing to the MCTDH-numerics collaborator and the open-systems collaborator. If not, the framework's theoretical spine does not map cleanly onto the variance signal, and the framing needs revision before committing group resources. Both outcomes are useful.

---

## 2. Physical setup

### 2.1 Hamiltonian

Rotating frame, Lamb–Dicke approximation retained, **no RWA imposed** (full $\sigma_x$ coupling preserves counter-rotating terms, which matter at $g/\omega = 0.1$):

$$H = \sum_{k=1}^{N} \Delta_k \, a_k^\dagger a_k + \sum_{k=1}^{N} g_k \, \sigma_x (a_k + a_k^\dagger)$$

with $\Delta_k = \omega_k - \omega_{\text{drive}}$ the spin–mode detuning.

**Gauge convention.** Stokes & Nazir (2019) demonstrate that the presence of counter-rotating terms in ultrastrong and intermediate-coupling spin-boson Hamiltonians is gauge-dependent (see reconciliation §R3 item 8). The form above corresponds to the **dipole-gauge** spin-boson Hamiltonian in the rotating frame, in which counter-rotating terms are explicit and not gauge-removable without a Bogoliubov transformation. Stage 1 sign-off requires explicit documentation of this gauge choice in the run notes so that "no RWA" is unambiguous.

### 2.2 Reference units

$\omega_{\text{ref}}$ sets the frequency unit; all times in units of $\omega_{\text{ref}}^{-1}$. Dimensional mapping to ²⁵Mg⁺ radial-mode frequencies (MHz range) deferred to writeup.

### 2.3 Initial state

$|\Psi(0)\rangle = |\uparrow\rangle \otimes |0\rangle^{\otimes N}$ — spin excited, all modes in vacuum.

### 2.4 Locked parameter choices

| Parameter | Value | Rationale |
|---|---|---|
| Coupling $g_k / \omega_{\text{ref}}$ | $0.1$ (all modes, fixed) | Intermediate regime, approaching ultrastrong boundary; counter-rotating terms non-negligible |
| Detuning range (Cut A) | ~~$\Delta / \omega_{\text{ref}} \in \{-0.5, -0.2, 0, +0.2, +0.5\}$~~ **Superseded 2026-04-14:** $\Delta / \omega_{\text{ref}} \in \{-0.5, -0.3, -0.15, +0.15, +0.3, +0.5\}$ | Six points, symmetric, evenly log-ish-spaced, three per sign. $\Delta = 0$ dropped because the §2.1 Hamiltonian with the $\|\uparrow\rangle\|0\rangle$ initial state drives unbounded coherent-amplitude growth at exactly zero detuning (see §2.5 and `PLAN_AMENDMENTS.md`). Inner sampling at $|\Delta|/\omega_{\text{ref}} = 0.15$ is the closest approach at which a *homogeneous* $n_{\max}=12$ default with $n_{\max}=18$ convergence check meets the Stage-1 error target (see §2.5 convergence table). H3 is re-read as a limit-claim probed by fitting a trend across the three points per sign and extrapolating *toward* zero, not as a point-claim at the limit itself. |
| Mode type | Radial | Contribute more equally than axial (no COM hierarchy); detuning sweep samples symmetric coupling landscape |
| Fock truncation $n_{\max}$ | $12$ per mode (default); $18$ for on-resonance convergence check | See §2.5 |
| Noise model | Trap-frequency drift only — Gaussian noise on $\Delta_k$, 1% RMS | **Deliberate stress-test level**, not a realistic operating-point prediction. Published active-feedback trapped-ion platforms achieve $\sim 5 \times 10^{-6}$ short-term (Verifier P4 / D3); clock-grade systems approach $\sim 10^{-18}$. 1% RMS is chosen to force visible ensemble variance at modest $M$; Stage 3 writeup reframes accordingly (see `literature_search/reconciliation.md` §R3 item 9 and Standing item 6). |
| Coupling noise | None (fixed $g_k$) | Simplifies noise structure; follow-up voyage can relax |
| Ensemble size $R$ | 100 trajectories per parameter point | Balance statistical power vs. compute |
| Shot budgets $M$ | $\{100, 1000, 10\,000\}$ | Spans realistic experimental range |
| Simulation window | $t \in [0, 50 \, \omega_{\text{ref}}^{-1}]$ | Long enough for several Rabi-scale oscillations; adjust after Stage 1 |
| Output timesteps | 500 points, uniform | Smooth plots; negligible cost |

### 2.5 Fock truncation justification

~~At $g/\omega = 0.1$, on-resonance ($\Delta = 0$) vacuum-Rabi dynamics populates Fock states up to $n \sim 5$–$8$ at coherent-excursion peaks. Counter-rotating terms (no RWA) can push further. $n_{\max} = 12$ gives a safety margin of ~4 levels above expected population; $n_{\max} = 18$ convergence check in Stage 1 confirms this is sufficient.~~

**Superseded 2026-04-14 (Stage 1 prep).** The struck paragraph imported JC-Rabi folklore ("$n \sim 5\text{–}8$ at vacuum-Rabi coherent-excursion peaks") into the unbiased Rabi Hamiltonian of §2.1, where it does not apply. Correct analysis:

- **At non-zero detuning** with the voyage initial state $|\uparrow\rangle|0\rangle$, each $\sigma_x$-sector sees $H_\pm = \Delta\, a^\dagger a \pm g(a + a^\dagger)$ — a harmonic oscillator with a constant linear force. Solving the Heisenberg equation $\dot a = -i\Delta\, a \mp i g$ with $a(0) = 0$ gives
  $$\alpha_\pm(t) = \mp \frac{g}{\Delta}\bigl(1 - e^{-i\Delta t}\bigr), \qquad |\alpha_\pm(t)|^2 = \frac{4 g^2}{\Delta^2}\sin^2\!\tfrac{\Delta t}{2},$$
  so the mode occupation in each branch is bounded by $\langle n \rangle_{\max} = 4 g^2 / \Delta^2$, reached at $\Delta t = \pi$. The factor of 4 is the interference between the drive and the free-oscillation phase; a naive "$\langle n \rangle \lesssim (g/|\Delta|)^2$" estimate (which does *not* account for this interference) underestimates the Fock requirement by a factor of 4.

- **At exactly $\Delta = 0$** with the same initial state, the linear-force term is unopposed: $|\alpha(t)| = g t$ and $\langle n \rangle = (g t)^2$ is unbounded in $t$ — no finite Fock budget saturates. This point is excluded from Cut A (see §2.4 superseding note). It is not a property of the model alone; a different initial state (for example a $\sigma_x$-eigenstate tensor a matched coherent state) would give bounded dynamics. See Standing Question #12.

- **Convergence data (not folklore, measured truncation-convergence against a reference at $n_{\max} + 20$, simulation window $t \in [0, 50\,\omega_{\text{ref}}^{-1}]$, $g/\omega_{\text{ref}} = 0.1$):**

  | $|\Delta|/\omega_{\text{ref}}$ | $\langle n\rangle_{\max}$ | $n_{\max}=12$ | $n_{\max}=18$ | $n_{\max}=30$ | floor for $10^{-4}$ |
  |---:|---:|---:|---:|---:|:---|
  | 0.05 | 16.00 | $4.4\!\times\!10^{-3}$ | $2.8\!\times\!10^{-4}$ | $1.4\!\times\!10^{-7}$ | $n_{\max} \geq 30$ |
  | 0.07 | 8.16 | $4.3\!\times\!10^{-3}$ | $1.6\!\times\!10^{-4}$ | $4.7\!\times\!10^{-10}$ | $n_{\max} \geq 30$ |
  | 0.10 | 4.00 | $2.4\!\times\!10^{-3}$ | $1.9\!\times\!10^{-6}$ | $5.4\!\times\!10^{-15}$ | $n_{\max} \geq 18$ |
  | 0.12 | 2.78 | $1.2\!\times\!10^{-4}$ | $9.5\!\times\!10^{-9}$ | $1.6\!\times\!10^{-15}$ | $n_{\max} \geq 18$ |
  | **0.15** | **1.78** | $\mathbf{1.4\!\times\!10^{-6}}$ | $8.0\!\times\!10^{-12}$ | $2.7\!\times\!10^{-15}$ | $\mathbf{n_{\max} = 12}$ |
  | 0.20 | 1.00 | $8.9\!\times\!10^{-9}$ | $2.6\!\times\!10^{-15}$ | $2.2\!\times\!10^{-15}$ | $n_{\max} = 12$ |
  | 0.50 | 0.16 | $8.9\!\times\!10^{-16}$ | $4.4\!\times\!10^{-16}$ | $1.6\!\times\!10^{-15}$ | $n_{\max} = 12$ |

  The innermost Cut A point $|\Delta|/\omega_{\text{ref}} = 0.15$ (bold row) is the closest approach at which a *homogeneous* $n_{\max} = 12$ default clears the $10^{-4}$ target with margin, with $n_{\max} = 18$ as the convergence check.

- **Code-anchor validation** (Stage 1 gate 1) is run at $\Delta = 0$ with $n_{\max} = 60$ specifically for the analytic-Gaussian comparison (dim $= 122$, still trivial). This is a propagator-correctness test, not a sweep point.

Hilbert-space dimensions for the sweep (bounded-amplitude cuts, $n_{\max} = 12$):
- $N=1$: $2 \times 13 = 26$ (trivial)
- $N=2$: $2 \times 169 = 338$ (trivial)
- $N=3$: $2 \times 2197 = 4394$ (easy for sparse propagation)

---

## 3. Observables

Computed at each output timestep:

1. **Spin excitation probability:** $p(t) = \langle \Psi(t) | P_\uparrow | \Psi(t) \rangle$
2. **Per-mode natural occupations:** $\{\lambda_j^{(k)}(t)\}$ from $\rho^{(k)}(t) = \text{Tr}_{\bar{k}} |\Psi(t)\rangle\langle\Psi(t)|$
3. **Effective orbital count:** $n_{\text{eff}}^{(k)}(t) = \exp\left(-\sum_j \lambda_j^{(k)}(t) \log \lambda_j^{(k)}(t)\right)$
4. **Aggregate complexity:** $\mathcal{C}(t) = \sum_k \log n_{\text{eff}}^{(k)}(t)$
5. **Intrinsic variance:** $\sigma^2_{\text{intrinsic}}(t) = \text{Var}_{\text{ensemble}}[p(t)]$ across $R$ trajectories with perturbed $\Delta_k$
6. **QPN floor:** $\sigma^2_{\text{QPN}}(t; M) = p(t)[1-p(t)]/M$
7. **Detectability horizon:** $T_{\text{det}}(M) = \max\{t : \sigma^2_{\text{intrinsic}}(t) > \sigma^2_{\text{QPN}}(t; M)\}$

---

## 4. Sweep structure

### Cut A — Single mode ($N=1$)

Full 5-point detuning sweep. 5 parameter points × 100 realisations = 500 trajectories.

### Cut B — Two modes ($N=2$)

Structured configurations, not full grid:
- $(0, 0)$ — both resonant
- $(0, 0.2)$ — one resonant, one detuned
- $(-0.2, +0.2)$ — symmetric detuning
- $(0, 0.5)$ — strong asymmetry

4 parameter points × 100 realisations = 400 trajectories.

### Cut C — Three modes ($N=3$), commensurability comparison

Three structured configurations comparing commensurability regimes. All at baseline $\omega_1 = \omega_{\text{ref}}$:

| Config | $(\omega_1 : \omega_2 : \omega_3)$ | Type |
|---|---|---|
| C-Ra | $1 : \varphi : \varphi^2$ with $\varphi = 1.618...$ | Golden-ratio incommensurate |
| C-Rb | $1 : \sqrt{2} : \sqrt{3}$ | Irrational incommensurate (alternative) |
| C-Rc | $3 : 5 : 7$ (scaled to unit reference) | Rational commensurate |

Detuning $\Delta_k$ swept uniformly (three values: on-resonant, symmetric $\pm 0.2$) per config.

3 configs × 3 detuning sets × 100 realisations = 900 trajectories.

### Total compute

~1800 trajectories. Each at most $\sim 4400$-dim sparse propagation over 500 timesteps. Estimated runtime: tens of minutes to a few hours on a standard machine.

---

## 5. Hypotheses

- **H1 (weak, trivially expected):** both $n_{\text{eff}}^{(k)}(t)$ and $\sigma^2_{\text{intrinsic}}(t)$ rise from their $t=0$ values. Not a real test.
- **H2 (moderate):** temporal alignment of peaks/shoulders in $\mathcal{C}(t)$ and $\sigma^2_{\text{intrinsic}}(t)$. Moments of rapid complexity growth coincide with moments of large ensemble variance.
- **H3 (strong, Ordinans-native):** as detuning is swept through resonance ($\Delta \to 0$), both $T_{\text{det}}(M)$ and the saturation value of $\mathcal{C}(t)$ scale in a correlated way. Off-resonant: short $T_{\text{det}}$, low $\mathcal{C}$. Near-resonant: long $T_{\text{det}}$, high $\mathcal{C}$. **Reading (clarified 2026-04-14):** "$\Delta \to 0$" is a *limit* claim, probed by fitting a trend across the three per-sign points at $|\Delta|/\omega_{\text{ref}} \in \{0.15, 0.3, 0.5\}$ and extrapolating *toward* zero, not a *point* claim at $\Delta = 0$ exactly (see §2.4 and §2.5 superseding notes and Standing Question #12).

**H3 is the voyage's real target.** H1 is sanity, H2 is suggestive, H3 is the signature worth bringing to the MCTDH-numerics and open-systems collaborators.

---

## 6. Staged execution

Each stage produces an inspectable artifact; no stage begins without sign-off on the previous one.

### Stage 1 — Single-mode propagator

Minimal $N=1$ propagation engine. Verify against Jaynes–Cummings analytics at $\Delta=0, g/\omega = 0.1$ ~~(vacuum Rabi oscillations at frequency $2g$ with counter-rotating corrections)~~. Run convergence check: $n_{\max} = 12$ vs. $18$ on the on-resonance case, confirm $p(t)$ agreement to $\sim 10^{-4}$.

**Superseded 2026-04-14 (Stage 1 prep).** The §2.1 Hamiltonian is the unbiased Rabi model (no $\sigma_z$ term in the rotating frame); at $\Delta = 0$ it does not produce $2g$ vacuum Rabi oscillations. The correct analytic target is $p(t) = \tfrac{1}{2}(1 + e^{-2 g^2 t^2})$ — a Gaussian monotonic decay from $1$ to $1/2$, derived by factorising $H = g \sigma_x (a + a^\dagger)$ in the $\sigma_x$ eigenbasis into conditional displacements of the mode vacuum, $|\alpha_\pm(t)\rangle$ with $\alpha_\pm(t) = \mp i g t$. Stage 1 validates against this form. A separate JC code-machinery sanity check — $p(t) = \cos^2(g t)$ on $H_{\text{JC}} = (\omega_0/2) \sigma_z + \omega a^\dagger a + g (\sigma_+ a + \sigma_- a^\dagger)$ at resonance (RWA) — is run alongside as an independent anchor.

**Artifact:** single figure showing $p(t)$ for the on-resonance case, overlaid with the $n_{\max}$ convergence comparison, plus a short `notes.md` including the gauge-convention statement.

**Go/no-go gates (all three must pass):**
1. Propagator validated against JC analytics at $\Delta=0$ to $\sim 10^{-4}$ absolute in $p(t)$.
2. $n_{\max}=12$ vs. $n_{\max}=18$ agreement to the same tolerance (per §2.5 and Standing item 1).
3. **Gauge-convention statement** present in `stages/stage1_single_mode_propagator/notes.md`, stating: (i) the gauge adopted (per §2.1), (ii) where in the code the Hamiltonian assembly enforces it, (iii) what "no RWA" means *within* that gauge — per reconciliation §R3 item 8 / Standing item 5. Without this, "no RWA" is not yet unambiguous and Stage 2 cannot begin.

### Stage 2 — Observables layer

Add natural-occupation diagonalisation and $n_{\text{eff}}(t)$ computation on the Stage 1 run. Verify $n_{\text{eff}}(0) = 1$ and monotonic early-time growth.

**Artifact:** two-panel figure: $p(t)$ above, $n_{\text{eff}}(t)$ below, same axis.

**Go/no-go:** complexity measure behaves sensibly.

### Stage 3 — Ensemble and QPN layer

Add the 100-realisation ensemble with $\Delta$-noise, compute $\sigma^2_{\text{intrinsic}}(t)$, compare to $\sigma^2_{\text{QPN}}(t; M)$ for three $M$ values. Still $N=1$, still on-resonance only.

**Primary artifact:** three-panel figure showing $p(t)$, $n_{\text{eff}}(t)$, and $\sigma^2_{\text{intrinsic}}(t)$ vs. $\sigma^2_{\text{QPN}}(t; M)$ curves for $M \in \{100, 1000, 10^4\}$.

**Extended scope (added 2026-04-14, from reconciliation Standing items 1–2):**
1. **QFI-reduction check.** On the same trajectory ensemble, compute the small-noise-limit Fisher-information criterion $(\partial_{\Delta}\langle \sigma_z \rangle)^2 \sigma_\Delta^2$ and compare against $\sigma^2_{\text{intrinsic}}(t)$. If they coincide across the simulation window, Scout's C2 candidate reduction holds and the operational-crosswalk novelty contracts along the third reduction path in reconciliation §R5. **Artifact:** an additional fourth panel or a companion figure overlaying the two.
2. **BLP trace-distance cross-check.** Compute the BLP non-Markovianity witness (trace distance between the reduced spin states for a representative antipodal pair, its time-derivative sign-integral) on a sample trajectory. This tests the canonical-measure-applicability divergence (Scout: under-applicable in recurrent regimes; Verifier: well-defined) flagged in reconciliation R2. **Artifact:** companion figure and a one-paragraph note stating which reading the Stage 3 evidence supports.

**Also:** Stage 3 writeup must reframe the 1% RMS noise level as a deliberate stress-test rather than a realistic operating-point prediction (§2.4 rationale note, reconciliation Standing item 6).

**Symmetry note for the on-resonance cut (added 2026-04-14, Stage 1 prep).** At $\Delta=0$, the §2.1 Hamiltonian has a $\Delta \to -\Delta$ symmetry (combined with a bosonic phase rotation) that forces $\partial_\Delta p\rvert_{\Delta=0} = 0$. The leading small-noise contribution to $\sigma^2_{\text{intrinsic}}(t)$ at $\Delta=0$ is therefore second-order in the detuning-noise width $s$, i.e. $\tfrac{1}{2}(\partial_\Delta^2 p)^2 s^4 + O(s^6)$, *not* first-order $(\partial_\Delta p)^2 s^2$. The QFI-reduction check above must compute the second-order term on the on-resonance cut; the first-order expression is the right object only at non-zero-$\Delta$ points of Cut A.

### Stage 4 — Go/no-go checkpoint on H2

Inspect Stage 3 figure. Do peaks in $\mathcal{C}(t)$ align with peaks in $\sigma^2_{\text{intrinsic}}(t)$ even qualitatively? If yes → proceed. If no → stop, reconsider framework, consult before continuing.

### Stage 5 — Cut A (single-mode detuning sweep)

Run Cut A. Produce the Cut A summary figure.

### Stage 6 — Cut B (two modes)

Add second mode, verify convergence still holds, run Cut B.

### Stage 7 — Cut C (three modes, commensurability)

Run Cut C. Produce comparison across commensurability regimes.

### Stage 8 — Synthesis

- Scatter plot: $T_{\text{det}}(M=1000)$ vs. saturation $\mathcal{C}$, across all parameter points. This is the **H3 diagnostic plot**.
- One-page writeup recording which hypotheses survived, parameter values, outcomes.
- Short note on what is worth bringing to the MCTDH-numerics collaborator (bounded MCTDH scenario) and to the open-systems collaborator (non-Markovianity witness question).

---

## 7. Scope limits (Guardian restraint)

Explicitly *not* in this voyage:

- Ultrastrong-coupling sweep (fixed $g/\omega = 0.1$)
- Coupling-strength noise (fixed $g_k$)
- Axial mode structure
- Realistic technical noise budget beyond trap-frequency drift
- Decoherence channels (closed-system dynamics throughout)
- Beyond-Lamb–Dicke corrections
- MCTDH comparison (exact propagation only; MCTDH is a parallel collaborator's domain)

Any of these can motivate a follow-up voyage. In this one, they stay fixed.

---

## 8. Failure modes and honest outcomes

| Mode | Interpretation |
|---|---|
| $n_{\text{eff}}$ and $\sigma^2_{\text{intrinsic}}$ grow on disjoint timescales | Theoretical complexity and measurement variance probe different things; framework needs revision |
| H1–H3 hold for $N=1$ but break at $N=2,3$ | Single-mode intuition fails under multi-mode spread; useful bound on applicability |
| Convergence failure at $n_{\max}=12$ | Exact-propagation proxy itself fails; reinforces need for MCTDH; tells us nothing about physics |
| 1% $\Delta$-noise too small to generate signal | Noise model insufficient; escalate to realistic ²⁵Mg⁺ levels |
| H3 holds cleanly | Bring to MCTDH-numerics collaborator (bounded MCTDH follow-up) and open-systems collaborator (non-Markovianity witness formalisation) |

All outcomes, including nulls, get recorded.

---

## 9. Deliverables

1. Propagation and analysis code (Python: numpy, scipy, qutip if available, else hand-rolled sparse).
2. Per-stage inspection figures (Stages 1–3, 5–7).
3. Synthesis figure (Stage 8): the H3 scatter plot.
4. One-page writeup: parameters, outcomes, next steps.
5. This document itself, version-controlled, as the voyage log.

---

## 10. Standing questions (to revisit before Stage 5)

*This section was patched on 2026-04-14 by the Harbourmaster reconciliation of the literature search (see `literature_search/reconciliation.md` §R3). Source legend: (C3) = Scout C3 pitfall; (P#) = Verifier Pn return; (HM) = Harbourmaster-derived.*

**Numerical and methodological pitfalls**

1. **Fock-truncation entropy ceiling.** $n_{\text{eff}}^{(k)} \leq n_{\max}^{(k)}$ exactly. Physical saturation must be truncation-independent: run $n_{\max}$ and $2 n_{\max}$, confirm agreement. (C3.1; already inscribed as H1 convergence — reaffirmed.)
2. **Mode-labelling ambiguity near degeneracy.** Report aggregate $\mathcal{C}(t) = \sum_k \log n_{\text{eff}}^{(k)}(t)$ as the primary invariant; per-mode curves only as decomposition. (C3.2)
3. **Early-time $t^2$ universal growth.** Subtract the short-time coefficient before reading saturation structure. (C3.3)
4. **Entropy is not complexity.** Inspect the eigenvalue spectrum of $\rho^{(k)}(t)$ directly in Stage 2; the "effective orbital count" reading requires a peaked spectrum. (C3.4)
5. **MCTDH-adjacent lessons without running MCTDH.** Near-degenerate populations jitter; false-saturation plateaus can break under factor-2 window extension; SPF-style convergence is not observable convergence. (C3.5)
6. **Normalisation drift.** Log $\|\psi(t)\|^2$ at every inspection point; reject runs above stated tolerance. (C3.6; already inscribed — reaffirmed.)
7. **Initial-state dependence.** Hold the initial state fixed across stages and document; the complexity curves are state-conditioned, not Hamiltonian-conditioned. (C3.7)
8. **Gauge convention for counter-rotating terms.** Gauge choice determines whether counter-rotating terms appear; fix and document the gauge before Stage 1 so that "no RWA" is unambiguous. (P1 / Stokes & Nazir 2019)
9. **Noise spectrum, not only variance.** Gaussian $\Delta$-noise captures stochastic jitter; coherent periodic contamination (60 Hz power-line coupling) is a distinct and documented regime. At least one Stage 3 cut should include a coherent-modulation component. (P4 / D9)
10. **Non-Markovianity formalism choice affects the quantitative witness.** BLP, RHP, QFI flow, coherent-information, and memory-kernel formalisms give different numerical signatures on the same dynamics. If Stage 8 invokes non-Markovianity, compute at least two formalisms on a sample trajectory for cross-check. (P5 / E1–E5)
11. **Canonical-measure applicability — unresolved divergence.** Scout reads canonical non-Markov measures as *under-applicable* in recurrent regimes; Verifier reads them as *well-defined and recurrence-sensitive*. Stage 3 should compute BLP trace-distance on a sample trajectory alongside $T_{\text{det}}(M)$ to test whose reading holds in this parameter regime. (HM, from reconciliation R2)
12. **Resonance-point accessibility (Stage 1 prep, 2026-04-14).** The §2.1 Hamiltonian with the voyage's $|\uparrow\rangle|0\rangle$ initial state has unbounded mode-amplitude growth at exactly $\Delta = 0$; no finite Fock budget saturates the numerical error. The current voyage probes the resonance *limit* via Cut A's innermost points at $|\Delta|/\omega_{\text{ref}} = 0.15$ (the closest approach at which a homogeneous $n_{\max}=12$ default meets the Stage-1 error target; see §2.5 convergence table), not the resonance *point*. Future voyages interested in on-resonance dynamics should consider (a) coherent-state initial conditions matched to one $\sigma_x$-branch (no runaway), (b) Krylov-propagator infrastructure allowing adaptive Fock cutoff at tighter detunings, or (c) explicit analytic limit-taking. The H3 claim in §5 is accordingly a limit-claim, not a point-claim. (HM, from Stage 1 prep; Guardian adjudication)

**Parameter and scoping questions (retained from v1)**

- Realistic ²⁵Mg⁺ trap-frequency drift level. Verifier P4 indicates active-feedback trapped-ion platforms reach $\sim 5 \times 10^{-6}$ short-term; clock-grade systems approach $\sim 10^{-18}$. The voyage's "1% RMS" assumption is therefore a **deliberate stress-test level**, not a realistic operating-point prediction. Reframe in Stage 3 writeup. (HM)
- Simulation window of $50 \, \omega_{\text{ref}}^{-1}$: does Stage 1 reveal the relevant dynamical timescales, or does the window need extending/contracting?
- Cut C commensurability configs: execute all three, or drop one if Cut A + B already settle H3?

---

*End of Stage 0 document. Ready for repo creation and Stage 1 kickoff.*
