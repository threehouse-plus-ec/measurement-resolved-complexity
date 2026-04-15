# stages/

**Endorsement Marker:** T(h)reehouse +EC voyage, Coastline layer. No external endorsement implied.

**Licence:** CC BY-SA 4.0 for notes and writeups; run scripts and code fragments under MIT (see repository `LICENCE`).

Per-stage artifacts, scripts, notes, and writeups. Voyage-complete layout (as committed at Stage 8):

```
stages/
├── stage1_single_mode_propagator/  metrics.json, notes.md, run.py
├── stage2_observables/             metrics.json, notes.md, run.py
├── stage3_ensemble_qpn/            metrics.json, notes.md, run.py
├── stage4_checkpoint/              metrics.json, notes.md, run.py
├── stage5_cut_a/                   metrics.json, notes.md, run.py
├── stage6_cut_b/                   metrics.json, notes.md, run.py
├── stage7_cut_c/                   metrics.json, notes.md, run.py, run.log
└── stage8_synthesis/               notes.md, writeup.md, novelty_statement.md,
                                    collaborator_notes.md, figure.py,
                                    cross_stage_summary.json
```

Each stage directory contains the run/figure script, a `notes.md` recording parameters and observations, and `metrics.json` storing headline scalars for cross-stage reuse. Stage 8's `figure.py` consumes the committed `metrics.json` files to produce the synthesis figure (plus one on-the-fly N=2 ensemble regeneration for the phase-space loop).

No stage begins without sign-off on the previous one. See `../VOYAGE_PLAN.md` §6 for the gate structure; `../PLAN_AMENDMENTS.md` for the amendment register; `./stage8_synthesis/writeup.md` for the closed-voyage verdict.
