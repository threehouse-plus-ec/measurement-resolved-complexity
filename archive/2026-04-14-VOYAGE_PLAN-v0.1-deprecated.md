# Deprecation note — `VOYAGE_PLAN.md` v0.1

**Endorsement Marker:** T(h)reehouse +EC voyage, archival. No external endorsement implied.

**Licence:** CC BY-SA 4.0 (see repository `LICENCE`).

**Deprecation date:** 2026-04-14.
**Deprecated file:** `archive/VOYAGE_PLAN-v0.1.md` (preserved unchanged).
**Superseding file:** `VOYAGE_PLAN.md` (v0.2, at repo root).
**Authority:** Harbourmaster, under Guardian adjudication.

## Reason

v0.1 accumulated four structural amendments during Stages 1–4 preparation and inspection. The Guardian tripwire rule inscribed in `PLAN_AMENDMENTS.md` at the Stage 1 commit ("if a third structural amendment arises before Stage 1 code completes, issue v0.2 rather than stacking strikethroughs") took effect after the fourth amendment and was honoured preemptively by Stage 4's verdict ("proceed to Stage 5 *subject to v0.2 being issued first*").

The four amendments, all from the same underlying pattern (plan written against JC-Rabi and dissipative-environment defaults; actual physics is unbiased-Rabi + bounded-recurrent), are absorbed into v0.2 as coherent design rather than chained corrections:

| Amendment | Source | v0.1 form | v0.2 form |
|---|---|---|---|
| PA-01 — Stage 1 JC phrasing | Stage 1 prep, 2026-04-14 | Strikethrough on "2g Rabi" parenthetical + superseding note | Stage 1 reads against the correct analytic target (Gaussian conditional-displacement form) from the outset |
| PA-02 — Fock budget and detuning range | Stage 1 prep / convergence scan / Guardian option (III-b) | Strikethrough on old §2.5 + detuning range + superseding notes in §2.4, §2.5, §5 (H3), §10 (Q#12) | Correct $\langle n \rangle_{\max} = 4(g/\Delta)^2$ formula, measured convergence table embedded, detuning set $\{\pm 0.15, \pm 0.3, \pm 0.5\}$, H3 limit-reading inline |
| PA-03 — H3 scalar ($T_{\text{det}} \to f_{\text{resolved}}$) | Stage 3 finding — $T_{\text{det}}$-as-last-exceedance saturates in bounded recurrent regimes | Flagged in Stage 3 notes for Stage 4 amendment | H3 rewritten in terms of $f_{\text{resolved}}(M)$ and $\bar{\mathcal{C}}$; §3 observables updated; §Stage 8 scatter redefined |
| PA-04 — H2 growth-framing and N=1 Schmidt caveat | Stage 4 inspection — $\mathcal{C}$ saturates to $\log 2$ at N=1 by Schmidt bound | Flagged in Stage 4 notes for v0.2 | H2 rewritten around $|\dot{\mathcal{C}}|$-vs-$\sigma^2$ alignment; N=1 under-testing and N≥2 full-test caveat written into §5 |

Each change in v0.2 is cited back to its origin amendment or Standing Question number, per the Harbour convention established in the reconciliation §R3 source-legend.

## What is not claimed resolved

v0.2 does not silently close genuinely open items. The following remain live in `VOYAGE_PLAN.md` v0.2 §10:

- Krylov / spread-complexity identity check (deferred to v3 of TASK_CARD, not within this voyage's scope).
- Noise-spectrum sensitivity (coherent modulation; optional for Stage 5).
- QFI-reduction confirmation across the full sweep (Stage 3 confirmed at $\Delta = 0.15$; sweep-wide confirmation is Stage 5/8 work).
- BLP pair optimisation (Stage 3 used a fixed antipodal pair).
- Scout C5 reduction-paths (all four) remain unretired pending Stage 5/8 evidence.

## Archive conformity

- v0.1 content preserved verbatim at `archive/VOYAGE_PLAN-v0.1.md` (no edits after this deprecation note is written).
- This deprecation note at `archive/2026-04-14-VOYAGE_PLAN-v0.1-deprecated.md`.
- Amendment-level audit trail in `PLAN_AMENDMENTS.md` at the repo root.
- Per CD §15 step 4 (tag `cd-vX.Y.Z`): not applicable here — this is a voyage-internal plan revision, not a Corporate Design asset version bump. The `PLAN_AMENDMENTS.md` register serves as the voyage-local versioning record.

*End of deprecation note.*
