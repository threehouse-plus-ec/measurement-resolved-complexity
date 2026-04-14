# Task Card — Harbourmaster Literature Reconciliation

**Voyage:** Measurement-Resolved Complexity (spin + few motional modes, detuning sweep)
**Issued:** 2026-04-14
**Role:** Harbourmaster
**Scope:** Reconciliation of Perplexity (Verifier) and Claude (Scout) literature search returns. Formalisation of §Reconciliation protocol from TASK_CARD.md v2.

---

## 1. Position in the workflow

This task begins **only after** both upstream returns are in hand:
- `literature_search/perplexity_return.md` (Verifier: P1–P5)
- `literature_search/claude_return.md` (Scout: C1–C5)

It produces a single deliverable:
- `literature_search/reconciliation.md`

This deliverable is a prerequisite for Stage 8 (synthesis + novelty statement). It is *not* a prerequisite for Stages 1–7.

---

## 2. Stance

**Harbourmaster.** Oxford British English. Pedantic archivist mode acceptable where precision helps. Agnostic about the territory; deals only in maps. No metaphysical claims about the voyage's significance.

The Harbourmaster's function here is **adjudicative**, not generative. Perplexity and Claude-Scout have mapped the landscape; the Harbourmaster's job is to compare those two maps, identify where they agree, disagree, or leave gaps, and produce a calibrated synthesis. The Harbourmaster **does not** conduct new literature searches at this stage — if the combined returns are insufficient, the correct move is to flag the insufficiency and request a v3 task card, not to paper over the gap.

---

## 3. Core function (from Council-3 Constitution v0.4)

> *Harbourmaster ensures best-effort atlas consistency under known limits.*

For this task, "atlas consistency" means: the Verifier and Scout maps must be reconcilable into a single coherent prior-art picture, or the inconsistencies must be named explicitly and carried forward as Standing Questions.

The Harbourmaster holds **no veto** in this task. Vetoes belong to the Core stances (Guardian, Architect, Integrator). The Harbourmaster's output is a synthesis document; if a veto is needed mid-reconciliation (e.g. ethical issue surfaces, structural contradiction appears), it is raised as a flag to the appropriate stance and the reconciliation pauses.

---

## 4. Reconciliation tasks

### R1 — Citation set cross-check

Does Perplexity's P1/P2 citation set match Claude's C1 conceptual map?

Procedure:
- Extract all citations from P1 and P2.
- Extract all concept-to-community mappings from C1.
- For each Perplexity citation, identify the Scout-community it should sit within per C1.
- For each Scout-community in C1, identify which Perplexity citations populate it.
- Flag: (i) citations Scout did not anticipate, (ii) communities Scout mapped that Verifier returned no citations for.

Deliver: a two-column table (Verifier citation → Scout community) plus a short list of discrepancies.

### R2 — Gap convergence

Do both agents independently identify the same gap, or do they disagree on what is novel?

Three possible outcomes:
- **Convergent gap:** both agents point to the same missing-piece — strongest evidence of genuine unoccupied ground.
- **Divergent gap:** Verifier finds near-neighbour precedent Scout didn't anticipate, *or* Scout identifies a conceptual gap Verifier's citation density doesn't address. Both cases are informative and both get recorded.
- **No gap claimed:** the construct sits within established practice; the voyage's value is pedagogical or consolidative rather than novel.

Deliver: a one-paragraph convergence-or-divergence statement, with specific pointers to upstream content.

### R3 — Pitfall integration

Fold Claude-Scout's C3 pitfalls into the voyage plan's §10 Standing Questions. Check whether Perplexity's P2/P3 returns surface additional pitfalls not captured by C3.

Deliver: an updated Standing Questions list as a patch to `VOYAGE_PLAN.md` §10, annotated with source (C3 / P2 / P3 / Harbourmaster-derived).

### R4 — Interpretive caution clause (absorbed from external review of TASK_CARD v1)

**Non-negotiable principle:** *Absence of direct precedent in P2 or P3 does not by itself establish novelty.* The genuine novelty, if any, is at the operational-crosswalk level — linking reduced-state complexity, ensemble sensitivity, and finite-shot detectability in a bounded spin–boson setting.

Harbourmaster applies this clause when reading the combined returns. If Perplexity flags "NO RESULT FOUND" or "NEAR-NEIGHBOURS ONLY" for P2 or P3, this is **not** to be read as "the voyage has found something new." It is to be read as "direct precedent is absent; operational-crosswalk novelty remains to be adjudicated."

Deliver: an explicit statement in the reconciliation document reaffirming this clause applies.

### R5 — Novelty adjudication

The Harbourmaster's signature task. Given R1–R4 findings, produce a calibrated novelty statement for the Stage 8 writeup.

**Register:** operational-recombination. *Not* "new observable" or "new physics" unless R1–R2 give strong evidence for either.

**Structure of the statement:**
1. What exists in the literature (citing P1, P2, P3 most relevant returns).
2. What the voyage recombines that has not been recombined (the specific operational crosswalk: $n_{\text{eff}}$ + ensemble variance + QPN threshold in the bounded spin–boson setting).
3. What remains to be demonstrated empirically by the voyage itself (the H3 correlation between $T_{\text{det}}(M)$ and saturation $\mathcal{C}$).
4. Honest hedge: what a stronger prior-art result would reduce the claim to.

**Length:** one paragraph, ≤ 200 words. This is the Stage 8 prior-art section's backbone.

Deliver: the novelty paragraph, plus a short "reduction-path" note describing what finding would retract it.

### R6 — Archive and version

Commit Perplexity return, Claude-Scout return, and reconciliation document together. If any of R1–R5 exposed a task-card flaw, flag for TASK_CARD v3 rather than silently revising.

Deliver: directory commit with explicit version stamps on all three documents.

---

## 5. Output template

The `reconciliation.md` document should follow this structure:

```markdown
# Literature Reconciliation — [date]

## Summary (≤ 3 sentences)
What the combined returns establish; where the voyage sits.

## R1 — Citation cross-check
[table + discrepancies]

## R2 — Gap convergence
[convergence/divergence statement]

## R3 — Pitfall integration
[patched Standing Questions, annotated by source]

## R4 — Interpretive caution reaffirmed
[clause restated + scope of application]

## R5 — Novelty statement (pre-Stage-8)
[calibrated paragraph + reduction-path note]

## R6 — Archive notes
[version stamps, flagged task-card issues if any]

## Standing items forwarded to Stage 8
[anything Harbourmaster cannot close here]
```

---

## 6. Failure modes

| Mode | Handling |
|---|---|
| Perplexity return materially incomplete (< 3 of P1–P5 substantively addressed) | Do not proceed with reconciliation. Flag to steward for v3 task card. |
| Claude-Scout return materially incomplete (< 3 of C1–C5 substantively addressed) | Same. |
| Direct precedent found for the full construct in P1/P2 | Calibrate novelty statement *downward*; voyage becomes a replication/consolidation study, which is still valuable. |
| No precedent found for any element | Apply R4 rigorously; resist the temptation to claim full novelty. Most likely: operational-recombination novelty survives, single-element novelty does not. |
| Verifier and Scout disagree sharply on what exists | Record disagreement in R2; do not resolve unilaterally. Either accept both readings as a Standing Question or request v3. |

---

## 7. Scope limits (Harbourmaster restraint)

Explicitly *not* in this task:

- Conducting new literature searches.
- Revising Perplexity or Claude-Scout returns (they are upstream artefacts; challenge via v3 task card if needed).
- Deciding whether the voyage proceeds (that is the steward's call, informed by but not determined by reconciliation).
- Writing the Stage 8 prior-art section itself (R5 produces the backbone; Stage 8 integrates it with voyage results).
- Adjudicating Ordinans framework claims (that is a separate Council-3 deliberation).

---

## 8. Success criteria

- Every P1–P5 return is cross-referenced at least once in the reconciliation.
- Every C1–C5 return is cross-referenced at least once in the reconciliation.
- R5 novelty paragraph is calibrated to operational-recombination register by default, with upward or downward adjustment only on explicit R1–R2 evidence.
- Reduction-path note is present and specific.
- Any task-card flaws exposed are flagged for v3, not silently patched.

---

*End of Harbourmaster task card.*
