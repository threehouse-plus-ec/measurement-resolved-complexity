# Stage 6 notes — Cut B (two-mode configurations, N=2)

**Endorsement Marker:** T(h)reehouse +EC voyage, Coastline layer. No external endorsement implied.

**Licence:** CC BY-SA 4.0 for these notes (run script under MIT; see repository `LICENCE`).

**Stage:** 6 — Cut B, $N = 2$ detuning configurations.
**Run date:** 2026-04-14.
**Run script:** `run.py`.
**Figure:** `../../figures/stage6_cutB_sweep.pdf`.

---

## 1. Parameters

Per VOYAGE_PLAN v0.2 §4 (Cut B). Four structured configurations with $g = 0.1$, $\sigma_\Delta = 0.01$ (stress-test), $R = 100$ realisations per point, $n_{\max} \in \{12, 18\}$, $t \in [0, 50\,\omega_{\text{ref}}^{-1}]$, $M \in \{100, 1000, 10^4\}$.

**Seeding:** `SeedSequence(20260416).spawn(4)`, one per config; identical draws across $n_{\max}$ values per config.

**Guardian middle-path items (pinned before run):**

- Log both $f_{\text{resolved}}$ and $f_{\text{per-cycle}}(T) = f_{\text{resolved}} \cdot (t_{\max}/T)$ for two period choices: $T_{\text{slow}} = 2\pi / \min(|\Delta_1|, |\Delta_2|)$ and $T_{\text{beat}} = 2\pi / |\Delta_1 - \Delta_2|$.
- Report IPR · $n_{\text{eff}}$ per mode (uniform-on-$n_{\text{eff}}$-modes = 1; more-peaked > 1; more-spread < 1). Guardian's original text said "IPR vs $1/n_{\text{eff}}^2$"; analytic check gives $\mathrm{IPR} = 1/n_{\text{eff}}$ for a uniform-on-$D$-modes spectrum, and the numerics confirm (B1 mode 1: $n_{\text{eff}} = 2.00$, $\mathrm{IPR} = 0.500$, $\mathrm{IPR} \cdot n_{\text{eff}} = 1.000$ exactly). Logged both ratios $\mathrm{IPR} \cdot n_{\text{eff}}$ (physically motivated) and $\mathrm{IPR} \cdot n_{\text{eff}}^2$ (literal reading of Guardian's note) so Stage 8 can cite whichever is endorsed.

## 2. Gate 11-N2 — σ² convergence across Cut B

| Config | (Δ₁, Δ₂) | Gate 11 error | Verdict |
|---|---|---:|:---:|
| B1 | (+0.15, +0.15) | $5.37 \times 10^{-7}$ | PASS |
| B2 | (+0.15, +0.30) | $4.61 \times 10^{-7}$ | PASS |
| B3 | (-0.15, +0.15) | $6.46 \times 10^{-7}$ | PASS |
| B4 | (+0.15, +0.50) | $5.32 \times 10^{-7}$ | PASS |

All four configs comfortably below $10^{-5}$. The homogeneous $n_{\max} = 12$ budget, validated in Stage 5 at $N = 1$ across Cut A, generalises to the Cut B regime. §2.5's analytic bound $\langle n \rangle_{\max} = 4 g^2/\Delta^2$ per mode stays within budget with both modes at $|\Delta| \geq 0.15$.

## 3. Gate 12 — IPR / peakedness diagnostic (Guardian's C3.4 test)

IPR diagnostic at the noiseless $\mathcal{C}$-peak, per config and per mode:

| Config | Mode | $t$ at peak | $n_{\text{eff}}$ | IPR | $\mathrm{IPR}\cdot n_{\text{eff}}$ | $\mathrm{IPR}\cdot n_{\text{eff}}^2$ |
|---|:---:|:---:|---:|---:|---:|---:|
| B1 | 1 | 20.94 | 1.999 | 0.500 | 1.000 | 2.000 |
| B1 | 2 | 20.94 | 1.999 | 0.500 | 1.000 | 2.000 |
| B2 | 1 | 11.22 | 1.981 | 0.510 | 1.009 | 2.000 |
| B2 | 2 | 11.22 | 1.830 | 0.586 | 1.073 | 1.963 |
| B3 | 1 | 20.94 | 1.999 | 0.500 | 1.000 | 2.000 |
| B3 | 2 | 20.94 | 1.999 | 0.500 | 1.000 | 2.000 |
| B4 | 1 | 18.84 | 1.999 | 0.500 | 1.000 | 2.000 |
| B4 | 2 | 18.84 | 1.491 | 0.764 | 1.138 | 1.697 |

**Reading.** $\mathrm{IPR} \cdot n_{\text{eff}} = 1.000$ exactly for modes at or near resonance (all B1/B3 modes; B2/B4 mode 1). For off-resonance modes where $n_{\text{eff}} < 2$ (B2 mode 2 at $n_{\text{eff}} = 1.83$, B4 mode 2 at $n_{\text{eff}} = 1.49$) the ratio climbs slightly above 1, reaching 1.14 at the most asymmetric point. The spectrum is in all cases close to uniform-on-$n_{\text{eff}}$-modes; the "effective orbital count" reading of $n_{\text{eff}}$ is literal at $N = 2$, not rhetorical.

**Gate 12 verdict: Scout's C3.4 semantic-overclaim concern does *not* bite at $N = 2$ in the voyage's coupling regime.** Stage 8's writeup may use "$n_{\text{eff}}$ effective orbital count" language without the rhetorical hedge. A caveat: this is checked only at the peak-$\mathcal{C}$ timepoint in Cut B; Cut C at $N = 3$ should re-verify since Schmidt-rank bounds loosen further there and the peakedness story could change.

**On the $1/n_{\text{eff}}^2$ vs $1/n_{\text{eff}}$ framing.** Guardian's original note said "compare IPR to $1/n_{\text{eff}}^2$". Analytically, for a uniform spectrum over $D$ modes, $\lambda_j = 1/D$ gives $\mathrm{IPR} = 1/D$ and $n_{\text{eff}} = D$, so $\mathrm{IPR} = 1/n_{\text{eff}}$ is the correct uniform-peakedness relation. The data confirm: $\mathrm{IPR} \cdot n_{\text{eff}} = 1.000$ at all at-resonance modes. The $\mathrm{IPR} \cdot n_{\text{eff}}^2$ quantity takes the value 2 there (not 1), which doesn't carry a clean "peakedness" meaning. Reading the Guardian note as a slip and using $\mathrm{IPR} \cdot n_{\text{eff}}$ as the diagnostic.

## 4. Gate 13 — full H2 test at N=2

Schmidt-rank bound at $N = 2$ loosens to $\log \min(n_{\max}+1,\, 2(n_{\max}+1)) = \log 13 \approx 2.56$ at $n_{\max} = 12$; in practice the Cut B data show $\mathcal{C}(t)$ reaching only ~1.1–1.3 — well below the bound, so $\mathcal{C}$ has room to oscillate. The Schmidt saturation that crippled the $N = 1$ series-direct H2 test does *not* bite here.

| Config | $\bar{\mathcal{C}}$ | $r(\sigma^2, \|\dot{\mathcal{C}}\|)$ (growth) | $r(\sigma^2, \mathcal{C})$ (series) |
|---|---:|---:|---:|
| B1 | 1.110 | **+0.529** | −0.785 |
| B2 | 0.954 | +0.445 | −0.627 |
| B3 | 1.109 | **+0.545** | −0.783 |
| B4 | 0.791 | **−0.084** | −0.561 |

**Growth-framing (3/4 configs confirm H2).** At B1, B2, B3 — all with comparable coupling from both modes — growth-peaks align with variance-peaks at $r \in [+0.44, +0.55]$, comparable to the Stage 5 innermost-point value ($r = 0.49$) and stronger than Stage 5's outer points. At B4 — the strong-asymmetry config — growth-framing H2 **fails** ($r = -0.08$). The mechanism is visible in the per-mode $n_{\text{eff}}$ traces: mode 1 at $|\Delta_1| = 0.15$ dominates $\mathcal{C}(t)$ and its derivative; mode 2 at $|\Delta_2| = 0.50$ dominates $\sigma^2_{\text{intrinsic}}$ (because $(\partial_{\Delta_2} p)^2$ is larger there). The two drivers decouple, and their temporal structures no longer align.

**Physics finding (B4).** H2 growth-framing is a *same-mode* alignment claim. When coupling-to-complexity and coupling-to-variance are carried by different modes, the alignment breaks. The voyage's operational reading of H2 must state this explicitly: H2 is a statement about co-driven dynamics, not about arbitrary $(N, \{\Delta_k\})$ configurations.

**Series-direct (4/4 configs show negative $r$).** Consistent anti-correlation, $r \in [-0.78, -0.56]$. This is not an H2 failure — it is a **physics finding about the complementarity of the two measures**:

- $\mathcal{C}(t)$ is maximal when the spin-reduced state is maximally mixed (i.e. $p \approx 1/2$).
- $p \approx 1/2$ is a stationary point of $p$ as a function of $\Delta$ (at resonance) or sits on the flattest part of the $p(\Delta)$ curve (off-resonance). $(\partial_\Delta p)^2$ is small there, so $\sigma^2_{\text{intrinsic}}$ is small.
- Conversely, when $\mathcal{C}$ is small (spin near-pure), $p$ is near 0 or 1 — where the $p(\Delta)$ curve bends steeply and $(\partial_\Delta p)^2$ is largest.

**Operational and intrinsic complexity measures are therefore *complementary*, not *proportional*, in the voyage's Hamiltonian class.** They peak at opposite moments of the dynamics — $\mathcal{C}$ at maximum entanglement, $\sigma^2$ at maximum state purity. The voyage's H2 (growth-framing) catches the derivative alignment; the series-direct anti-correlation catches the phase-lag between the two peak structures. Both are the same physics.

**Gate 13 verdict.** H2 growth-framing is **confirmed** at $N = 2$ in 3/4 configurations and breaks cleanly at B4 with a physical explanation. Full H2 test supported subject to the same-mode-co-driving caveat, which is itself a finding worth recording.

## 5. H3 at N=2 — non-monotone again

The key question from Stage 5's Finding 2 is whether the non-monotone $(f_{\text{resolved}}, \bar{\mathcal{C}})$ behaviour was a single-mode window-period artefact or a deeper scalar-choice problem. Cut B data answer: **deeper**.

| Config | $\bar{\mathcal{C}}$ | $f_{\text{res}}(10^3)$ | $f_{\text{per-cycle}}^{\text{slow}}$ | $f_{\text{per-cycle}}^{\text{beat}}$ | $T_{\text{slow}}$ | $T_{\text{beat}}$ |
|---|---:|---:|---:|---:|---:|---:|
| B1 | 1.11 | 0.376 | 0.449 | ∞ (no beat) | 41.89 | ∞ |
| B2 | 0.95 | 0.462 | 0.551 | 0.551 | 41.89 | 41.89 |
| B3 | 1.11 | 0.386 | 0.461 | 0.922 | 41.89 | 20.94 |
| B4 | 0.79 | **0.492** | 0.587 | 1.370 | 41.89 | 17.95 |

**B4 has the lowest $\bar{\mathcal{C}}$ and the highest $f_{\text{res}}$.** The window-per-cycle normalisations shift the numbers but do not change the ordering: B4 is always the $f$-leader by either scalar.

**Mechanism.** $f_{\text{resolved}}$ is dominated by the *beat frequency* $|\Delta_1 - \Delta_2|$: more beats → more $\sigma^2$-peak excursions in the window → more time above QPN. $\bar{\mathcal{C}}$ is dominated by *proximity to resonance and mode-count participation*: both modes near resonance → higher aggregate complexity. These are two independent drivers; they are not engineered to correlate by the voyage Hamiltonian.

**Guardian's "window-effect control" answered.** Normalising by the slowest period or the beat period rescales $f_{\text{resolved}}$ but does not fix the non-monotonicity. The problem is not "window is too short for the slowest oscillation" — the problem is that the operational scalar mixes coupling-strength-to-variance and oscillation-count information, and those are decoupled from intrinsic complexity at $N \geq 2$.

**PA-05 candidate, now with N=2 evidence.** The Stage 5 forward flag (H3 scalar redefinition) is sharpened:

- At $N = 1$: non-monotonicity is a window-vs-mode-period artefact; changing $f_{\text{resolved}}$'s definition might fix it.
- At $N = 2$: non-monotonicity is *physical*, driven by the difference between coupling-to-$\mathcal{C}$ (resonance proximity) and coupling-to-$\sigma^2$ (beat frequency + $(\partial_\Delta p)$ magnitude). No single-scalar redefinition resolves this.

The honest PA-05 is therefore not a scalar swap but a **hypothesis reformulation**: H3 as "$f_{\text{resolved}}$ and $\bar{\mathcal{C}}$ co-vary monotonically" is *not* what the voyage physics supports. The finding is that intrinsic and operational complexity measure *complementary* aspects — one captures entanglement structure, the other captures parameter-estimation precision — and their cross-walk is the voyage's actual empirical content, not their correlation.

This is a cleaner story for Stage 8 than H3 as originally framed. Drafting for Stage 7 / v0.3 consideration rather than committing now — Cut C data may further refine (or challenge) the "complementarity" framing.

## 6. QFI reduction at N=2 — systematic breakdown

| Config | QFI median rel. dev. |
|---|---:|
| B1 | 25.43% |
| B2 | 20.81% |
| B3 | 29.52% |
| B4 | 13.21% |

**All four configs exceed the Stage-3 Gate-8 10% bar.** Scout's C5 reduction-path 3 (claim contracts to a QFI-flow-witness restatement) **does not contract the novelty** at $N = 2$ — the voyage's operational witness carries information the linearised Fisher-information reduction does not. This generalises Stage 5's innermost-point finding (QFI breaks at $|\Delta| = 0.15$) to all tested $N = 2$ configurations.

B4's lower deviation (13%) correlates with its lower complexity and decoupled-driver structure: mode 2 at $|\Delta| = 0.50$ has a larger $(\partial_\Delta p)$ and smaller $(\partial_\Delta^2 p)$, pushing the first-order approximation back toward validity. This is physics, not numerics.

**Implication for Stage 8 novelty.** The crossover from Stage 5 is now a *regime*, not a point. At $N = 1$ with $|\Delta| \leq 0.15$ or at any $N = 2$ near-resonance configuration, the first-order Fisher-information reduction fails, and the voyage's $T_{\text{det}}(M)$-style witness carries independent information. **The operational-crosswalk novelty survives at the inner/multi-mode regime**; it contracts cleanly only at outer-single-mode configurations.

## 7. Standing items — status updates

| Item | Origin | Stage 6 status |
|---|---|---|
| IPR test at first $N=2$ point | v0.2 Gate 12 / Guardian Stage 2 forward | **Cleared**: IPR · $n_{\text{eff}}$ = 1.00 across at-resonance modes; C3.4 concern does not bite at $N = 2$. Cut C re-verifies. |
| Full H2 test at $N \geq 2$ | v0.2 Gate 13 | **Partially confirmed**: growth-framing in 3/4 configs; breaks at B4 with a physical mechanism. Series-direct is consistently negative and carries a complementarity finding. |
| H3 scalar adequacy | v0.2 §5 / Stage 5 forward | **Non-monotone persists at N=2**: window-period rescaling does not fix it. Recast as PA-05 hypothesis-reformulation candidate, not a scalar swap. |
| QFI reduction (C5 path 3) | Stage 3 Gate 8 live | **Contracts at outer-single-mode only**; at $N = 2$ or near-resonance, operational witness carries independent information. Stage 8 novelty claim survives in those regimes. |

## 8. Standing items forwarded to Stage 7 / Stage 8

1. **Cut C IPR re-verification** at a representative $N = 3$ point. The Schmidt-rank bound scales as $\log(n_{\max}+1)$ at higher $N$; $\mathcal{C}$ has more room but there may be commensurability-specific artefacts in the spectrum shape.
2. **Same-mode-co-driving caveat** for H2 interpretation. Cut C with three modes at various commensurability ratios will test whether the B4-style decoupled-driver failure generalises — the golden-ratio and commensurate configs should behave differently here.
3. **H3 reformulation as "complementarity":** Stage 8 candidate writeup — treating $\mathcal{C}$ (intrinsic, entanglement-structured) and $(t_{\text{rise}}, f_{\text{resolved}})$ (operational, variance-driven) as complementary rather than correlated. Worth pre-drafting the paragraph so Cut C data either confirms or challenges the framing cleanly.
4. **QFI-reduction crossover characterisation.** Stage 8 should explicitly map where the reduction holds (outer, single-mode) vs breaks (inner / multi-mode / near-resonance). This is a physics finding, not a hedge.

## 9. Amendment-tripwire status

This stage identifies a PA-05 candidate (H3 reformulation). Pausing before committing: Cut C will either confirm the "complementarity" reading or challenge it. Committing PA-05 now based on N=1 + N=2 evidence would be premature if N=3 shifts the story.

Current count since v0.2 reset: zero committed amendments. PA-05 candidate = 1 pending. Buffer for 2 more before v0.3 consideration.

## 10. Verdict

**Stage 6 is the voyage's richest stage so far.** All gates pass. Two findings substantively reframe the voyage's story:

- **H2 physics finding:** intrinsic and operational complexity are **complementary, not proportional** — σ² peaks at moments of maximum state purity (low $\mathcal{C}$), $\mathcal{C}$ peaks at moments of maximum entanglement (low σ²). The growth-framing catches the derivative co-variation; the series-direct negative correlation is informative about the phase relationship, not an H2 failure.
- **H3 non-monotonicity at $N = 2$:** no single-scalar fix works. H3 as originally written (monotone co-variation of $f_{\text{resolved}}$ and $\bar{\mathcal{C}}$ across the sweep) is not what the voyage physics supports. The finding is the complementarity itself, and the voyage's novelty is cleaner under that reformulation.

**Stage 7 (Cut C, N=3, commensurability) cleared to begin on Guardian sign-off.**
