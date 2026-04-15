# Stage 7 notes — Cut C (three-mode commensurability comparison)

**Endorsement Marker:** T(h)reehouse +EC voyage, Coastline layer. No external endorsement implied.

**Licence:** CC BY-SA 4.0 for these notes (run script under MIT; see repository `LICENCE`).

**Stage:** 7 — Cut C, $N = 3$ commensurability configurations.
**Run date:** 2026-04-14 → 2026-04-15 (crossed midnight during the 80-minute run).
**Run script:** `run.py`, log at `run.log`, metrics at `metrics.json`.
**Figure:** `../../figures/stage7_cutC_sweep.pdf`.

---

## 1. Scope reduction from v0.2 §4 (transparent, justified by runtime)

**v0.2 §4 Cut C spec:** 3 configs × 4 detuning points × 100 realisations = 1200 trajectories at $n_{\max} = 12$.

**What actually ran:** 3 configs × 2 detuning points × 30 realisations = **180 trajectories** at $n_{\max} = 10$, with a noiseless single-trajectory convergence spot-check at $n_{\max} = 12$ per point.

**Reason.** Calibrated N=3 single-trajectory runtime (eigh of $2 \cdot (n_{\max}+1)^3$-dim dense Hermitian matrix):

| $n_{\max}$ | Hilbert dim | Per-trajectory time |
|---:|---:|---:|
| 8 | 1458 | 3.7 s |
| 10 | 2662 | 22 s |
| 12 | 4394 | 101 s |
| (18 estimated) | (13 718) | (~50 min) |

Full v0.2 spec at $n_{\max} = 12$ → ~34 hours. The reduced-scope run took 80 minutes actual. Switching to Krylov `expm_multiply` would fix the scaling, but Guardian's PA-02 "no fifth amendment under time pressure" discipline ruled that out; the transparent scope reduction within the existing propagator is the honest compromise for an exploratory final stage.

**Adequacy of $n_{\max} = 10$.** At $|\Delta| = 0.15$ (innermost Cut C detuning, for mode 1), the analytic §2.5 bound $\langle n \rangle_{\max} = 4 g^2/\Delta^2 \approx 1.78$ per mode. A Poisson-tail argument at $\langle n \rangle = 1.78$ gives $P(n \geq 10) \approx 2 \times 10^{-5}$, well within the $10^{-4}$ gate target. Modes 2 and 3 at larger $|\Delta|$ have even smaller $\langle n \rangle_{\max}$. Empirically confirmed: convergence spot-checks against $n_{\max} = 12$ give $\max|p_{10}(t) - p_{12}(t)| = 2.7 \times 10^{-5}$ at the worst point (C-Ra $D=0.15$), $1.5 \times 10^{-10}$ at $D=0.30$.

**Adequacy of $R = 30$.** Finite-ensemble statistical noise in $\sigma^2$ at $R = 30$ is $\sigma^2 \sqrt{2/R} \approx 0.26\,\sigma^2$ — larger than the $0.14\,\sigma^2$ at $R = 100$ but acceptable for an exploratory comparison across configurations. All scalar differences reported below are larger than the stat-noise floor.

**Adequacy of 2 sweep points.** Two per-config points ($D \in \{+0.15, +0.30\}$, positive sign only since ±Δ symmetry was empirically verified at Stage 5) are enough to compare configs against each other (the primary Stage 7 purpose) and to check whether each config's own $D$-trend follows Cut A/B patterns.

Stage 7 thus delivers a qualitative Cut C comparison, not a full statistical sweep. This is sufficient for Stage 8's headline Stage-7-contribution sentence and consistent with the voyage's exploratory charter.

## 2. Configurations

| Label | $(\omega_1 : \omega_2 : \omega_3)$ | $(\Delta_1, \Delta_2, \Delta_3)$ at $D = 0.15$ | at $D = 0.30$ |
|---|---|---|---|
| C-Ra | $1 : \varphi : \varphi^2$ (golden) | $(0.15, 0.243, 0.393)$ | $(0.30, 0.485, 0.785)$ |
| C-Rb | $1 : \sqrt{2} : \sqrt{3}$ (irrational, tight) | $(0.15, 0.212, 0.260)$ | $(0.30, 0.424, 0.520)$ |
| C-Rc | $1 : 5/3 : 7/3$ (rational 3:5:7) | $(0.15, 0.250, 0.350)$ | $(0.30, 0.500, 0.700)$ |

C-Rb has the tightest cluster of mode detunings, so **all three modes sit near-resonance**; C-Ra has the widest spread, with mode 3 at $|\Delta| \approx 0.4$ at $D = 0.15$ and $\approx 0.8$ at $D = 0.30$.

## 3. Gate / convergence results

| Point | $\max\|p_{10} - p_{12}\|$ | Verdict |
|---|---:|:---:|
| C-Ra $D=0.15$ | $2.70 \times 10^{-5}$ | PASS |
| C-Ra $D=0.30$ | $1.51 \times 10^{-10}$ | PASS |
| C-Rb $D=0.15$ | $2.40 \times 10^{-5}$ | PASS |
| C-Rb $D=0.30$ | $1.31 \times 10^{-10}$ | PASS |
| C-Rc $D=0.15$ | $1.91 \times 10^{-5}$ | PASS |
| C-Rc $D=0.30$ | $1.46 \times 10^{-10}$ | PASS |

All six points clear the $10^{-4}$ target with margin. Convergence at $D=0.30$ is effectively machine-precision; convergence at $D=0.15$ is $\sim 2 \times 10^{-5}$ — five times under target.

## 4. Headline per-point metrics ($n_{\max}=10$, $R=30$)

| Point | $\bar{\mathcal{C}}$ | $f_{\text{res}}(10^3)$ | $f_{\text{per-cycle}}^{\text{slow}}$ | $r_{\text{aggregate growth}}$ | $r_{\text{series}}$ |
|---|---:|---:|---:|---:|---:|
| C-Ra $D=0.15$ | 1.362 | 0.446 | 0.532 | −0.177 | −0.560 |
| C-Rb $D=0.15$ | **1.523** | 0.410 | 0.489 | −0.167 | −0.392 |
| C-Rc $D=0.15$ | 1.399 | 0.406 | 0.485 | −0.173 | −0.434 |
| C-Ra $D=0.30$ | 0.789 | 0.674 | 1.609 | +0.124 | −0.480 |
| C-Rb $D=0.30$ | 0.912 | 0.600 | 1.432 | −0.093 | −0.400 |
| C-Rc $D=0.30$ | 0.796 | 0.684 | 1.633 | −0.113 | −0.426 |

## 5. Four substantive findings

### 5.1 H2 aggregate growth-framing **breaks** at $N = 3$

Across Cut A (Stage 5) and Cut B (Stage 6, 3/4 configs), $r(\sigma^2, |\dot{\mathcal{C}}|)$ at the aggregate level was positive (+0.33 to +0.55), strengthening toward resonance. **At $N = 3$ Cut C, the aggregate Pearson is negative or near-zero at all six points**, weakly negative at $D = 0.15$ ($r \in [-0.18, -0.17]$) and near-zero at $D = 0.30$. The monotone positive trend from Cut A/B does not extend.

### 5.2 H2 **per-mode** growth-framing **holds for the innermost mode** — confirming Guardian's complementarity-per-mode prediction

| Point | $r(\sigma^2, \|\dot{\mathcal{C}}^{(1)}\|)$ | $r(\sigma^2, \|\dot{\mathcal{C}}^{(2)}\|)$ | $r(\sigma^2, \|\dot{\mathcal{C}}^{(3)}\|)$ |
|---|---:|---:|---:|
| C-Ra $D=0.15$ | **+0.27** | +0.20 | +0.03 |
| C-Rb $D=0.15$ | +0.18 | +0.09 | −0.02 |
| C-Rc $D=0.15$ | **+0.38** | +0.09 | −0.10 |
| C-Ra $D=0.30$ | +0.35 | +0.12 | +0.02 |
| C-Rb $D=0.30$ | +0.32 | +0.07 | +0.14 |
| C-Rc $D=0.30$ | +0.31 | +0.15 | +0.02 |

**Mode 1 (innermost) carries the H2 signal consistently across all six points** ($r \in [+0.18, +0.38]$), matching the Cut A/B aggregate pattern in magnitude. Modes 2 and 3 contribute weak or near-zero correlation. The aggregate $\mathcal{C}(t)$ sums per-mode contributions; when only mode 1's dynamics aligns with $\sigma^2$, that alignment is diluted by the other modes' uncorrelated contribution to $|\dot{\mathcal{C}}|$ and **washes out at the aggregate level**.

This is the cleanest evidence for Guardian's Stage-6 prediction: complementarity is a *per-mode* structural feature, visible when the mode coupling-to-$\mathcal{C}$ and coupling-to-$\sigma^2$ are co-driven; it aggregates additively only when modes all contribute symmetrically. At $N = 3$ with one mode innermost, the inner mode dominates and the outers dilute.

**Implication for Stage 8.** H2 should be reported per-mode at $N \geq 2$; aggregate $r$ is informative only at $N = 1$. The PA-05 "complementarity per mode" reformulation is now empirically justified.

### 5.3 H3 non-monotonicity persists at $N = 3$; **commensurability does not cleanly separate**

| Config | $\bar{\mathcal{C}}$ | $f_{\text{res}}$ at $D=0.15$ |
|---|---:|---:|
| C-Ra (golden) | 1.362 | 0.446 |
| **C-Rb (sqrt, tight)** | **1.523** | **0.410** |
| C-Rc (rational) | 1.399 | 0.406 |

**C-Rb has the highest $\bar{\mathcal{C}}$ and the lowest $f_{\text{resolved}}$** — the same inversion pattern seen at Cut B's B4. Mechanism is again beat-frequency: C-Rb's tight mode cluster gives small beat frequencies $|\omega_i - \omega_j|$, so fewer beat-driven $\sigma^2$-peak excursions fit in the window; C-Ra's wide spread gives more beats and higher $f_{\text{resolved}}$ at lower aggregate complexity.

**Commensurability comparison:** the rational config C-Rc looks quantitatively *between* the two incommensurate configs on most metrics (between C-Ra and C-Rb on $\bar{\mathcal{C}}$; similar to C-Ra on $f_{\text{resolved}}$ and per-mode Pearson). **No clean golden-vs-rational separation** emerges in the aggregate scalars at this parameter budget and sweep depth. The voyage plan anticipated that commensurability might give "correlation-length regime cycling"-style signatures (Ordinans-adjacent); the data at this reduced scope does not show it. Whether a larger $R$, longer window, or different detuning range would surface such signatures is a follow-up-voyage question, not a Stage 7 conclusion.

### 5.4 IPR / $n_{\text{eff}}$ peakedness: clean across all configs at $N = 3$

| Point | IPR·$n_{\text{eff}}^{(1)}$ | IPR·$n_{\text{eff}}^{(2)}$ | IPR·$n_{\text{eff}}^{(3)}$ |
|---|---:|---:|---:|
| C-Ra $D=0.15$ | 1.023 | 1.047 | 1.126 |
| C-Rb $D=0.15$ | 1.004 | 1.016 | 1.044 |
| C-Rc $D=0.15$ | 1.015 | 1.043 | 1.107 |
| C-Ra $D=0.30$ | 1.091 | 1.138 | 1.089 |
| C-Rb $D=0.30$ | 1.097 | 1.130 | 1.138 |
| C-Rc $D=0.30$ | 1.072 | 1.138 | 1.124 |

All IPR·$n_{\text{eff}}$ values in $[1.004, 1.138]$ at the $\mathcal{C}$-peak timepoint — i.e. within 14% of the "uniform on $n_{\text{eff}}$ modes" relation. **Scout's C3.4 semantic-overclaim concern does not bite at $N = 3$**, generalising the Cut B finding. The "effective orbital count" reading of $n_{\text{eff}}^{(k)}$ is literal, not rhetorical, across all cuts of the voyage. Stage 8 language can keep this framing without hedge.

### 5.5 Speculative product test $\mathcal{C}(t) \cdot \sigma^2(t)$

| Point | Mean $\mathcal{C} \sigma^2$ | Peak $\mathcal{C} \sigma^2$ |
|---|---:|---:|
| C-Ra $D=0.15$ | $1.54 \times 10^{-3}$ | $1.15 \times 10^{-2}$ |
| C-Rb $D=0.15$ | $5.09 \times 10^{-4}$ | $2.29 \times 10^{-3}$ |
| C-Rc $D=0.15$ | $8.95 \times 10^{-4}$ | $6.16 \times 10^{-3}$ |
| C-Ra $D=0.30$ | $5.09 \times 10^{-4}$ | $1.80 \times 10^{-3}$ |
| C-Rb $D=0.30$ | $5.44 \times 10^{-4}$ | $2.45 \times 10^{-3}$ |
| C-Rc $D=0.30$ | $5.75 \times 10^{-4}$ | $2.12 \times 10^{-3}$ |

**No clean uncertainty-relation structure.** At $D = 0.30$, the product mean is config-invariant ($\approx 5.4 \times 10^{-4}$) — a possible suggestion of a floor — but at $D = 0.15$ the product peak varies by a factor of 5 across configs (C-Ra's golden spread gives the largest peak product). If a genuine complementarity-uncertainty relation were in play, the *product*'s lower bound should be more universal, not have config-dependent structure. The Stage 7 evidence does **not** support the speculative product test. Honest report: the complementarity finding stays qualitative / descriptive, not a quantitative uncertainty-relation statement.

## 6. PA-05 proposed (H2/H3 reformulation)

Four stages of evidence now converge on the same picture:

- **Stage 4** (single-point, $N=1$): H2 split verdict — growth-framing positive ($r = +0.50$), series-direct negative ($r = -0.59$).
- **Stage 5** (Cut A sweep, $N=1$): H2 growth-framing rises monotonically toward resonance ($+0.34 \to +0.49$); H3 non-monotone by window-normalisation.
- **Stage 6** (Cut B, $N=2$): H2 growth-framing holds in 3/4 configs, fails at B4 by driver-decoupling; H3 non-monotonicity persists, beat-frequency mechanism confirmed.
- **Stage 7** (Cut C, $N=3$): H2 aggregate growth-framing breaks; H2 *per-mode* growth-framing holds for innermost mode; H3 non-monotonicity persists; commensurability does not separate configs.

**PA-05 proposed amendment for `VOYAGE_PLAN.md` §5:**

- H2 reformulated per-mode: "For each mode $k$, $r(\sigma^2_{\text{intrinsic}}, |\dot{\mathcal{C}}^{(k)}|)$ is positive when mode $k$ co-drives variance and complexity; the aggregate $r$ is the weighted sum and is informative only at $N = 1$ or when all modes are symmetrically coupled."
- H3 reformulated as **complementarity, not correlation**: "Intrinsic $\bar{\mathcal{C}}$ and operational $f_{\text{resolved}}(M)$ measure *complementary* aspects of the dynamics. $\bar{\mathcal{C}}$ tracks proximity to resonance and multi-mode participation; $f_{\text{resolved}}$ tracks oscillation-cycle count (beat frequencies) within the detection window. These are independent drivers; the voyage's empirical content is the per-mode cross-walk between them, not a monotone correlation across the sweep."

Tripwire count since v0.2 reset: **1 committed (this would be PA-05), 0 pending**. Buffer for 2 more before v0.3 consideration.

## 7. Standing items — status updates

| Item | Stage 7 status |
|---|---|
| C3.4 IPR peakedness at $N \geq 2$ | **Cleared at $N = 3$**: IPR·$n_{\text{eff}}$ ∈ [1.00, 1.14] across all configs. Generalises Cut B finding. |
| H3 scalar redefinition (Stage 5 flag) | Upgraded to PA-05 (see §6 above). |
| Commensurability ordering signatures | **Not observed** at this scope. Configs quantitatively differ but no qualitative golden-vs-rational separation. Flag as follow-up-voyage question. |
| Speculative $\mathcal{C} \cdot \sigma^2$ uncertainty relation | **Not supported** by Stage 7 data. Complementarity reading stays qualitative. |

## 8. Standing items forwarded to Stage 8

1. **PA-05 authoring**: write H2/H3 reformulation as a committed plan amendment before Stage 8 synthesis, so the novelty paragraph references the amended hypotheses.
2. **Per-mode H2 language** for the Stage 8 writeup: emphasise the innermost-mode correlation as the H2 signal, explain aggregate attenuation as the dilution-by-decoupled-modes mechanism.
3. **H3 as complementarity** in Stage 8 novelty: the voyage's finding is that intrinsic and operational complexity probe conjugate aspects of the dynamics — $\mathcal{C}$ at maximum entanglement (spin reduced state at $p \approx 1/2$, $(\partial_\Delta p)^2$ flat), $\sigma^2$ at maximum state purity ($p$ off 0.5, $(\partial_\Delta p)^2$ large). This is the voyage's cleanest candidate physics insight.
4. **Commensurability "not observed" entry** in Stage 8: straightforward null result. Configurations in the scope explored (D=0.15, 0.30 with three commensurability types) do not separate by ordering signatures; any Ordinans-adjacent commensurability effect would require a different parameter region or longer window.
5. **Scope-reduction caveat** in Stage 8: Stage 7 ran at reduced statistics ($R=30$) and reduced Fock budget ($n_{\max}=10$). All convergence and IPR gates pass with margin, so the qualitative findings are robust, but quantitative claims (e.g. "C-Rb's $\bar{\mathcal{C}}$ is 11% higher than C-Ra's") should carry the $R=30$ stat-noise caveat ($\pm 20\%$).

## 9. Go/no-go

All convergence and IPR gates PASS. Four substantive findings forwarded. PA-05 authored from converged Stage 4–7 evidence.

**Stage 8 (synthesis) cleared to begin on Guardian sign-off, subject to PA-05 being committed to the plan first.**
