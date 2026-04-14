# Literature Reconciliation — 2026-04-14

**Endorsement Marker:** T(h)reehouse +EC voyage, Coastline layer. No external endorsement implied.

**Licence:** CC BY-SA 4.0 (see repository `LICENCE`).

**Role:** Harbourmaster. Oxford British English. Adjudicative, not generative.
**Upstream:** [`perplexity_return.md`](perplexity_return.md) (Verifier, 2026-04-14); [`claude_return.md`](claude_return.md) (Scout, 2026-04-14).
**Task card:** [`HARBOURMASTER_TASK.md`](HARBOURMASTER_TASK.md) (2026-04-14).
**Voyage task card this reconciles:** [`TASK_CARD.md`](TASK_CARD.md) v2 (same folder).

## Summary (≤ 3 sentences)

Both upstream agents independently locate the voyage's candidate unoccupied ground at the operational recombination — the three-way cross-walk of single-mode reduced-state entropy, ensemble-variance sensitivity, and quantum-projection-noise-floor thresholding in a bounded spin + few-mode bosonic system at intermediate coupling without RWA. No direct precedent for the full construct is surfaced in P1–P3, and no single-element novelty survives scrutiny. One substantive divergence remains unresolved (canonical non-Markovianity measures: under-applicable per Scout, well-defined per Verifier) and is forwarded as a Standing Question rather than adjudicated here.

---

## R1 — Citation cross-check

### Verifier → Scout-community map

| Verifier citation | Scout C1 community | Anticipated by Scout? |
|---|---|---|
| A1 Kockum (2019) — USC circuit-QED | Trapped-ion simulation (Hamiltonian-adjacent) / Open systems | Partially — Scout flagged Porras-Cirac-Solano lineage, not Kockum directly |
| A2 De Liberato (2013) — deep-USC polariton | Many-body (polariton self-interaction) | No — deep-USC is outside voyage regime, mentioned for methodology only |
| A3 Braak (2011) — analytic Rabi diagonalisation | Many-body / Quantum chaos (spectral methods) | Implicit — Scout named "Rabi model" as Hamiltonian reference |
| A4 Wang et al. (2019) — spin-boson MPS w/wo RWA | Many-body / Open systems | Yes — aligned with Scout's quench / entropy-growth references |
| A5 Cárdenas et al. (2015) — circuit-QED non-Markovian exact | Open quantum systems | Yes — direct near-neighbour for $T_{\text{det}}$ logic |
| A6 Stokes & Nazir (2019) — gauge ambiguities USC | (Scout did not allocate) | **No — surfaces a pitfall Scout missed** (see R3 item 8) |
| A7 Di Stefano et al. (2017) — Feynman diagrams USC | Many-body / diagrammatic | No — tangential to voyage; methodological only |
| A8 Solano et al. — generalised Rabi extensions | Trapped-ion / Many-body | Yes — Scout named this lineage explicitly |
| B1 Alba & Calabrese (2018) — quench entanglement | Many-body dynamics | Yes — Scout named Calabrese-Cardy phenomenology |
| B2 BLP (2009–2010) | Open quantum systems | Yes — Scout named BLP in C1 and analysed in C2 |
| B3 Textbook von Neumann entropy | Many-body (background) | Yes — background |
| B4 Wu et al. (2020) — coherence-based non-Mark. | Open quantum systems | Partial — Scout named "coherence-based witnesses" genre |
| B5 Lu, Wang & Sun (2010) — QFI flow | Quantum metrology / Open systems | **Yes — Scout predicted QFI connection in C2** |
| C1' Döring et al. (2010) — QPN interferometry | Quantum metrology | Yes — Scout named QPN-as-floor logic |
| C2' Brewer et al. (2019) — Al/Mg clock | Quantum metrology / Trapped-ion | Yes — Scout named metrological QPN in trapped-ion context |
| C3' Tserkis et al. (2022) — backflow/teleportation | Open quantum systems | Yes — Scout expected near-neighbours here |
| C4' Cárdenas et al. (2015) — repeated | Open systems | Yes |
| C5' Lakshmi Pooja et al. (2024) — QSL with coherence | (Scout did not allocate) | No — tangential, no action |
| C6' Breuer/Hall/Cresser canonical reviews | Open systems | Yes — Scout named "BLP / RHP / QFI-based" families |
| D1–D9 trap-frequency stability corpus | Trapped-ion simulation | Yes, with one pitfall extension — **D9 (60 Hz power-line coupling) was not anticipated** (see R3 item 9) |
| E1 BLP / E2 RHP / E3 QFI / E4 Coherent-info | Open quantum systems | Yes — Scout named all four explicitly |
| E5 Memory-kernel / time-local approaches | (Scout did not allocate) | **No — alternative non-Markov formalism Scout missed** (see R3 item 10) |

### Discrepancies

**(i) Verifier citations Scout did not anticipate:**
- **A6 Stokes & Nazir — gauge ambiguities in USC.** Surfaces a genuine methodological pitfall (see R3 item 8).
- **D9 — 60 Hz power-line coupling** as a *coherent* noise contribution on top of stochastic jitter. Bears on the voyage's Gaussian-$\Delta$-noise ensemble model (see R3 item 9).
- **E5 — memory-kernel / time-local formalism.** An alternative non-Markov framework Scout's C1/C2 did not canvass (see R3 item 10).
- **A7, C5'** — tangential to the voyage's construct; no action required.

**(ii) Scout communities Verifier returned no citations for:**
- **Quantum chaos proper** (OTOCs, spectral form factor, **Krylov / spread complexity**). Scout flagged the Krylov-complexity ↔ single-mode reduced-entropy mapping as a potential second identity for the voyage's intrinsic measure and explicitly marked it for reconciliation check. Verifier's P2 returns no citations in this lineage. Two readings are possible: (a) the mapping is not made in published literature, supporting Scout's "apparent gap" flag; (b) Verifier's P2 phrasing around reduced-state-entropy terminology missed the Krylov-complexity idiom. **This is a task-card scope issue; see R6.**
- **Trapped-ion-specific time-resolved multimode exact propagation at $g/\omega = 0.1$ without RWA.** Both agents converge: Verifier explicitly flags NOT FOUND in P1; Scout anticipated this as where the voyage's parameter-specificity lives. Convergent gap.

---

## R2 — Gap convergence

**Convergent gap (strong):** both agents independently point to the **three-way operational cross-walk** as the candidate unoccupied ground. Scout (C1 closing, C5 draft): "the three-way conjunction as an analysis methodology … may be without direct precedent." Verifier (P3 outcome; overall conclusion): "operative construction appears genuinely novel … constituent elements individually well-established … synthesis is novel and methodologically justified." Both also converge on the parameter-specific gap (trapped-ion-accessible multimode at $g/\omega = 0.1$, no RWA, time-resolved) being absent.

**Substantive divergence (one, unresolved):** on the applicability of canonical non-Markovianity measures in bounded environments with recurrence structure.
- **Scout C1/C5:** "canonical non-Markovianity measures are under-applicable due to the bounded environment's recurrence structure," used as part of the justification for the voyage's own operational witness.
- **Verifier P5:** all five canonical measures (BLP, RHP, QFI flow, coherent-information, memory-kernel) are *well-defined* in bounded environments; BLP and RHP detect recurrence naturally; coherent-information is particularly suited to unitary closed-system regimes and is the Verifier's recommended primary measure.

The divergence matters because Scout's "under-applicability" argument is load-bearing for the novelty claim. Verifier's P5 removes that rhetorical support: canonical measures *are* applicable; the voyage's $T_{\text{det}}(M)$ is an *alternative operational witness*, not a replacement for unavailable tools. This does not refute the operational-crosswalk novelty, but it contracts Scout's C5 language. **The reconciliation does not resolve this unilaterally; it is recorded as a Standing Question and propagated into §10 of VOYAGE_PLAN.**

**Divergence on novelty temperature:** Verifier is more forward-leaning ("genuinely novel", "synthesis is novel and methodologically justified"). Scout is more restrained ("may be without direct precedent … pending Perplexity", with explicit contraction conditions). Harbourmaster aligns with Scout's register — the task-card's interpretive-caution clause (R4) weighs against Verifier's assertive language.

**No-gap outcome (third possibility from §4.R2) is not triggered.** Both maps jointly describe a near-neighbour region with a specific recombination the voyage contributes.

---

## R3 — Pitfall integration (patch to VOYAGE_PLAN §10)

This section *supersedes and extends* VOYAGE_PLAN.md §10 Standing Questions. The patch is applied in the same commit as this reconciliation document.

**Source legend:** (C3) = Scout C3 pitfall; (P#) = Verifier Pn return; (HM) = Harbourmaster-derived from the reconciliation itself.

1. **Fock-truncation entropy ceiling.** $n_{\text{eff}}^{(k)} \leq n_{\max}^{(k)}$ exactly; saturation near the truncation bound reports the grid, not the physics. Run $n_{\max}$ and $2 n_{\max}$; physical saturation is truncation-independent. *(C3.1; already in voyage plan as H1 convergence check — reaffirmed here.)*
2. **Mode-labelling ambiguity near degeneracy.** Per-mode $n_{\text{eff}}^{(k)}$ curves can rotate between near-degenerate modes under symplectic reshuffling. Report aggregate $\mathcal{C}(t) = \sum_k \log n_{\text{eff}}^{(k)}(t)$ as the primary invariant. *(C3.2)*
3. **Early-time $t^2$ growth masks informative signal.** Subtract the universal short-time coefficient before reading saturation structure. *(C3.3)*
4. **Entropy is not complexity (semantic overclaim).** Inspect the eigenvalue spectrum of $\rho^{(k)}(t)$ directly in Stage 2; the "effective orbital count" reading requires a peaked spectrum, which is a stronger claim than entropy alone licenses. *(C3.4)*
5. **MCTDH-adjacent lessons (even without running MCTDH).** Near-degenerate populations yield numerically jittery $n_{\text{eff}}$; false-saturation plateaus can break under factor-2 window extension; SPF-style convergence ≠ observable convergence. *(C3.5)*
6. **Normalisation drift at long times.** Log $\|\psi(t)\|^2$; reject runs above stated tolerance. *(C3.6; already in voyage plan — reaffirmed.)*
7. **Initial-state dependence of the complexity curve.** The detuning-sweep curves are state-conditioned, not Hamiltonian-conditioned; hold initial state fixed across stages and document. *(C3.7)*
8. **[NEW] Gauge convention for counter-rotating terms.** Stokes & Nazir demonstrate that gauge choice (Coulomb vs. dipole) determines whether counter-rotating terms appear in the Hamiltonian, with different physical predictions. The voyage must fix and document its gauge convention before Stage 1 so that "no RWA" is unambiguous. *(P1/A6)*
9. **[NEW] Noise spectrum, not only variance.** The voyage's Gaussian ensemble model over $\Delta$ captures stochastic jitter but not coherent periodic contamination (60 Hz power-line coupling; D9). At least one sensitivity cut should include a coherent-modulation component to test whether $T_{\text{det}}(M)$ is robust to non-Gaussian noise structure. *(P4/D9)*
10. **[NEW] Non-Markovianity formalism choice affects quantitative witness.** BLP trace-distance, RHP CP-divisibility, QFI flow, and coherent-information-based measures give different quantitative signatures on the same dynamics; memory-kernel / time-local formalism is a further alternative. If the voyage invokes non-Markovianity language in Stage 8, compute at least two formalisms on a sample trajectory to cross-check. *(P5/E1–E5)*
11. **[NEW] Canonical-measure applicability divergence (R2).** Scout's "canonical measures are under-applicable in recurrent regimes" and Verifier's "canonical measures are well-defined, BLP/RHP detect recurrence naturally" are in tension. Stage 3 should compute BLP trace-distance on a sample trajectory alongside $T_{\text{det}}(M)$ to test whose reading holds in this parameter regime. *(HM, from R2 divergence)*

**Items in the previous §10 retained verbatim** (not superseded, reasserted):

- Realistic ²⁵Mg⁺ trap-frequency drift level: 1% RMS defensibility — Verifier P4 indicates active-feedback trapped-ion platforms reach $\sim 5 \times 10^{-6}$ short-term and $\sim 10^{-18}$ in clock-grade systems. The voyage's "1% RMS" is therefore a *pessimistic stress-test level*, not a realistic prediction. Reframe this in Stage 3 accordingly.
- Simulation window of $50\,\omega_{\text{ref}}^{-1}$: defer to Stage 1 findings.
- Cut C commensurability: defer to Stage 6 findings.

---

## R4 — Interpretive caution reaffirmed

**Non-negotiable principle (from HARBOURMASTER_TASK.md §4.R4):** *Absence of direct precedent in P2 or P3 does not by itself establish novelty.* The genuine novelty, if any, is at the operational-crosswalk level — linking reduced-state complexity, ensemble sensitivity, and finite-shot detectability in a bounded spin–boson setting.

**Scope of application in this reconciliation:**
- Verifier's P2 "NOT CANONICAL" and P3 "NOT FOUND / NO DIRECT PRECEDENT" readings are *not* read as novelty licences.
- Verifier's assertive conclusion language ("appears genuinely novel", "synthesis is novel and methodologically justified") is adjusted downward by this clause into the operational-recombination register used in R5.
- Where Scout and Verifier converge on a gap (R2 convergent gap), the clause still requires that the voyage's H3 correlation between $T_{\text{det}}(M)$ and saturation $\mathcal{C}$ be *empirically demonstrated* before any novelty claim is earned. Prior-art absence is necessary but not sufficient.

---

## R5 — Novelty statement (pre-Stage-8)

> **Calibrated novelty paragraph (Stage 8 backbone, pre-reconciliation with voyage results).**
>
> Three constructs frame the voyage and are each well-established in the literature: exact no-RWA propagation of a two-level system coupled to bosonic modes at intermediate to ultrastrong coupling [A1, A3, A5, A8]; the von Neumann entropy of a single-mode reduced state as a dynamical observable in many-body quench dynamics [B1] and as an information-theoretic primitive adjacent to non-Markov witnesses [B2, B4, B5]; and quantum projection noise as a metrological floor in trapped-ion measurements [C1', C2']. What the voyage recombines, and what has not been recombined in this specific parameter regime, is the *three-way cross-walk*: $n_{\text{eff}}^{(k)}(t)$ derived from the single-mode reduced state, ensemble variance $\sigma^2_{\text{intrinsic}}(t)$ under controlled parameter noise, and quantum projection noise $\sigma^2_{\text{QPN}}(t; M)$ as a detectability floor, combined in a bounded spin + 1–3 radial-mode bosonic system at $g/\omega = 0.1$ with counter-rotating terms retained. The voyage's empirical content reduces to a single testable claim: whether the detectability horizon $T_{\text{det}}(M)$ and the saturation of the aggregate complexity $\mathcal{C}(t) = \sum_k \log n_{\text{eff}}^{(k)}(t)$ are correlated across the detuning sweep $\Delta/\omega \in [-0.5, +0.5]$. This is neither a new observable nor new physics; it is a specific operational crosswalk connecting theorist-visible intrinsic complexity to experimentalist-visible variance-above-noise in a trapped-ion-accessible regime.

Word count: 198.

### Reduction-path note

This paragraph contracts under any of the following findings during Stage 1–8 or at a future literature pass:

- **Single-element precedent for the full crosswalk.** If a study surfaces that combines $n_{\text{eff}}$-style reduced-state complexity, ensemble-variance sensitivity, and QPN thresholding on any spin-boson class (not only trapped-ion): the claim contracts to "a trapped-ion-specific implementation of [cited] construction at $g/\omega = 0.1$ with no RWA." This is the strongest single contraction condition.
- **Krylov-complexity mapping.** If a reconciliation pass against the quantum-chaos literature (currently outside Verifier's P2 return) establishes that $n_{\text{eff}}^{(k)}$ has a direct identity as a spread-complexity object in spin-boson systems: the "dynamical complexity proxy" component is fully precedented and the novelty rests on (ii)+(iii)+operational anchoring only.
- **Reduction of $T_{\text{det}}(M)$ to QFI-flow non-Markovianity.** Scout's C2 candidate reduction (small-noise limit, Fisher-information-vs-QPN threshold) if confirmed numerically in Stage 3 against E3 / B5 canonical QFI-flow measure: the claim contracts to "a measurement-budget-parametrised experimental proxy for [cited] QFI-flow witness."
- **Empirical disconfirmation of H3.** If $T_{\text{det}}(M)$ and $\mathcal{C}$-saturation do *not* track each other across the sweep: the operational crosswalk has no empirical content and the claim retracts to a methodological null result. This is the voyage-internal contraction path and is the Stage 4 go/no-go checkpoint.

---

## R6 — Archive notes

**Version stamps.**

| Document | Date stamped | Status |
|---|---|---|
| `perplexity_return.md` | 2026-04-14 | Verifier return complete; all P1–P5 substantively addressed |
| `claude_return.md` | 2026-04-14 | Scout return complete; all C1–C5 substantively addressed |
| `reconciliation.md` (this doc) | 2026-04-14 | Harbourmaster reconciliation; Standing Questions patched into VOYAGE_PLAN §10 |
| `HARBOURMASTER_TASK.md` | 2026-04-14 | Task card (Harbourmaster role) |
| `TASK_CARD.md` | v2, 2026-04-14 | Voyage literature-search task card |

**Commit intention:** all four returns plus the VOYAGE_PLAN §10 patch are committed together per HARBOURMASTER_TASK §4.R6.

**Task-card flaws exposed — flagged for v3, not silently patched:**

1. **TASK_CARD v2 P2 terminology scope is narrower than it should be.** P2 was phrased around reduced-state-entropy / subsystem-entropy terminology and explicitly de-prioritised MCTDH natural-orbital idiom. However, the *quantum-chaos* literature (Krylov / spread complexity, OTOC-based measures) uses yet another idiom again, and was not within P2's surface area. Scout flagged this in C1 ("worth a reconciliation check") and the reconciliation cannot close it from the current returns. **v3 fix:** add a P6 or expand P2 to include an explicit pass over the Krylov-complexity / spread-complexity / operator-growth literature with the question "has $n_{\text{eff}}^{(k)}(t)$ a direct identity as a spread-complexity object in bounded spin-boson systems?"
2. **TASK_CARD v2 P4 asked for stability but not noise *spectrum*.** Verifier's D9 (60 Hz power-line coupling) surfaced because of Verifier diligence, not because the task card requested it. Voyage noise modelling depends on spectral structure, not only RMS amplitude. **v3 fix:** rephrase P4 to request both RMS jitter (stochastic) and *coherent modulation sources* (AC-line, laser-intensity harmonics, thermal-cycle-coupled drifts).
3. **Minor bookkeeping.** Verifier labels Brewer et al. (2019) as both C2 under P3 and D1/D2 under P4. The content is consistent across both uses; the duplicate label system is not a flaw in the return but may confuse downstream citation extraction. **v3 fix:** adopt a single citation key per reference across all P-returns.

No R1–R5 finding requires a silent revision of v2; all flagged items route explicitly to v3.

---

## Standing items forwarded to Stage 8

1. **QFI-reduction of $T_{\text{det}}(M)$.** Stage 3 must compute the small-noise-limit Fisher-information criterion and compare to $T_{\text{det}}$ on the same trajectory ensemble. If they coincide, the operational-crosswalk novelty contracts along the third reduction path in R5.
2. **Canonical-measure applicability (R2 divergence).** Stage 3 should additionally compute BLP trace-distance on a sample trajectory. This tests Scout's "under-applicability" claim against Verifier's "well-defined" claim in the voyage's specific parameter regime.
3. **Krylov / spread-complexity identity.** Pending v3 task-card expansion (R6 item 1). Flagged here so that Stage 8 writeup does not inadvertently claim novelty on the intrinsic-complexity component before that check is done.
4. **Noise-spectrum sensitivity.** At least one Stage 3 cut should include a coherent-modulation noise component (per R3 item 9) to test $T_{\text{det}}(M)$ robustness beyond Gaussian-ensemble assumptions.
5. **Gauge convention.** Stage 1 must document its gauge choice before claiming "no RWA" unambiguously (per R3 item 8).
6. **1% RMS reframing.** The voyage's "1% RMS" detuning noise assumption sits several orders of magnitude above published trapped-ion active-feedback stability ($\sim 5 \times 10^{-6}$). Reframe as a *deliberate stress-test level* rather than a realistic operating-point prediction; document in the Stage 3 writeup.

---

*End of reconciliation. No Harbourmaster veto raised. Three items routed to v3 task card; six items forwarded to Stage 8.*
