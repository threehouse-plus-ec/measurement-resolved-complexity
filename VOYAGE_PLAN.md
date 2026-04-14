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

### 2.2 Reference units

$\omega_{\text{ref}}$ sets the frequency unit; all times in units of $\omega_{\text{ref}}^{-1}$. Dimensional mapping to ²⁵Mg⁺ radial-mode frequencies (MHz range) deferred to writeup.

### 2.3 Initial state

$|\Psi(0)\rangle = |\uparrow\rangle \otimes |0\rangle^{\otimes N}$ — spin excited, all modes in vacuum.

### 2.4 Locked parameter choices

| Parameter | Value | Rationale |
|---|---|---|
| Coupling $g_k / \omega_{\text{ref}}$ | $0.1$ (all modes, fixed) | Intermediate regime, approaching ultrastrong boundary; counter-rotating terms non-negligible |
| Detuning range (Cut A) | $\Delta / \omega_{\text{ref}} \in \{-0.5, -0.2, 0, +0.2, +0.5\}$ | Wider pedagogical range, 5 points |
| Mode type | Radial | Contribute more equally than axial (no COM hierarchy); detuning sweep samples symmetric coupling landscape |
| Fock truncation $n_{\max}$ | $12$ per mode (default); $18$ for on-resonance convergence check | See §2.5 |
| Noise model | Trap-frequency drift only — Gaussian noise on $\Delta_k$, 1% RMS | Dominant experimental noise source in ²⁵Mg⁺ setup |
| Coupling noise | None (fixed $g_k$) | Simplifies noise structure; follow-up voyage can relax |
| Ensemble size $R$ | 100 trajectories per parameter point | Balance statistical power vs. compute |
| Shot budgets $M$ | $\{100, 1000, 10\,000\}$ | Spans realistic experimental range |
| Simulation window | $t \in [0, 50 \, \omega_{\text{ref}}^{-1}]$ | Long enough for several Rabi-scale oscillations; adjust after Stage 1 |
| Output timesteps | 500 points, uniform | Smooth plots; negligible cost |

### 2.5 Fock truncation justification

At $g/\omega = 0.1$, on-resonance ($\Delta = 0$) vacuum-Rabi dynamics populates Fock states up to $n \sim 5$–$8$ at coherent-excursion peaks. Counter-rotating terms (no RWA) can push further. $n_{\max} = 12$ gives a safety margin of ~4 levels above expected population; $n_{\max} = 18$ convergence check in Stage 1 confirms this is sufficient.

Hilbert-space dimensions:
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
- **H3 (strong, Ordinans-native):** as detuning is swept through resonance ($\Delta \to 0$), both $T_{\text{det}}(M)$ and the saturation value of $\mathcal{C}(t)$ scale in a correlated way. Off-resonant: short $T_{\text{det}}$, low $\mathcal{C}$. Near-resonant: long $T_{\text{det}}$, high $\mathcal{C}$.

**H3 is the voyage's real target.** H1 is sanity, H2 is suggestive, H3 is the signature worth bringing to the MCTDH-numerics and open-systems collaborators.

---

## 6. Staged execution

Each stage produces an inspectable artifact; no stage begins without sign-off on the previous one.

### Stage 1 — Single-mode propagator

Minimal $N=1$ propagation engine. Verify against Jaynes–Cummings analytics at $\Delta=0, g/\omega = 0.1$ (vacuum Rabi oscillations at frequency $2g$ with counter-rotating corrections). Run convergence check: $n_{\max} = 12$ vs. $18$ on the on-resonance case, confirm $p(t)$ agreement to $\sim 10^{-4}$.

**Artifact:** single figure showing $p(t)$ for the on-resonance case, overlaid with the $n_{\max}$ convergence comparison.

**Go/no-go:** propagator validated against known limit.

### Stage 2 — Observables layer

Add natural-occupation diagonalisation and $n_{\text{eff}}(t)$ computation on the Stage 1 run. Verify $n_{\text{eff}}(0) = 1$ and monotonic early-time growth.

**Artifact:** two-panel figure: $p(t)$ above, $n_{\text{eff}}(t)$ below, same axis.

**Go/no-go:** complexity measure behaves sensibly.

### Stage 3 — Ensemble and QPN layer

Add the 100-realisation ensemble with $\Delta$-noise, compute $\sigma^2_{\text{intrinsic}}(t)$, compare to $\sigma^2_{\text{QPN}}(t; M)$ for three $M$ values. Still $N=1$, still on-resonance only.

**Artifact:** three-panel figure showing $p(t)$, $n_{\text{eff}}(t)$, and $\sigma^2_{\text{intrinsic}}(t)$ vs. $\sigma^2_{\text{QPN}}(t; M)$ curves for $M \in \{100, 1000, 10^4\}$.

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

- Realistic ²⁵Mg⁺ trap-frequency drift level: is 1% RMS defensible, or should this be calibrated against local experimental measurements?
- Simulation window of $50 \, \omega_{\text{ref}}^{-1}$: does Stage 1 reveal the relevant dynamical timescales, or does the window need extending/contracting?
- Cut C commensurability configs: execute all three, or drop one if Cut A + B already settle H3?

---

*End of Stage 0 document. Ready for repo creation and Stage 1 kickoff.*
