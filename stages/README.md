# stages/

**Endorsement Marker:** T(h)reehouse +EC voyage, Coastline layer. No external endorsement implied.

**Licence:** CC BY-SA 4.0 for notes and writeups; run scripts and code fragments under MIT (see repository `LICENCE`).

Per-stage artifacts, scripts, and short writeups.

Expected layout (filled in as voyage proceeds):

```
stages/
├── stage1_single_mode_propagator/
│   ├── run.py
│   ├── notes.md
│   └── convergence_check.md
├── stage2_observables/
│   ├── run.py
│   └── notes.md
├── stage3_ensemble_qpn/
│   ├── run.py
│   └── notes.md
├── stage4_checkpoint.md          # go/no-go decision on H2
├── stage5_cut_A/
├── stage6_cut_B/
├── stage7_cut_C/
└── stage8_synthesis/
    ├── h3_scatter.py
    ├── writeup.md
    └── novelty_statement.md
```

Each stage directory contains its run script, a short `notes.md` recording parameters used and observations, and (eventually) figures copied or linked into the top-level `figures/`.

No stage begins without sign-off on the previous one. See `../VOYAGE_PLAN.md` §6.
