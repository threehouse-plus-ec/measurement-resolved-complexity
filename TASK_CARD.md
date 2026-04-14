# Task Card — Background Literature Search (v2)

**Endorsement Marker:** T(h)reehouse +EC voyage task card — internal numerical exploration. Local candidate framework under T(h)reehouse +EC stewardship. No external endorsement implied.

**Licence:** Coastline layer, CC BY-SA 4.0 (see repository `LICENCE`).

**Voyage:** Measurement-Resolved Complexity (spin + few motional modes, detuning sweep)
**Issued:** 2026-04-14
**Revision:** v2, incorporating external review (terminology precision, expected-granularity framing, novelty calibration)
**Purpose:** Ground the voyage in prior work before Stage 8 synthesis. Identify prior art, calibrate novelty honestly, surface pitfalls the voyage should anticipate.

**Division of labour:**
- **Perplexity (Verifier stance):** citation precision, quantitative parameter values, field conventions. Returns sourced factual claims. *Finds prior art; does not adjudicate novelty.*
- **Claude (Scout stance):** conceptual bridges, cross-field synthesis, gap identification. Returns structured maps and open questions. *Maps the conceptual landscape; does not adjudicate novelty.*

Both deliver to a shared markdown stub. **Novelty adjudication is deferred to Harbourmaster reconciliation, not to either agent.**

---

## Shared context (both agents receive this)

A numerical exploration is being planned: a single spin coupled to 1–3 radial motional modes (trapped-ion context, ²⁵Mg⁺), intermediate coupling $g/\omega = 0.1$, detuning sweep $\Delta/\omega \in [-0.5, +0.5]$, closed-system exact propagation (no RWA, counter-rotating terms retained). Two complexity measures are compared time-resolved:

1. **$n_{\text{eff}}^{(k)}(t)$** — the exponential of the **von Neumann entropy of the single-mode reduced state** $\rho^{(k)}(t) = \text{Tr}_{\bar{k}} |\Psi(t)\rangle\langle\Psi(t)|$. This is *not* a generic MCTDH SPF population, *not* a chemistry-style natural-orbital occupation. It is specifically the entanglement-entropy-derived effective orbital count, $n_{\text{eff}}^{(k)}(t) = \exp\left(-\sum_j \lambda_j^{(k)}(t) \log \lambda_j^{(k)}(t)\right)$ where $\lambda_j^{(k)}$ are eigenvalues of $\rho^{(k)}$.

2. **$\sigma^2_{\text{intrinsic}}(t)$** — ensemble variance of spin population under shot-to-shot detuning noise.

These are thresholded against quantum projection noise $\sigma^2_{\text{QPN}}(t; M) = p(1-p)/M$ to define a **detectability horizon** $T_{\text{det}}(M)$: the time beyond which ongoing dynamics is buried below projection noise for shot budget $M$.

The central hypothesis is that $T_{\text{det}}(M)$ correlates with saturation of $n_{\text{eff}}$, i.e. that measurement-resolved complexity and intrinsic complexity track each other in this parameter regime.

---

## Perplexity task card (Verifier)

**Stance:** Precise. Sourced. Numerical where possible. Declines to speculate. **Returns prior art; does not decide what is novel.**

### P1 — Prior exact-diagonalisation studies of spin + few bosonic modes at intermediate/ultrastrong coupling

Find papers (≥ 2015) that do exact propagation of a two-level system coupled to 1–5 bosonic modes at $g/\omega \in [0.05, 0.5]$, *without* RWA, and report time-resolved observables. Key authors to probe: Solano, Ciuti, De Liberato, Nori, Kockum, Forn-Díaz.

**Scope boundary (explicit):** multimode cavity-QED and circuit-QED analogues *are in scope* — they share the underlying Hamiltonian structure. However, please flag which platform each result comes from (trapped-ion / cavity-QED / circuit-QED / molecular polaritons) so transferability can be assessed.

Deliver: citation list with (i) platform, (ii) coupling regime studied, (iii) number of modes, (iv) whether counter-rotating terms retained, (v) observables reported.

### P2 — Single-mode entanglement entropy as a dynamical observable

Has the **von Neumann entropy of the single-mode reduced density matrix** — or its exponential $n_{\text{eff}}^{(k)}$ — been used as a *time-resolved* diagnostic in spin-boson or Rabi-model contexts?

**Prioritise the entropy-of-reduced-state definition** over terminology. Search terms may include "single-mode entanglement entropy Rabi", "subsystem entropy dynamics spin-boson", "entanglement entropy quench bosonic mode", "Schmidt number time evolution". Do *not* restrict to "natural orbital" or "SPF population" phrasings — these belong to adjacent but distinct literatures (quantum chemistry, MCTDH benchmarking).

Deliver: citation list with object-of-study clearly identified, or gap-confirmation.

### P3 — Projection-noise or shot-noise floors as operational threshold for resolving late-time structure

Has projection-noise or shot-noise floor been used as an *operational threshold* for resolving late-time dynamical structure, memory effects, or backflow signatures? (The voyage's $T_{\text{det}}(M)$ construction.) Search terms: "shot-noise-limited non-Markovianity", "projection-noise floor revival detection", "finite-sampling witness quantum dynamics", "detection threshold information backflow".

**Expected granularity:** this is likely to return mostly *near-neighbour* literature rather than direct precedent. That is expected and not a problem. Please return near-neighbours with explicit characterisation of how they differ from the voyage's construction. "NO RESULT FOUND" here should be a last resort, not a default.

Deliver: citation list of direct or near-neighbour work, with explicit distance-from-target annotation.

### P4 — Trap-frequency stability in trapped-ion experiments

What is the typical shot-to-shot trap-frequency drift / stability in modern trapped-ion experiments? Published RMS values as fraction of $\omega_{\text{trap}}$.

**Priority order:**
1. ²⁵Mg⁺ specifically (NIST Boulder lineage; trapped-ion groups at Freiburg and comparable institutions)
2. Other single-ion / small-crystal trapped-ion platforms (Yb⁺, Ca⁺, Be⁺, Sr⁺) — flag as non-Mg-specific if used as fallback calibration
3. PTB and comparable metrology-grade setups

Deliver: numerical range with citations, clearly separated by priority level.

### P5 — Non-Markovianity measures for bounded explicit environments

Which **canonical** non-Markovianity measures are most relevant to closed-system unitary dynamics of a spin coupled to a few explicit bosonic modes (bounded mode set, not a true thermodynamic bath)?

Focus on applicability, not taxonomic completeness. Relevant candidates to consider: BLP trace-distance, RHP CP-divisibility, Fisher-information-based, coherent-information-based. For each, briefly note *whether it is well-defined for bounded environments with recurrence structure* — this is the key applicability question.

Deliver: ≤ 5 measures, brief applicability characterisation per measure, canonical citation each.

### Output format

Single markdown document, one section per task (P1–P5), with explicit "NO RESULT FOUND" or "NEAR-NEIGHBOURS ONLY" flag where applicable. Citations in full bibliographic form. Speculation explicitly bracketed or omitted. **Do not adjudicate novelty of the voyage construct** — that is Harbourmaster's job during reconciliation.

---

## Claude task card (Scout)

**Stance:** Harbourmaster. Conceptual mapping. Cross-field synthesis. Honest about where voyage-level uncertainty lies. **Maps the landscape; does not adjudicate novelty.**

### C1 — Conceptual family tree of the voyage's central construct

Place the measurement-resolved complexity idea in its conceptual lineage. Which communities have adjacent tools?
- Quantum chaos (level statistics, spectral form factor, OTOCs)
- Open quantum systems (non-Markovianity witnesses, information backflow)
- Quantum metrology (Fisher information as distinguishability)
- Many-body dynamics (entanglement entropy growth, ETH)
- Trapped-ion simulation specifically

Deliver: a short map showing which concepts the voyage imports from where, and where the apparent conceptual gap (if any) lies. Flag apparent gaps as *apparent*, pending Perplexity confirmation.

### C2 — Relationship between $T_{\text{det}}(M)$ and existing information-backflow measures

Analytical question. The structure is: information backflow from environment to system generates $\sigma^2_{\text{intrinsic}} > \sigma^2_{\text{QPN}}$ at late times. This is close to the BLP construction (trace distance revivals) but operationalised through variance-over-ensemble rather than state distinguishability.

Deliver: either (a) identification of an existing measure it reduces to under specific conditions, (b) argument that it is a distinct, measurement-budget-dependent witness, or (c) ambiguity statement flagging that the answer depends on reconciliation with Perplexity P5.

### C3 — Pitfalls from the reduced-state dynamics literature

The voyage computes $n_{\text{eff}}^{(k)}(t)$ from the single-mode reduced state's von Neumann entropy. What are known pitfalls in interpreting this dynamically?

Specifically:
- Basis-dependence (the reduced state itself is basis-invariant, but truncation effects can introduce artefacts)
- Fock-truncation-induced entropy bounds and how to distinguish physical saturation from numerical ceiling
- Early-time scaling: quadratic-in-t entropy growth is generic; what's informative is the *deviation* from generic behaviour
- Comparison to entanglement-entropy pitfalls from MCTDH convergence studies (even though we're not running MCTDH, their hard-won lessons apply)

Deliver: short list of pitfalls with brief explanation of each.

### C4 — The Ordinans-framework adjacency question

The voyage is framed against the Ordinans framework (correlation-length regime cycling as complexity signature). Is the measurement-resolved-complexity construct an *instance* of Ordinans, or does it stand alone?

Deliver: honest scoping note — what the voyage tests about Ordinans, what it does not, where the framework needs the voyage to succeed vs. where it is independent. If the answer is "the voyage stands alone and Ordinans is separately worth testing", say so.

### C5 — Draft novelty statement (pre-reconciliation)

Given what C1–C4 surface plus Perplexity's P1–P5 returns, draft a one-paragraph novelty statement for the Stage 8 writeup.

**Calibration instruction:** the defensible novelty is most likely at the level of *operational recombination* — linking reduced-state complexity, ensemble sensitivity, and finite-shot detectability in a bounded spin–boson setting — rather than "new observable" or "new physics". Draft the statement in that register. If the search surfaces direct precedent that reduces the claim further (e.g. the recombination itself has been done), say so explicitly.

**This draft is pre-reconciliation.** Harbourmaster revises against Perplexity's return.

### Output format

Single markdown document, one section per task (C1–C5). Explicit epistemic hedges (Scout flags) where synthesis is speculative. Cross-references to Perplexity's return in C5. **Do not claim novelty independently of Perplexity's findings.**

---

## Reconciliation protocol (Harbourmaster)

After both agents return:

1. **Cross-check:** Does Perplexity's P1/P2 citation set match Claude's C1 conceptual map? Flag discrepancies.
2. **Gap convergence:** Do both agents independently identify the same gap, or do they disagree on what's novel? Disagreement is informative.
3. **Pitfall integration:** Fold C3 pitfalls into the voyage plan's §10 standing questions.
4. **Interpretive caution (absorbed from external review):** *Absence of direct precedent in P2 or P3 does not by itself establish novelty.* The genuine novelty, if any, is more likely at the operational-crosswalk level — linking reduced-state complexity, ensemble sensitivity, and finite-shot detectability in a bounded spin–boson setting. Harbourmaster calibrates the Stage 8 claim accordingly.
5. **Novelty adjudication:** This is the Harbourmaster's decision, made against the combined P1–P5 + C1–C5 return. Neither agent should have made this call upstream.
6. **Archive:** Task card + both returns + reconciliation note go into the repo as `literature_search/` folder.

---

## Scope limits

- **Not** a systematic review. ~2–4 hours of focused searching per agent.
- **Not** a prerequisite for Stage 1 (the single-mode propagator). Can run in parallel.
- **Is** a prerequisite for Stage 8 (synthesis + novelty claim).
- **Is** revisable: if Stage 3 findings shift the voyage's question, the task card gets a v3.

---

## Success criteria

- At least one concrete citation or characterised near-neighbour per task line (direct gap-confirmation flagged as last resort).
- Clear statement of what the voyage can legitimately claim at the *operational-recombination* level.
- No agent fabricates citations (verifiable in P1–P5; trust-based in C1–C5).
- Harbourmaster can produce a 200-word prior-art section for Stage 8 from the combined return.

---

## Change log

- **v1 → v2:** Terminology clarification in shared context (von Neumann entropy of reduced state, not SPF populations). P1 scope boundary made explicit (cavity/circuit-QED in scope, flag platform). P2 definition prioritised over terminology. P3 rephrased to "operational threshold for resolving late-time structure" with near-neighbour granularity expected. P4 widened to trapped-ion neighbours with priority levels. P5 tightened to "canonical + applicable" rather than comprehensive. C5 calibrated to operational-recombination register. Reconciliation §4 added interpretive-caution clause. Role split now explicit: agents map, Harbourmaster adjudicates.

---

*End of task card v2.*
