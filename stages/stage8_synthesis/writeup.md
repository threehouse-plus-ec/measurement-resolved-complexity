# Voyage writeup — measurement-resolved complexity

**Endorsement Marker:** T(h)reehouse +EC voyage, Coastline layer. No external endorsement implied.

**Licence:** CC BY-SA 4.0 (see repository `LICENCE`).

**Voyage dates:** 2026-04-14 → 2026-04-15 (repo init → Stage 8 synthesis).
**Figure:** [`../../figures/stage8_synthesis.pdf`](../../figures/stage8_synthesis.pdf).
**Novelty statement:** [`novelty_statement.md`](novelty_statement.md).
**Collaborator notes:** [`collaborator_notes.md`](collaborator_notes.md).

---

## 1. Executive summary (three sentences)

The voyage hypothesised that an intrinsic complexity measure $\bar{\mathcal{C}}$ (aggregate reduced-state von Neumann entropy) and an operational scalar $f_{\text{resolved}}(M)$ (duty cycle of ensemble variance above quantum-projection-noise) would co-vary monotonically across a detuning sweep in a bounded spin + $N \in \{1, 2, 3\}$ mode system at intermediate coupling without RWA — a correlation that, if confirmed, would operationalise a cross-walk between theorist-visible entanglement and experimentalist-visible variance. The central hypothesis is **empirically falsified** (Stages 5, 6, 7): $\bar{\mathcal{C}}$ and $f_{\text{resolved}}$ have independent drivers (proximity to resonance versus beat-frequency-driven oscillation count) and do not correlate across the sweep. The voyage's positive finding — which emerged from the same data but was not predicted in advance — is that intrinsic and operational measures probe **complementary** dynamical moments, with $\mathcal{C}$-peaks at maximum entanglement and $\sigma^2$-peaks at maximum parameter sensitivity; per-mode growth-framing $r(\sigma^2, |\dot{\mathcal{C}}^{(k)}|) > 0$ holds consistently for the dominantly-coupled mode across $N = 1, 2, 3$ and settles the empirical H2 claim at the per-mode rather than aggregate level.

## 2. Parameters (final, locked at v0.2 + PA-05)

| Parameter | Value |
|---|---|
| Coupling $g/\omega_{\text{ref}}$ | 0.1 (all modes, fixed) |
| Detuning range (Cut A) | $\{-0.5, -0.3, -0.15, +0.15, +0.3, +0.5\}$ |
| Cut B configurations | $(+0.15, +0.15)$, $(+0.15, +0.3)$, $(-0.15, +0.15)$, $(+0.15, +0.5)$ |
| Cut C configurations | C-Ra $(1, \varphi, \varphi^2)$; C-Rb $(1, \sqrt2, \sqrt3)$; C-Rc $(1, 5/3, 7/3)$ |
| Cut C detuning sweep | $D \in \{+0.15, +0.30\}$ (PA-05 reduced scope) |
| Gauge | Dipole-gauge, rotating frame at drive, $\sigma_z$ absent |
| Initial state | $|\uparrow\rangle \otimes |0\rangle^{\otimes N}$ |
| Simulation window | $t \in [0, 50\,\omega_{\text{ref}}^{-1}]$, 500 timesteps |
| Fock truncation | $n_{\max} = 12$ default (Cut A, Cut B); $n_{\max} = 10$ at Cut C (scope-reduced) |
| $\Delta$-noise | Gaussian, $\sigma_\Delta/\omega_{\text{ref}} = 0.01$ (stress test, not realistic operating point) |
| Ensemble size | $R = 100$ (Cut A, B); $R = 30$ (Cut C) |
| Shot budgets | $M \in \{100, 1000, 10^4\}$ |
| Reproducibility | `np.random.SeedSequence` spawn pattern per stage (`20260415`, `20260416`, `20260417`) |

## 3. Hypotheses — what survived, what did not

| Hypothesis | v0.2 form (struck through if superseded by PA-05) | Empirical status |
|---|---|---|
| H1 | Both observables rise from $t = 0$ values | **Holds trivially** (Stages 1–7). Not a real test. |
| H2 (aggregate growth-framing) | ~~$r(\sigma^2, \|\dot{\mathcal{C}}\|) > 0$ across sweep~~ | **Breaks at $N \geq 2$ in asymmetric configs, fully at $N = 3$** (Stages 6 B4, 7 Cut C). |
| H2 (per-mode, PA-05 replacement) | $r(\sigma^2, \|\dot{\mathcal{C}}^{(k)}\|) > 0$ for dominantly-coupled mode $k$ | **Holds at $N = 1, 2, 3$**; $r_{\text{mode 1}} \in [+0.18, +0.55]$ across 16 data points (Stages 4–7). |
| H3 (scalar correlation) | ~~$f_{\text{resolved}}(M) \propto \bar{\mathcal{C}}$ across sweep~~ | **Empirically falsified** across Stages 5, 6, 7. Non-monotone with beat-frequency mechanism. |
| H3 (complementarity, PA-05 replacement) | $\mathcal{C}$ and $\sigma^2$ probe conjugate dynamical moments; their cross-walk is the empirical content | **Structurally confirmed** (Stages 4–7). Quantitative $\mathcal{C}\cdot\sigma^2$ uncertainty-relation test **null** at Stage 7. |

## 4. Physics findings (positive)

### 4.1 Per-mode complementarity (four-stage convergent)

- At each mode $k$, $\mathcal{C}^{(k)}(t) = \log n_{\text{eff}}^{(k)}(t)$ peaks when the single-mode reduced state is maximally mixed — the spin-reduced state sits near $p \approx 1/2$ at the same moments.
- $\sigma^2_{\text{intrinsic}}(t) \approx (\partial_\Delta p)^2 \sigma_\Delta^2$ (at leading order in small noise, at outer detunings) peaks when $(\partial_\Delta p)^2$ is large, which occurs at state-transition moments where $p$ is near 0 or 1 — i.e. at minimum entanglement.
- Peaks of $|\dot{\mathcal{C}}^{(k)}|$ (rapid-growth moments) align temporally with peaks of $\sigma^2_{\text{intrinsic}}$ when mode $k$ is the dominantly-coupled one; series-direct $r(\sigma^2, \mathcal{C})$ is consistently negative ($-0.78$ to $-0.39$) capturing the phase offset between entanglement-peak and sensitivity-peak.
- The aggregate $\mathcal{C}$ dilutes when modes contribute asymmetrically (Stage 6 B4, Stage 7 Cut C) because weakly-coupled modes contribute uncorrelated variance to $|\dot{\mathcal{C}}|$; the per-mode signal survives the dilution.

### 4.2 QFI-reduction regime boundary (physics finding)

The first-order Fisher-information reduction $\sigma^2_{\text{intrinsic}} \approx (\partial_\Delta p)^2 \sigma_\Delta^2$ holds at outer single-mode detunings (10% relative deviation at $|\Delta| = 0.5$; 13% at $|\Delta| = 0.3$) and breaks approaching resonance and under multi-mode coupling (22% at single-mode $|\Delta| = 0.15$; 13–30% across all $N = 2$ Cut B configurations). The crossover maps a regime boundary in parameter space: where the first-order Fisher linearisation suffices, the voyage's operational witness is equivalent to a QFI-flow-style non-Markovianity witness; where the linearisation breaks, the operational witness carries independent information.

### 4.3 $n_{\text{eff}}^{(k)}$ is a literal effective-orbital count, not a rhetorical scalar

IPR · $n_{\text{eff}} \in [1.00, 1.14]$ at the $\mathcal{C}$-peak timepoint across all Cut B and Cut C configurations (Stages 6, 7). The reduced-state eigenvalue spectrum is close to uniform-on-$n_{\text{eff}}$-modes. Scout's C3.4 semantic-overclaim concern is licensed to not bite at $N = 1, 2, 3$ in the tested coupling regime.

### 4.4 BLP trace distance is recurrence-sensitive and well-defined

Stage 3 confirmed BLP trace distance on an antipodal initial-state pair shows 2 sign changes in $\dot D(t)$ and $N_{\text{BLP}} = 0.97$. Scout's R2 "canonical measures under-applicable" claim is settled in Verifier's favour at this parameter point.

## 5. Null results (honest, not hedged)

- **H3 scalar correlation (Stages 5, 6, 7).** $\bar{\mathcal{C}}$ and $f_{\text{resolved}}$ have independent drivers; no monotone trend across any of Cut A, B, C. The beat-frequency mechanism is clean and reproducible.
- **Commensurability separation (Stage 7).** Golden ($\varphi$), $\sqrt2/\sqrt3$ irrational, and rational 3:5:7 configurations do not cleanly separate on any aggregate scalar in the tested scope. No Ordinans-adjacent ordering signature emerges. The voyage plan invited this question; the answer at this scope is null.
- **$\mathcal{C}\cdot\sigma^2$ uncertainty relation (Stage 7).** Product peak varies 5× across configurations at $D = 0.15$ with no universal lower bound. Complementarity stays structural-descriptive, not inequality-bounded.

## 6. Staging and gate record

All gates passed; all convergence checks passed.

| Stage | Purpose | Commit | Gates |
|---|---|---|---|
| 0 | Repo init, parameter lock | `cf00d15` | — |
| 1 | Propagator validated (Gaussian anchor + JC sanity) | `e3bb8ad` | 3/3 at $10^{-9}$–$10^{-15}$ |
| 2 | $n_{\text{eff}}$ observable layer | `1008eee` | 4/4 at $10^{-6}$–$10^{-15}$ |
| 3 | Ensemble + QPN + QFI/BLP cross-checks | `cc1bf5e` | 4/4; R2 resolved in Verifier's favour |
| 4 | H2 checkpoint | `1e8d4a0` | Growth-framing visible; full-H2 deferred to $N \geq 2$ |
| 5 | Cut A (6-point detuning sweep) | `214ec62` | Gate 11 PASS; QFI crossover confirmed |
| 6 | Cut B (4 $N=2$ configs) | `b71bf2a` | Gates 11/12/13 PASS; complementarity finding |
| 7 | Cut C (3 $N=3$ commensurability configs) | `df08746` | Convergence PASS; per-mode H2; commensurability null |
| 8 | Synthesis | this commit | — |

PA-05 committed between Stages 7 and 8 (`ecbf754`); plan at v0.2 + PA-05.

## 7. Deferred items (follow-up voyages)

- Krylov / spread-complexity identity for $n_{\text{eff}}^{(k)}$ — TASK_CARD v3.
- On-resonance dynamics with alternative initial states (coherent-state matched to $\sigma_x$-branch) — inaccessible with this voyage's $|\uparrow\rangle|0\rangle$.
- Coupling-strength sweep beyond $g/\omega = 0.1$.
- Coherent-modulation $\Delta$-noise (AC-line analogue) — Standing item 9 unexercised.
- Full BLP pair optimisation for quantitative $\mathcal{N}_{\text{BLP}}$.
- Direct QFI-reduction measurement at $N = 3$ (Stage 7 oversight; extrapolation from $N = 2$ remains in the record).
- Krylov-propagator infrastructure for $N \geq 3$ at $n_{\max} \geq 12$ without 30-hour runtime.

## 8. Verdict

The voyage's empirical content is: **(a)** a cleanly-demonstrated per-mode complementarity structure between intrinsic and operational complexity measures, robust across $N = 1, 2, 3$; **(b)** a physics-regime boundary delineating where the first-order Fisher-information reduction of the operational witness holds; **(c)** an honest null on the original H3 scalar-correlation hypothesis; **(d)** a honest null on commensurability separation at the tested scope.

This is sufficient to bring to collaborators (see [`collaborator_notes.md`](collaborator_notes.md)). It is not sufficient for a publication claim on its own; the follow-up voyage at wider scope and with a quantitative complementarity bound would be needed for that.
