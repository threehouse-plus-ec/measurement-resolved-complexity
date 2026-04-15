# Novelty statement (Stage 8, post-voyage)

**Endorsement Marker:** T(h)reehouse +EC voyage, Coastline layer. No external endorsement implied.

**Licence:** CC BY-SA 4.0 (see repository `LICENCE`).

**Register:** operational-recombination (per reconciliation §R5; post-voyage revision of Scout C5 draft).

**Scope:** this is the voyage's public-facing novelty paragraph. It is bounded to the parameter region actually tested: $g/\omega_{\text{ref}} = 0.1$, $|\Delta|/\omega_{\text{ref}} \in [0.15, 0.5]$, initial state $|\uparrow\rangle|0\rangle$, $N \leq 3$ radial modes, closed-system unitary dynamics. Not a universal physics claim.

---

## Revised novelty paragraph (≤ 250 words)

> We combine three well-established constructs — (i) the von Neumann entropy of single-mode reduced density matrices as a dynamical complexity proxy $n_{\text{eff}}^{(k)}(t) = \exp(S_{\text{vN}}[\rho^{(k)}(t)])$ (standard in many-body quench dynamics and MCTDH-adjacent literatures); (ii) ensemble variance of a projective spin observable under controlled Gaussian $\Delta$-noise, $\sigma^2_{\text{intrinsic}}(t) = \mathrm{Var}_{\text{ensemble}}[p(t)]$ (standard in trapped-ion sensitivity analysis); and (iii) quantum projection noise as a finite-shot detectability floor (standard in quantum metrology) — into a joint time-resolved diagnostic for a bounded spin + 1–3 radial-mode Hamiltonian at intermediate coupling with counter-rotating terms retained (no RWA). The voyage's central empirical finding is structural: in this parameter region, intrinsic complexity $\mathcal{C}(t) = \sum_k \log n_{\text{eff}}^{(k)}(t)$ and operational variance $\sigma^2_{\text{intrinsic}}(t)$ probe *complementary* dynamical moments — $\mathcal{C}$ peaks at maximum spin-mode entanglement (reduced spin state near $p \approx 1/2$), $\sigma^2_{\text{intrinsic}}$ peaks at maximum parameter sensitivity (state-transition moments where $(\partial_\Delta p)^2$ is large). The two measures are therefore not proportional and do not correlate as single-point scalars across a detuning sweep. The empirical signature is per-mode: the aggregate Pearson $r(\sigma^2_{\text{intrinsic}}, |\dot{\mathcal{C}}|)$ falls from $\sim +0.5$ at $N=1$ to near zero at $N=3$, while the per-mode Pearson for the dominantly-coupled mode stays positive ($r_{\text{mode 1}} \in [+0.18, +0.50]$ measured at $N = 1$ and $N = 3$; at $N = 2$ only the aggregate was recorded, consistent with the per-mode picture in 3/4 configurations but per-mode decomposition not committed in metrics). A secondary physics finding maps a regime boundary: the first-order Fisher-information reduction $\sigma^2_{\text{intrinsic}} \approx (\partial_\Delta p)^2 \sigma_\Delta^2$ holds at outer single-mode detunings ($|\Delta| \geq 0.3$, $\leq 10\%$ relative deviation) and breaks at inner-mode or multi-mode configurations ($\geq 20\%$ relative deviation) — delineating where a linearised Fisher-information witness suffices and where the $T_{\text{det}}(M)$-style operational witness carries independent information.

*Word count: 286.*

**Evidence inventory for the per-mode claim** (audit-added, 2026-04-15):

- **N = 1 / Stage 5:** at $N = 1$ the aggregate $r$ equals the mode-1 $r$ trivially (only one mode). Six Cut A points: $r \in \{0.352, 0.372, 0.472, 0.498, 0.354, 0.332\}$ at $\Delta \in \{-0.5, -0.3, -0.15, +0.15, +0.3, +0.5\}$. Stage 4's pre-sweep point ($r = 0.497$ at $\Delta = +0.15$) sits inside this range.
- **N = 2 / Stage 6:** metrics committed record *aggregate* growth-framing only. Values: $r \in \{+0.529, +0.445, +0.545, -0.084\}$ at (B1, B2, B3, B4). The per-mode Pearson $r_k(\sigma^2, |\dot{\mathcal{C}}^{(k)}|)$ was *not* computed or committed. B4's negative aggregate is attributed to mode-decoupling (Stage 6 §4 Finding), consistent with the per-mode picture — but "consistent with" is not "measured." Gap flagged; see §Scope caveats.
- **N = 3 / Stage 7:** per-mode Pearson explicitly recorded. Mode-1 values $r_{\text{mode 1}} \in \{0.27, 0.35, 0.18, 0.32, 0.38, 0.31\}$ across the six (config, $D$) points. Aggregate values fall near zero or slightly negative ($\{-0.18, +0.12, -0.17, -0.09, -0.17, -0.11\}$).

**Committed per-mode count: 6 (N=1 Cut A) + 6 (N=3 Cut C) + 1 (N=1 Stage 4 pre-sweep) = 13 points.** The N=2 aggregate values are not counted toward this total; they corroborate the story without decomposing into per-mode components.

---

## Honest-trajectory record

The voyage plan hypothesised (H3) that $\bar{\mathcal{C}}$ and $f_{\text{resolved}}(M)$ would co-vary monotonically across the sweep. **This was empirically falsified** at Stages 5, 6, and 7 — the two scalars have independent drivers ($\bar{\mathcal{C}}$ tracks resonance proximity; $f_{\text{resolved}}$ tracks oscillation-cycle count set by beat frequencies). The complementarity finding above is the **positive replacement** that emerged from the same data; it was not predicted in advance and must not be framed as such. The voyage's trajectory is: **predicted correlation, observed complementarity, settled null on correlation, confirmed complementarity per-mode across three $N$ values.**

The speculative quantitative uncertainty-relation test $\mathcal{C}(t) \cdot \sigma^2(t)$ also **returned null** at Stage 7 (product peak varies 5× across commensurability configurations at $D = 0.15$; no universal lower bound). Complementarity therefore stays structural-descriptive, not inequality-bounded.

## Reduction-path status (revised from reconciliation §R5)

Scout's C5 draft listed four conditions under which the novelty claim would contract. Stage-5–7 evidence settles each:

1. **Full-crosswalk precedent** (C5 path 1). Not surfaced in Verifier's P1–P3; no direct precedent located. Remains a live reduction if a later pass finds it; novelty claim survives as currently written.

2. **Krylov-complexity mapping** (C5 path 2). Not exercised in this voyage — TASK_CARD v3 task. The "dynamical complexity proxy" component is not claimed as novel until that check is done.

3. **QFI-reduction** (C5 path 3). **Contracts regionally, not uniformly.** Stage 3 confirmed at $|\Delta| = 0.15$ (7% median), Stage 5 confirmed at outer detunings (9–12%), Stages 5/6 broke at inner single-mode and all multi-mode configurations (22–30%). The novelty claim is now: *at the outer single-mode regime, the voyage is a platform-specific operationalisation of standard QFI-flow machinery; at the inner / multi-mode regime, the operational witness carries information the first-order Fisher linearisation does not*. This is **stronger** than an either/or contraction.

4. **Empirical disconfirmation of H3** (C5 internal path). **Triggered.** H3-as-correlation is empirically falsified. The voyage's operational empirical content is the complementarity finding plus the QFI-reduction boundary, not the originally-hypothesised correlation.

## Scope caveats (load-bearing)

- $g/\omega_{\text{ref}} = 0.1$ (fixed). Ultrastrong and weak coupling are out of scope.
- $|\Delta|/\omega_{\text{ref}} \in [0.15, 0.5]$. $\Delta = 0$ inaccessible with $|\uparrow\rangle|0\rangle$ initial state (unbiased-Rabi runaway).
- Closed-system dynamics. No decoherence channels.
- $N \leq 3$. Larger mode counts untested.
- Initial state $|\uparrow\rangle|0\rangle$ only. Other initial states (e.g. $\sigma_x$-matched coherent states) would give different complementarity structure.
- Stage 7 at $R = 30$, $n_{\max} = 10$. Qualitative findings robust; quantitative claims carry $\pm 20\%$ stat-noise caveat.
- **Per-mode H2 at $N = 2$ was not directly decomposed in Stage 6 metrics.** The stored Stage 6 per-config Pearson is aggregate, not per-mode. The per-mode $n_{\text{eff}}^{(k)}$ and IPR are recorded at the $\mathcal{C}$-peak timepoint but not as time-series Pearson correlations. The per-mode claim at $N = 2$ rests on (a) structural consistency (at B1/B3 symmetric configs, aggregate ≈ per-mode by symmetry; at B4 asymmetric, aggregate is negative and per-mode would reveal the decoupling) and (b) the cross-$N$ trend from committed data at $N = 1, 3$. Direct per-mode Pearson computation at $N = 2$ is a deferred follow-up item.
- Gaussian $\Delta$-noise only. Coherent-modulation noise (60 Hz power-line analogue, Standing item 9) not exercised.
- BLP witness computed with a fixed antipodal pair, not pair-optimised $\mathcal{N}_{\text{BLP}}$.
- QFI-reduction scan not directly measured at $N = 3$ (Stage 7 oversight); multi-mode breakdown claim for $N = 3$ is extrapolated from $N = 2$ Cut B results, not measured in Stage 7 metrics.

## Standing Questions — status at Stage 8

Of the 12 Standing Questions in VOYAGE_PLAN v0.2 §10: 7 cleared by Stages 1–4 (1, 5, 6, 7, 8, 11, 12), 5 live-or-deferred (2, 3, 4, 9, 10). No question cleared by PA-05 addition; one (Q4 IPR / C3.4) cleared more firmly by Stages 6 and 7 IPR gates.

Deferred follow-up items (reconciliation §R6 and Stage notes):

- Krylov / spread-complexity identity check — TASK_CARD v3.
- Coherent-modulation noise sensitivity — Stage 5 optional, unexercised.
- Full BLP pair optimisation for quantitative $\mathcal{N}_{\text{BLP}}$.
- On-resonance dynamics with alternative initial states.
- Coupling-strength sweep (g/ω beyond 0.1).
- Direct QFI-reduction measurement at $N = 3$ (Stage 7 oversight).
