# measurement-resolved-complexity

**Endorsement Marker:** T(h)reehouse +EC voyage — internal numerical exploration. Local candidate framework under T(h)reehouse +EC stewardship. No external endorsement implied.

A bounded numerical exploration: spin coupled to few radial motional modes under detuning sweep, comparing intrinsic (entanglement-entropy-derived) complexity against measurement-resolved (variance-over-projection-noise) complexity.

**Status:** Pre-execution. Parameters locked, staging defined, Stage 1 ready for kickoff.

**Stance:** Exploratory, self-contained, Harbourmaster discipline. Not a replacement for MCTDH; not a validation of Ordinans; not a publication-ready study. It is an internal-use numerical exploration to sharpen a research proposal before committing collaborator time.

**Corporate-design compliance:** This repository follows the folder and licensing conventions of the T(h)reehouse +EC Corporate Design blueprint (`threehouse-plus-ec/cd-rules`). See `LICENCE` for the per-layer licence map (Section 0.3).

---

## Structure

```
measurement-resolved-complexity/
├── README.md                   # this file (Coastline, CC BY-SA 4.0)
├── LICENCE                     # split-licence declaration (see Section 0.3)
├── VOYAGE_PLAN.md              # full Stage 0 plan, locked parameters
├── requirements.txt            # Python dependencies
├── .gitignore
├── src/                        # propagation and analysis code (MIT)
├── stages/                     # per-stage artifacts and writeups
├── literature_search/          # task cards, Perplexity + Claude returns, reconciliation
├── figures/                    # per-stage inspection figures (MIT)
├── docs/                       # auxiliary documentation (per CD §14)
└── archive/                    # deprecated artefacts (per CD §0.8, §15)
```

## Voyage overview

Two complexity measures, time-resolved, compared on the same trajectories:

1. **Intrinsic:** $n_{\text{eff}}^{(k)}(t) = \exp(S_{\text{vN}}[\rho^{(k)}(t)])$ — exponential of the von Neumann entropy of the single-mode reduced state.
2. **Operational:** $\sigma^2_{\text{intrinsic}}(t)$ thresholded against quantum projection noise $\sigma^2_{\text{QPN}}(t; M) = p(1-p)/M$, defining a detectability horizon $T_{\text{det}}(M)$.

**Central hypothesis:** $T_{\text{det}}(M)$ and saturation of $n_{\text{eff}}$ track each other across the detuning sweep.

See `VOYAGE_PLAN.md` for full parameter lock, staging, hypotheses, and scope limits.

## Staging

| Stage | Purpose | Status |
|---|---|---|
| 0 | Parameter lock + repo init | ✅ done |
| 1 | Single-mode propagator, JC validation | pending |
| 2 | Add $n_{\text{eff}}$ observables | pending |
| 3 | Add ensemble + QPN layer | pending |
| 4 | Go/no-go checkpoint on H2 | pending |
| 5 | Cut A: single-mode detuning sweep | pending |
| 6 | Cut B: two-mode configurations | pending |
| 7 | Cut C: three-mode, commensurability | pending |
| 8 | Synthesis + novelty statement | pending |

Each stage produces an inspectable artifact in `stages/` and `figures/` before the next begins.

## Literature search

Running in parallel with Stage 1, not blocking it. Split between Perplexity (Verifier: citations, parameters, field conventions) and Claude (Scout: conceptual mapping, pitfalls). See [`literature_search/TASK_CARD.md`](literature_search/TASK_CARD.md) for the v2 task specification and [`literature_search/reconciliation.md`](literature_search/reconciliation.md) for the Harbourmaster synthesis.

## Licence

Split architecture per the T(h)reehouse +EC Corporate Design blueprint (Section 0.3). Code and assets under MIT; framework and methodological documents under CC BY-SA 4.0. See `LICENCE` for the per-folder map.

## Acknowledgements

Part of the T(h)reehouse +EC open-science harbour. Voyage framing draws on the Ordinans working framework (correlation-length regime cycling as complexity signature) but is designed so its empirical content stands independently of framework adoption.
