# Plan Amendments Register

**Endorsement Marker:** T(h)reehouse +EC voyage, Coastline layer. No external endorsement implied.

**Licence:** CC BY-SA 4.0 (see repository `LICENCE`).

Tracks structural amendments to `VOYAGE_PLAN.md` made after Stage 0 lock. The Harbour convention is *superseding note + dated strikethrough* rather than silent edit, so anyone reading the plan cold encounters the correction in place. This file is the accompanying index — it does not contain content, only pointers.

## Convention

Each amendment is recorded as a single row: date, section amended, short description, driving document, amendment style. If three or more structural amendments accrue before a stage launches, the next move is a clean **v0.2 of `VOYAGE_PLAN.md`** — stacking strikethroughs past that point turns the plan into a palimpsest.

## Register

| Date | Section(s) | Amendment | Driver | Style |
|---|---|---|---|---|
| 2026-04-14 | §Stage 1 go/no-go, §Stage 3 scope, §2.1 (gauge), §2.4 (1% RMS rationale), §10 | Pre-Stage-1 plan patches from Harbourmaster reconciliation: gauge convention documented, 1% RMS reframed as stress-test, Stage 1 gate 3 added, Stage 3 scope extended with QFI + BLP cross-checks, §10 Standing Questions populated with reconciliation-derived pitfalls. | `literature_search/reconciliation.md` | Inline, no strikethrough (new content) |
| 2026-04-14 | §Stage 1 (JC-phrasing), §2.4 (detuning range), §2.5 (Fock justification), §5 (H3 reading), §10 (Standing Q #12) | Stage-1-prep corrections triggered by an analytic-validation check on the §2.1 Hamiltonian. The "$2g$ Rabi" phrasing and the "$n \sim 5\text{–}8$" Fock budget were both derived from JC-Rabi folklore that does not apply to the unbiased Rabi model; at $\Delta = 0$ the mode amplitude grows as $gt$ without bound (with the voyage's $\|\uparrow\rangle\|0\rangle$ initial state). Correction: analytic target replaced by Gaussian conditional-displacement form; $\Delta = 0$ dropped from the Cut A sweep; six near-resonance-bracketing points retained; H3 language re-read as a limit rather than a point. | Stage 1 preparation analytic check; Guardian adjudication of options (I)–(IV). | Superseding note + strikethrough on the affected parenthetical |

## Tripwire

Two amendments accumulated during Stage 1 preparation, both traceable to one underlying conceptual confusion (JC-Rabi folklore misapplied to the unbiased Rabi model). Guardian flag: if a *third* structural amendment arises before Stage 1 code completes, do not stack a third strikethrough — issue `VOYAGE_PLAN.md` v0.2 with the amendments absorbed cleanly, preserve v0.1 in `archive/` per CD §0.8, and continue from there.
