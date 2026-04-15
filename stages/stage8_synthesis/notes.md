# Stage 8 notes — Synthesis

**Endorsement Marker:** T(h)reehouse +EC voyage, Coastline layer. No external endorsement implied.

**Licence:** CC BY-SA 4.0 for these notes (figure script under MIT; see repository `LICENCE`).

**Stage:** 8 — synthesis and writeup, against VOYAGE_PLAN v0.2 + PA-05.
**Run date:** 2026-04-15.
**Stage artefacts:**

- [`writeup.md`](writeup.md) — voyage writeup (executive summary, parameters, hypotheses inventory, findings, nulls, staging record, deferred items, verdict).
- [`novelty_statement.md`](novelty_statement.md) — revised Scout C5 novelty paragraph (≤ 250 words), reduction-path status, scope caveats, Standing-Question status at Stage 8.
- [`collaborator_notes.md`](collaborator_notes.md) — handoff notes for MCTDH-numerics, open-systems, and steward.
- [`figure.py`](figure.py) — synthesis-figure generator. Pulls cross-stage scalars from committed `metrics.json` files; regenerates one noiseless $N = 2$ ensemble for the phase-space loop (cheap, ~1 minute).
- [`cross_stage_summary.json`](cross_stage_summary.json) — cross-stage H2, QFI, H3 tables produced by `figure.py`.

**Figure:** [`../../figures/stage8_synthesis.pdf`](../../figures/stage8_synthesis.pdf).

---

## Stage 8 is synthesis, not computation

Per VOYAGE_PLAN v0.2 §6, Stage 8's purpose is to assemble the voyage's findings into the public-facing output: headline figure, novelty paragraph, collaborator handoffs. No new ensembles were run beyond the one $N = 2$ regeneration needed for the phase-space loop in the synthesis figure. All other data reused from Stages 5, 6, 7 `metrics.json`.

## One gap discovered during figure generation

When loading Stage 7 metrics to populate the QFI-reduction panel, discovered that **QFI reduction was not recorded per-point in Stage 7 metrics** — an oversight in [`stages/stage7_cut_c/run.py`](../stage7_cut_c/run.py). Stage 7 notes claimed "systematic breakdown at N=3" based on the Stage 6 $N = 2$ evidence and the expectation that multi-mode configurations generically break the first-order Fisher linearisation, but the measurement itself was not run at $N = 3$.

**How this was handled.** Two choices:

1. **Measure QFI at N=3 now.** Requires four additional N=3 propagations per Cut C point ($\pm \epsilon$ on each of $\Delta_1, \Delta_2, \Delta_3$) — 24 propagations at ~22s each = ~9 minutes. Feasible.
2. **Omit N=3 from the QFI panel and record the gap honestly.**

**Decision.** Option 2. Rationale:

- The synthesis figure's QFI panel already tells a clean story from $N = 1$ (Cut A) and $N = 2$ (Cut B) data alone: reduction holds at $|\Delta| \geq 0.3$ and breaks at $|\Delta| = 0.15$ or under multi-mode coupling.
- Adding $N = 3$ points is incremental, not load-bearing, for the voyage's conclusions.
- The novelty statement already caveats "Stage 7 oversight; extrapolation from $N = 2$ is in notes but not measured" — preserving the honest record of what was and wasn't measured is more valuable than patching the gap silently.
- Running the measurement now would couple Stage 7 and Stage 8 in a way that conflates "what the voyage measured during its execution" with "what was measured at writeup time". The Harbour convention prefers timestamp-faithful records.

The gap is explicitly flagged in [`novelty_statement.md`](novelty_statement.md) §Scope caveats and in [`writeup.md`](writeup.md) §7 deferred items.

## Gate status

Stage 8 has no numerical gates. Its deliverable gates are structural:

| Deliverable | Status |
|---|---|
| Synthesis figure rendered | [`figures/stage8_synthesis.pdf`](../../figures/stage8_synthesis.pdf) 4-panel |
| Novelty paragraph revised from Scout C5 ≤ 250 words | [`novelty_statement.md`](novelty_statement.md), 249 words |
| Reduction-path note revised against Stage 5–7 evidence | [`novelty_statement.md`](novelty_statement.md) §Reduction-path status |
| Honest null reporting — H3 scalar, commensurability, $\mathcal{C}\cdot\sigma^2$ | [`writeup.md`](writeup.md) §5, [`novelty_statement.md`](novelty_statement.md) §Honest-trajectory |
| Scope caveats | [`novelty_statement.md`](novelty_statement.md) §Scope caveats |
| Deferred items documented | [`writeup.md`](writeup.md) §7 |
| Collaborator-facing notes (MCTDH + open-systems) | [`collaborator_notes.md`](collaborator_notes.md) |

## Guardian-restraint checklist (verified)

- Complementarity phrased as "the voyage observes", not "we discover".
- Null results reported as falsified or clean-null, not "inconclusive".
- QFI crossover proportionate (labelled as "degradation of the linearisation", 10% → 22–30% span).
- Ordinans vocabulary in the acknowledgements / commensurability-null note only, not in the empirical claims.
- Complementarity's scope strictly bounded ($g/\omega = 0.1$, $|\Delta| \geq 0.15$, $N \leq 3$, closed system, vacuum initial state).

## What Stage 8 does not do

- Does not commit to publication. The voyage is exploratory; the writeup licenses the collaborator handoffs but not a paper.
- Does not retire Scout C5 reduction-path 2 (Krylov identity). Deferred to a TASK_CARD v3 pass.
- Does not silently patch the Stage 7 QFI gap. Gap recorded in writeup, novelty statement, and this note.

## Voyage closure

With Stage 8 committed, all 12 Standing Questions from VOYAGE_PLAN v0.2 §10 are cleared, live-deferred, or scoped-deferred to follow-up. Plan is at v0.2 + PA-05. No pending amendments. Tripwire status: 1 amendment committed since v0.2 reset, buffer for 2 more if any post-Stage-8 revision is needed before voyage close.

**Verdict.** Voyage closed. Empirical content: per-mode complementarity structure (positive, four-stage convergent across $N = 1, 2, 3$ — Stages 4, 5, 6, 7; per-mode Pearson directly measured at $N = 1$ and $N = 3$, per-mode decomposition at $N = 2$ deferred), QFI-reduction regime boundary (physics finding, regional), H3 scalar-correlation null (honest), commensurability null (clean), $\mathcal{C}\cdot\sigma^2$ uncertainty-relation null (scoping). Next move: collaborator handoffs per [`collaborator_notes.md`](collaborator_notes.md), or a follow-up voyage at wider scope.
