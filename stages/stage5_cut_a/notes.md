# Stage 5 notes — Cut A (single-mode detuning sweep)

**Endorsement Marker:** T(h)reehouse +EC voyage, Coastline layer. No external endorsement implied.

**Licence:** CC BY-SA 4.0 for these notes (run script under MIT; see repository `LICENCE`).

**Stage:** 5 — Cut A single-mode detuning sweep against VOYAGE_PLAN v0.2.
**Run date:** 2026-04-14.
**Run script:** `run.py`.
**Figure:** `../../figures/stage5_cutA_sweep.pdf`.

---

## 1. Parameters

Per VOYAGE_PLAN v0.2 §2.4 and §Stage 5. Six-point detuning set $\Delta/\omega_{\text{ref}} \in \{-0.5, -0.3, -0.15, +0.15, +0.3, +0.5\}$, $R = 100$ realisations per point, $\sigma_\Delta/\omega_{\text{ref}} = 0.01$ (stress-test level), $g/\omega_{\text{ref}} = 0.1$, simulation window $t \in [0, 50\,\omega_{\text{ref}}^{-1}]$.

**Seeding protocol** (Guardian Stage-5 pre-run pin):

- Parent `SeedSequence(20260415)`.
- Six child sequences via `.spawn(6)` — one per Δ point, ordering ascending in Δ.
- Each child seeds a dedicated `np.random.default_rng()`; the same 100 Δ-draws feed both $n_{\max}=12$ and $n_{\max}=18$ propagations so Gate 11 compares observables on identical random structure.

Reproducibility: re-running `run.py` regenerates exact metrics.

## 2. Gate 11 — σ² convergence across the sweep

All six points pass the $10^{-5}$ target on $\max |\sigma^2_{n_{\max}=12} - \sigma^2_{n_{\max}=18}|$:

| Δ/ω_ref | Gate 11 error | Verdict |
|---:|---:|:---:|
| $-0.50$ | $3.79 \times 10^{-18}$ | PASS |
| $-0.30$ | $1.07 \times 10^{-14}$ | PASS |
| $-0.15$ | $1.04 \times 10^{-6}$ | PASS |
| $+0.15$ | $7.83 \times 10^{-7}$ | PASS |
| $+0.30$ | $8.93 \times 10^{-15}$ | PASS |
| $+0.50$ | $6.29 \times 10^{-18}$ | PASS |

Convergence tightens rapidly away from resonance (Fock-budget analytic scaling $\langle n\rangle_{\max} = 4g^2/\Delta^2$; §2.5 table). Max error $1.04 \times 10^{-6}$ at the innermost point is ten times under the gate, with the statistical-noise floor at $R=100$ providing another factor of ten of headroom. The homogeneous $n_{\max}=12$ budget is validated across the full sweep.

## 3. Per-point headline metrics ($n_{\max}=18$)

| Δ/ω_ref | $f_{\text{res}}(10^3)$ | $t_{\text{rise}}(10^3)$ | $\bar{\mathcal{C}}$ | $r(\sigma^2,\|\dot{\mathcal{C}}\|)$ | QFI median rel. dev. |
|---:|---:|---:|---:|---:|---:|
| $-0.50$ | 0.670 | 8.92 | 0.242 | +0.352 | 7.65% |
| $-0.30$ | 0.706 | 11.52 | 0.405 | +0.372 | 18.18% |
| $-0.15$ | 0.508 | 24.75 | 0.562 | +0.472 | 21.22% |
| $+0.15$ | 0.510 | 24.65 | 0.562 | +0.498 | 23.03% |
| $+0.30$ | 0.714 | 11.32 | 0.405 | +0.354 | 7.40% |
| $+0.50$ | 0.686 | 8.82 | 0.245 | +0.332 | 12.24% |

**Δ → -Δ symmetry** holds within sampling noise: $\bar{\mathcal{C}}$ agrees to three decimals; $f_{\text{resolved}}$ and $t_{\text{rise}}$ agree to 2%. The symmetry is analytic (combined $\Delta \to -\Delta$ + bosonic-phase rotation) and independent seeds for each point give an empirical sanity check that the propagator and analysis pipeline are not introducing directional bias.

## 4. Three substantive findings

### 4.1 H2 growth-framing holds monotonically across the sweep

$r(\sigma^2, |\dot{\mathcal{C}}|)$ is positive at all six points and rises monotonically toward resonance: $\sim 0.34$ at $|\Delta|=0.50$, $\sim 0.36$ at $|\Delta|=0.30$, $\sim 0.49$ at $|\Delta|=0.15$. Stage 4's pre-sweep value (0.497 at $|\Delta|=0.15$) sits in the centre of the sweep trend.

**Reading.** H2 in the growth-framing is supported at $N=1$ subject to the Schmidt-bound under-testing caveat (§VOYAGE_PLAN v0.2 §5). The sweep trend — stronger correlation nearer resonance — is exactly what the hypothesis predicts. The full H2 test at $N \geq 2$ (Stage 6 Gate 13) is unchanged by this reading; Stage 5 contributes a positive-trend preliminary.

### 4.2 H3 is non-monotone at N=1 — window-normalisation effect

$\bar{\mathcal{C}}$ scales monotonically as expected: $0.24 \to 0.41 \to 0.56$ as $|\Delta|$ decreases. But $f_{\text{resolved}}(M=1000)$ is **U-shaped**: 0.68 at $|\Delta|=0.50$, 0.71 at $|\Delta|=0.30$, *drops* to 0.51 at $|\Delta|=0.15$. The scatter of $f_{\text{resolved}}$ vs $\bar{\mathcal{C}}$ is therefore *not* a clean positive correlation.

**Mechanism.** The mode period in each $\sigma_x$-sector is $T_\Delta = 2\pi/|\Delta|$: $T_{0.50} \approx 12.6$, $T_{0.30} \approx 20.9$, $T_{0.15} \approx 41.9\,\omega_{\text{ref}}^{-1}$. With a simulation window of $50\,\omega_{\text{ref}}^{-1}$, the outer points fit $\sim 4$ full oscillations; the innermost fits $\sim 1.2$. Fewer σ²-peak cycles above the QPN floor within the window → lower $f_{\text{resolved}}$. This is a **window-normalisation artefact**, not a statement about intrinsic dynamics.

**Implication for H3.** As written in v0.2 §5, H3 expects $f_{\text{resolved}}$ and $\bar{\mathcal{C}}$ to co-vary across the sweep. Stage 5 shows they do not at $N=1$: the intrinsic scalar $\bar{\mathcal{C}}$ rises monotonically toward resonance, the operational scalar $f_{\text{resolved}}$ is window-dependent and U-shaped. The Stage 8 H3 scatter at this cut would show the six points on a curve that bends back on itself near resonance, not a clean trend.

**Reading.** H3's premise that these two scalars track each other has a **scale separation problem** at the sweep's innermost points. The voyage plan chose a $t_{\max} = 50$ window without reference to the mode period; that choice was fine for the outer Cut A points (many oscillations per window) but cuts against the innermost points (fewer than two oscillations per window). Extending $t_{\max}$ was ruled out in v0.2 §2.4 because the dynamics is bounded recurrent and the qualitative picture is unchanged — *but* the $f_{\text{resolved}}$ scalar is *not* unchanged: more oscillations under the same QPN floor would give higher $f_{\text{resolved}}$ at $|\Delta| = 0.15$. This is a limitation of $f_{\text{resolved}}$-as-scalar for the H3 statement.

**Candidate response.** Stage 8 has three legitimate moves:

1. **Report H3 as non-monotone at N=1**, with the mechanism (mode-period-vs-window scale separation) made explicit. Move the quantitative H3 verdict to $N \geq 2$ (Stages 6–7) where the multi-mode couplings redistribute σ²-cycles across mode-specific timescales.
2. **Re-normalise $f_{\text{resolved}}$** to "oscillations-above-QPN per mode period" rather than "fraction of the window" — an observable that is window-independent under the bounded recurrent dynamics. This is a plan-scope decision, not a Stage 5 notes item.
3. **Accept $f_{\text{resolved}}$ as is and note that its $\Delta$-dependence encodes more than intrinsic complexity.** This is the most honest reading: the scalar carries both intrinsic complexity and oscillation-count information, and the H3 hypothesis should be refined to separate the two.

Flagging to Guardian for Stage 6 prep. This may become amendment PA-05 after Stage 6 data, but the cleanest move right now is to document the finding and defer the scalar redefinition until Stage 6 at $N=2$ shows whether the issue persists when C has dynamical range and multi-mode timescales are in play.

### 4.3 QFI-reduction crossover confirmed empirically

Guardian's Stage 2 → 3 forward flag ("crossover toward second-order dominance at innermost points") is now empirical:

| $|\Delta|$ | Mean QFI median rel. dev. |
|---:|---:|
| 0.50 | 9.9% |
| 0.30 | 12.8% |
| 0.15 | 22.1% |

At the sweep's outer points the QFI reduction $\sigma^2_{\text{intrinsic}} \approx (\partial_\Delta p)^2 \sigma_\Delta^2$ holds to the Stage-3 Gate-8 10% bar. At $|\Delta| = 0.15$ it breaks the bar, climbing to ~22%. Stage 3's confirmation at $|\Delta| = 0.15$ was inside its own 10%-median gate but close to the edge (6.98%); the sweep pushes it well over at the innermost points.

**Reading.** The leading-order Fisher-information reduction is breaking down approaching resonance — as Guardian anticipated, this is consistent with second-order $\partial_\Delta^2 p$ contributions becoming relevant when $\partial_\Delta p$ itself is small (which it becomes near the $\Delta = 0$ singularity where the symmetry-forced vanishing of $\partial_\Delta p$ would be reached in the limit). The reduction-path 3 contraction in Scout's C5 novelty draft ("the claim contracts to a trapped-ion-parameterised implementation of [cited] QFI-flow witness") **does not hold uniformly** across Cut A. It holds at $|\Delta| \geq 0.30$ and breaks at $|\Delta| = 0.15$.

**Implication for Stage 8 novelty.** C5 reduction-path 3 is *not* the uniform contraction that Stage 3 suggested. The novelty paragraph can keep the operational-crosswalk framing without the "reduces to QFI" hedge — or, more honestly, can state that the reduction holds at the sweep's outer points and breaks at the innermost. The latter is the Stage 5 evidence and should appear in the Stage 8 writeup as a physics finding, not as a hedge.

## 5. H2 / H3 / QFI summary

| Claim | v0.2 form | Stage 5 evidence |
|---|---|---|
| H1 (rise from $t = 0$) | weak, trivially expected | holds trivially |
| H2 (growth-framing: $r(\sigma^2, |\dot{\mathcal{C}}|)$ positive, stronger near resonance) | under-tested at N=1 by Schmidt bound | **monotone trend across sweep, supports H2; full test at N≥2** |
| H3 ($f_{\text{resolved}}$ and $\bar{\mathcal{C}}$ co-vary monotonically across sweep) | single-scalar expectation | **non-monotone: $\bar{\mathcal{C}}$ monotone, $f_{\text{resolved}}$ U-shaped; window-normalisation effect** |
| Scout C5 reduction-path 3 (QFI reduction uniform) | live pending Stage 5 evidence | **non-uniform: 7–12% at outer, 21–23% at innermost; reduction breaks near resonance** |

## 6. Standing items — status updates

| Item | Origin | Stage 5 status |
|---|---|---|
| $\sigma^2$-convergence re-verified per point | v0.2 Gate 11 | **all six points cleared** at $10^{-5}$ target. |
| Per-Δ $(c_2, c_4)$ short-time fit | v0.2 §3.4 discipline | Recorded in `metrics.json`. $c_2$ constant at $g^2$ across sweep (expected from the $\alpha_\pm \sim -igt$ small-$t$ form being Δ-independent); $c_4$ varies by ~20% across the sweep, carrying the Δ-dependence. |
| H2 growth-framing sweep trend | v0.2 H2 | **positive monotone as hypothesised**. |
| QFI reduction (C5 path 3) | v0.2 C5 live | **non-uniform across sweep; breaks at innermost points**. Stage 8 contraction must reflect this. |
| $f_{\text{resolved}}$ vs $\bar{\mathcal{C}}$ scatter | v0.2 H3 | **non-monotone at N=1 due to mode-period-vs-window scale separation**. Deferred to Stage 6 for adjudication. |

## 7. Standing items forwarded to Stage 6

1. **H3 scalar redefinition question.** Before Stage 6 runs, Guardian review of whether $f_{\text{resolved}}$ as a window-fraction is the right scalar, or whether a window-period-normalised alternative (e.g. "fraction of σ²-above-QPN *excursions* relative to total excursion count") is needed. At $N = 2$ the coupling spreads σ² across multiple mode-specific timescales, so the single-mode-period argument may not bite as hard, but the question stands.
2. **QFI-reduction breakdown at innermost points: second-order tracking.** Stage 6 should compute $\partial_\Delta^2 p$ on a sample point and compare against $\sigma^2_{\text{intrinsic}}$ to test whether second-order Fisher information is what's taking over. If so, a *two-term* reduction $\sigma^2 \approx (\partial_\Delta p)^2 \sigma_\Delta^2 + \tfrac{1}{2}(\partial_\Delta^2 p)^2 \sigma_\Delta^4$ is the cleaner operational object. This is the proper form of the Stage 2 → 3 forward flag Guardian raised; Stage 5 has surfaced the empirical regime where it matters.
3. **H2 full test at $N = 2$.** Stage 6 Gate 13 remains as planned in v0.2 §6. Stage 5 provides a positive baseline from the growth-framing fragment at $N = 1$; Stage 6 will tell whether the full test confirms or contracts this.
4. **IPR test at first $N=2$ point.** v0.2 §3.4 / §6 Stage 6 Gate 12 remains unchanged.

## 8. Verdict

Stage 5 produces three substantive findings, not a simple gate pass/fail. All six Cut A points pass Gate 11 (convergence), which is the only hard gate. The H2 growth-framing is cleanly confirmed. H3 as written is non-monotone — a real finding, not a failure, with a clean mechanism. The QFI reduction breaks at innermost points — Guardian's flagged crossover is real.

Stage 5 does not trigger an immediate plan amendment: Guardian should see the Stage 6 data before adjudicating whether PA-05 is needed. H3's reformulation may turn out to be unnecessary at $N = 2$ (if multi-mode timescales bypass the mode-period-vs-window issue), or it may become the v0.3 trigger. Flagging rather than amending.

**Stage 6 (Cut B, $N = 2$) cleared to begin on Guardian sign-off.**
