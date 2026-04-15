# measurement-resolved-complexity

**Endorsement Marker:** T(h)reehouse +EC voyage — internal numerical exploration. Local candidate framework under T(h)reehouse +EC stewardship. No external endorsement implied.

A bounded numerical exploration: spin coupled to few radial motional modes under detuning sweep, comparing intrinsic (entanglement-entropy-derived) complexity against measurement-resolved (variance-over-projection-noise) complexity.

**Status (2026-04-15):** **Voyage closed.** All 8 stages complete; Stage 8 synthesis committed with writeup, revised novelty paragraph, and collaborator handoff notes. Plan at v0.2 + PA-05. Repo ready for collaborator handoffs ([MCTDH-numerics, open-systems](stages/stage8_synthesis/collaborator_notes.md)). A post-Stage-8 audit (2026-04-15) found and fixed five integrity issues (synthesis figure noise model; N=2 per-mode H2 overclaim; invalid JSON in three metrics files; README staleness; doc inconsistencies); all fixes applied.

**Stance:** Exploratory, self-contained, Harbourmaster discipline. Not a replacement for MCTDH; not a validation of Ordinans; not a publication-ready study. It is an internal-use numerical exploration to sharpen a research proposal before committing collaborator time.

**Corporate-design compliance:** Folder and licensing conventions of the T(h)reehouse +EC Corporate Design blueprint ([`threehouse-plus-ec/cd-rules`](https://github.com/threehouse-plus-ec/cd-rules)). See [`LICENCE`](LICENCE) for the per-layer licence map (Section 0.3).

---

## Structure

```
measurement-resolved-complexity/
├── README.md                   # this file (Coastline, CC BY-SA 4.0)
├── LICENCE                     # split-licence declaration (see Section 0.3)
├── VOYAGE_PLAN.md              # v0.2 plan: parameters, hypotheses, gates, standing questions
├── PLAN_AMENDMENTS.md          # amendment register (PA-01..04 absorbed at v0.2)
├── requirements.txt            # Python dependencies (numpy, scipy, matplotlib, qutip)
├── src/                        # propagation and analysis code (MIT)
├── stages/                     # per-stage artifacts, run scripts, notes, metrics
├── literature_search/          # task cards, Perplexity/Claude returns, reconciliation
├── figures/                    # per-stage inspection figures (MIT)
├── docs/                       # auxiliary documentation (per CD §14)
└── archive/                    # deprecated artefacts (per CD §0.8, §15), incl. VOYAGE_PLAN-v0.1
```

## Voyage overview

Two complexity measures, time-resolved, compared on the same trajectories:

1. **Intrinsic (theorist-visible):** $\mathcal{C}(t) = \sum_k \log n_{\text{eff}}^{(k)}(t)$ with $n_{\text{eff}}^{(k)}(t) = \exp\bigl(S_{\text{vN}}[\rho^{(k)}(t)]\bigr)$. Aggregate reported as primary invariant; per-mode curves as decomposition.
2. **Operational (experiment-visible):** $\sigma^2_{\text{intrinsic}}(t) = \mathrm{Var}_{\text{ensemble}}[p(t)]$ across $R=100$ realisations with Gaussian $\Delta$-noise, compared against the projection-noise floor $\sigma^2_{\text{QPN}}(t; M) = p(1-p)/M$. Headline scalar is $f_{\text{resolved}}(M)$ — the duty cycle of $\sigma^2_{\text{intrinsic}} > \sigma^2_{\text{QPN}}(M)$ over the simulation window. *(Replaces $T_{\text{det}}$-as-last-exceedance per Stage 3 finding; PA-03.)*

**Central hypothesis (v0.2 §5, with PA-05 reformulation pending from Stage 7).** Across the detuning sweep, $f_{\text{resolved}}(M)$ and the time-averaged complexity $\bar{\mathcal{C}}$ were hypothesised to co-vary monotonically toward resonance. Stages 5–7 show this is **not** what the voyage physics supports: the two measures probe **complementary** aspects — $\mathcal{C}$ peaks at maximum entanglement (spin reduced state at $p \approx 1/2$), $\sigma^2_{\text{intrinsic}}$ peaks at maximum state purity ($(\partial_\Delta p)^2$ large). H2 is **per-mode** at $N \geq 2$ (aggregate dilutes the signal); H3 is reframed as complementarity, not correlation. See [`stages/stage7_cut_c/notes.md`](stages/stage7_cut_c/notes.md) §6 for the PA-05 draft.

The claim is a *limit* claim probed via $|\Delta|/\omega_{\text{ref}} \in \{0.15, 0.30, 0.50\}$, not a point-claim at $\Delta = 0$ (inaccessible with the voyage's initial state; see VOYAGE_PLAN §2.5 and Standing Question 12).

See [`VOYAGE_PLAN.md`](VOYAGE_PLAN.md) for the full parameter lock, staging, hypotheses, and scope limits.

## Staging

| Stage | Purpose | Status | Commit | Headline verdict |
|---|---|---|---|---|
| 0 | Parameter lock + repo init | ✅ done | `cf00d15` | Voyage framed. |
| 1 | [Single-mode propagator + validation](stages/stage1_single_mode_propagator/notes.md) | ✅ done | `e3bb8ad` | 3 gates PASS at $10^{-9}$–$10^{-15}$; unbiased-Rabi analytic form used. |
| 2 | [$n_{\text{eff}}$ observable layer](stages/stage2_observables/notes.md) | ✅ done | `1008eee` | 4 gates PASS; Schmidt-rank-2 structural bound at $N=1$ documented. |
| 3 | [Ensemble + QPN + QFI/BLP cross-checks](stages/stage3_ensemble_qpn/notes.md) | ✅ done | `cc1bf5e` | 4 gates PASS; R2 divergence resolved in Verifier's favour (BLP recurrence-sensitive). |
| 4 | [H2 checkpoint](stages/stage4_checkpoint/notes.md) | ✅ done | `1e8d4a0` | Growth-framing alignment visible at Cut A inner ($r = 0.50$); full H2 deferred to $N \geq 2$. |
| 5 | [Cut A: single-mode detuning sweep](stages/stage5_cut_a/notes.md) | ✅ done | `214ec62` | Gate 11 PASS; H2 monotone trend; H3 non-monotone (window-normalisation); QFI crossover at innermost confirmed. |
| 6 | [Cut B: two-mode configurations](stages/stage6_cut_b/notes.md) | ✅ done | `b71bf2a` | 3 gates PASS; H2 complementarity-per-mode finding; H3 non-monotonicity persists (beat-frequency mechanism); C3.4 IPR gate clean at $N=2$. |
| 7 | [Cut C: three-mode, commensurability](stages/stage7_cut_c/notes.md) | ✅ done | `df08746` | Scoped to $R=30$, $n_{\max}=10$, 2 sweep points (runtime); all convergence PASS; H2 per-mode holds for innermost mode; aggregate H2 breaks at $N=3$; commensurability does not separate configs. |
| 8 | [Synthesis + novelty statement](stages/stage8_synthesis/writeup.md) | ✅ done | `392f642` + audit patch | Cross-stage synthesis figure; revised Scout-C5 novelty paragraph (operational-recombination register, 286 words with evidence inventory); collaborator handoff notes for MCTDH-numerics and open-systems. |

Each stage produces an inspectable artifact in [`stages/`](stages/) and [`figures/`](figures/) before the next begins.

## Literature search

Complete. Split between Perplexity (Verifier) and Claude (Scout), reconciled by the Harbourmaster:

- [`literature_search/TASK_CARD.md`](literature_search/TASK_CARD.md) — v2 task specification (Perplexity P1–P5, Claude C1–C5).
- [`literature_search/perplexity_return.md`](literature_search/perplexity_return.md) — Verifier return.
- [`literature_search/claude_return.md`](literature_search/claude_return.md) — Scout return.
- [`literature_search/reconciliation.md`](literature_search/reconciliation.md) — Harbourmaster synthesis, novelty calibration, Standing Questions.

## Reproduction

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python stages/stage1_single_mode_propagator/run.py  # and onward
```

Each stage's `run.py` is self-contained, writes `metrics.json`, and renders its figure under [`figures/`](figures/). Stages 5–7 use seeded `np.random.SeedSequence` spawn patterns (parent seeds `20260415`, `20260416`, `20260417` respectively); re-running regenerates exact metrics.

Runtime note: Stages 1–6 complete within 1–3 minutes each. Stage 7 at $N=3$ is ~80 minutes under the reduced scope ($R=30$, $n_{\max}=10$, two sweep points); the full v0.2 spec at $n_{\max}=12$ would be ~34 hours due to $O(\text{dim}^3)$ dense-eigh cost, and switching to Krylov `expm_multiply` is deferred to a follow-up voyage.

## Licence

Split architecture per the T(h)reehouse +EC Corporate Design blueprint (Section 0.3). Code and assets (MIT) under [`src/`](src/), [`figures/`](figures/); framework and methodological documents (CC BY-SA 4.0) for [`VOYAGE_PLAN.md`](VOYAGE_PLAN.md), [`stages/`](stages/), [`literature_search/`](literature_search/), [`docs/`](docs/). See [`LICENCE`](LICENCE) for the per-folder map.

## Acknowledgements

Part of the T(h)reehouse +EC open-science harbour. Voyage framing draws on the Ordinans working framework (correlation-length regime cycling as complexity signature) but is designed so its empirical content stands independently of framework adoption.
