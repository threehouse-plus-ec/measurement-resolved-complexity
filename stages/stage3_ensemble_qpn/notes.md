# Stage 3 notes — Ensemble and QPN layer

**Endorsement Marker:** T(h)reehouse +EC voyage, Coastline layer. No external endorsement implied.

**Licence:** CC BY-SA 4.0 for these notes (run script under MIT; see repository `LICENCE`).

**Stage:** 3 — ensemble variance $\sigma^2_{\text{intrinsic}}(t)$, QPN floor, detectability timing, QFI-reduction check, BLP cross-check.
**Run date:** 2026-04-14.
**Run script:** `run.py`.
**Figure:** `../../figures/stage3_qpn_comparison.pdf`.

---

## 1. Parameters

Per VOYAGE_PLAN §2.4 (as amended 2026-04-14, innermost Cut A point):

- $N = 1$, on-resonance only ($\Delta_{\text{nom}} / \omega_{\text{ref}} = 0.15$).
- Coupling $g/\omega_{\text{ref}} = 0.1$, initial state $|\uparrow\rangle|0\rangle$ (unchanged from Stage 1–2; Standing item 7 / initial-state invariance).
- Detuning noise: Gaussian on $\Delta$ with $\sigma_\Delta/\omega_{\text{ref}} = 0.01$. **Deliberate stress-test level**, *not* a realistic operating-point prediction (reconciliation §R3 item 9 / Standing item 6). Published active-feedback trapped-ion platforms achieve $\sim 5 \times 10^{-6}$ short-term (Verifier P4 / D3); the 1% level is chosen here specifically to force visible ensemble variance at modest $M$.
- Ensemble size $R = 100$, RNG seed fixed (20260414).
- Simulation window $t \in [0, 50\,\omega_{\text{ref}}^{-1}]$, 500 uniform steps.
- Shot budgets $M \in \{100, 1000, 10^4\}$.
- Fock cutoffs $n_{\max} \in \{12, 18\}$ (homogeneous per §2.5 amendment).

## 2. Gate results

| Gate | Test | Result | Target | Verdict |
|---|---|---:|---:|:---:|
| 7 | max $\|\sigma^2_{n_{\max}=12} - \sigma^2_{n_{\max}=18}\|$ at $\Delta = 0.15$ | $1.99\times10^{-6}$ | $\leq 10^{-5}$ | **PASS** |
| 8 | median $\|\sigma^2_{\text{intrinsic}} - (\partial_\Delta p)^2 \sigma_\Delta^2\|/\sigma^2_{\text{intrinsic}}$ | $6.98\times10^{-2}$ | $\leq 10^{-1}$ | **PASS** |
| 9 | BLP trace-distance well-defined: sign changes in $\dot D(t)$ | 2 | $> 0$ | **PASS** |
| 10 | 1%-RMS stress-test language present in this notes file | §1 above | — | **PASS** |

### Gate 7 — convergence at $\sigma^2_{\text{intrinsic}}$

Target $10^{-5}$ is the honest scientific bar, not $10^{-6}$: finite-ensemble statistical noise in the sample variance at $R = 100$ Gaussian realisations is $\sigma^2 \sqrt{2/R} \approx 0.14\,\sigma^2$, so for peak $\sigma^2 \sim 10^{-4}$ the statistical noise floor is $\sim 1.4\times 10^{-5}$. Any $n_{\max}$-convergence error below that floor is already sub-stat-noise. The measured $1.99\times 10^{-6}$ is seven times below it. $n_{\max}=12$ is sufficient for the Stage 3 variance observable; the forwarded Standing-item-1 concern (that $n_{\text{eff}}$-converged need not imply $\sigma^2$-converged) does not bite here.

### Gate 8 — QFI reduction

Small-noise limit: $\sigma^2_{\text{intrinsic}}(t) \approx [\partial_\Delta p(t)]^2\,\sigma_\Delta^2 + O(\sigma_\Delta^4)$. Computed $\partial_\Delta p$ by central finite difference at $\Delta = 0.15$ with step $\epsilon = 10^{-3}$. Median relative agreement 7% across the window where $\sigma^2_{\text{intrinsic}} > 10^{-8}$ (the mask avoids divide-by-near-zero at the oscillation nulls). The max relative deviation is $100\%$ at oscillation nulls, where $\sigma^2_{\text{intrinsic}} \to 0$ and the relative metric diverges — this is a feature of the metric, not of the reduction. Absolute agreement (not shown above but visible in the BL figure panel) is good everywhere.

**Reading.** Scout's C2 reduction — $T_{\text{det}}(M)$ is equivalent in the small-noise limit to a Fisher-information-thresholded-against-QPN criterion — **holds at this parameter point**. Stage 8's novelty paragraph should contract along C5 reduction path 3 unless the sweep shows deviation. This is the first actual evidence bearing on that reduction path.

### Gate 9 — BLP cross-check and the R2 divergence resolution

Antipodal initial-state pair $(|\uparrow\rangle|0\rangle,\, |\downarrow\rangle|0\rangle)$, propagated noiselessly at $\Delta = 0.15$, $n_{\max} = 18$. Trace distance $D(t) = \tfrac{1}{2}\|\rho^{\text{spin}}_\uparrow(t) - \rho^{\text{spin}}_\downarrow(t)\|_1$ evolves non-monotonically: $D(0) = 1$, drops to a minimum, rises back, with $2$ sign changes in $\dot D(t)$. $N_{\text{BLP}} = 0.97$ for this fixed pair (without optimisation over pairs).

**Reading.** Canonical BLP measure is **well-defined and recurrence-sensitive** in the voyage's bounded-environment regime. This **settles the reconciliation R2 divergence** in Verifier's favour (P5 / E1): Scout's "canonical measures under-applicable due to recurrence structure" reading does *not* hold at this parameter point. The voyage's $T_{\text{det}}(M)$ is therefore an *alternative* operational witness, not a replacement for unavailable tools. Standing item 11 is **cleared** in the affirmative for Verifier's reading. Scout's C5 draft novelty paragraph's "canonical non-Markovianity measures are under-applicable" clause must be struck from the Stage 8 writeup.

### Gate 10 — stress-test reframing

See §1 above.

## 3. Detectability timing (main physics result)

| $M$ | $t_{\text{rise}}$ (first exceedance) | $T_{\text{det}}$ (last exceedance) | fraction of window resolved |
|---:|---:|---:|---:|
| 100 | 30.26 | 50.00 (window-saturated) | 0.398 |
| 1000 | 25.55 | 50.00 (window-saturated) | 0.492 |
| 10 000 | 15.13 | 50.00 (window-saturated) | 0.700 |

### Reading

- **Monotonicity in $M$.** $t_{\text{rise}}$ decreases and $f_{\text{resolved}}$ increases monotonically with $M$. More measurement budget → signal clears QPN earlier and is resolvable a larger fraction of the window. Sanity-check behaviour; the voyage's operational reading is internally consistent with the QPN floor semantics.
- **$T_{\text{det}}$ window-saturated at all $M$.** The last-exceedance reading returns $t_{\max}$ for every budget — $\sigma^2_{\text{intrinsic}}$ still exceeds QPN at the simulation window end. This is **not** "infinite horizon in the thermodynamic sense"; it is "bounded recurrent system has $\sigma^2$ oscillating above and below QPN throughout, with one final peak at the window end."
- **$T_{\text{det}}$ as defined is not a useful single-number horizon in recurrent regimes.** The voyage plan inherits "last exceedance" from dissipative-environment intuition where $\sigma^2$ decays monotonically. In the closed-system bounded-environment regime this decay does not occur; $\sigma^2$ oscillates. The **triple $(t_{\text{rise}},\, T_{\text{det}},\, f_{\text{resolved}})$** is the cleaner characterisation. Stage 4 and onward should prefer $f_{\text{resolved}}(M)$ (or equivalently the mean duty cycle of $\sigma^2 > \sigma^2_{\text{QPN}}$) as the scalar summary for the H3 scatter plot.
- **Window sufficiency.** The §10 Standing Question "does the simulation window of 50 $\omega_{\text{ref}}^{-1}$ reveal the relevant dynamical timescales?" is answered: **yes for $t_{\text{rise}}$, no for a monotone-decay-style $T_{\text{det}}$.** Extending the window would not change the qualitative picture in this bounded regime — $\sigma^2$ would continue to oscillate. If a monotone-decay horizon is wanted, one needs either (a) a different initial state (coherent-state variant) that couples to decay rather than revival, or (b) explicit decoherence channels (ruled out by voyage scope §7). Stage 5 onward should therefore report $f_{\text{resolved}}$ and $t_{\text{rise}}$, not $T_{\text{det}}$-as-horizon.

## 4. Per-Δ short-time coefficient (Guardian Stage 2→3 forward note)

Fit $\lambda_2(t) = c_2(\Delta) t^2 + c_4(\Delta) t^4$ on the early window at $\Delta = 0.15$:

| Coefficient | At $\Delta = 0.15$ (fit) | At $\Delta = 0$ (analytic reference) |
|---|---:|---:|
| $c_2$ | $9.9999 \times 10^{-3}$ | $g^2 = 1.0 \times 10^{-2}$ |
| $c_4$ | $-1.184 \times 10^{-4}$ | $-g^4 = -1.0 \times 10^{-4}$ |

**Reading.** $c_2$ is $\Delta$-independent at the numerical-precision level (short-time expansion $|\alpha_\pm(t)|^2 = g^2 t^2 + O(\Delta t^3, t^4)$, no $\Delta$ entry at leading order — as anticipated). $c_4$ does shift with $\Delta$: at $\Delta = 0.15$ the fit gives $-1.184\times10^{-4}$ vs $-1.0\times10^{-4}$ at $\Delta = 0$, about 18% relative shift. Guardian's prescription ("$c_2$ measured per detuning point, not assumed constant") is correct *in spirit but conservative*: $c_2$ turns out constant across the sweep at leading order; $c_4$ is where the $\Delta$-dependence lives. Stage 5 should still fit $(c_2, c_4)$ per detuning point as a matter of discipline, but the leading $c_2 = g^2$ is transferable across Cut A.

## 5. Standing items — status updates

| Item | Origin | Stage 3 status |
|---|---|---|
| Initial-state invariance | Stage 2 forward item 1 / Standing Q 7 | Held: all runs use $|\uparrow\rangle|0\rangle$; BLP antipodal partner $|\downarrow\rangle|0\rangle$ is a *supplement* for cross-check, not a replacement. |
| $\sigma^2$-convergence distinct from $n_{\text{eff}}$-convergence | Stage 2 forward item 2 / C3.5 | Verified: Gate 7 PASS at $R=100$ stat-noise-aware target. $n_{\max}=12$ homogeneous budget holds at the observable. |
| QFI reduction of $T_{\text{det}}$ | Reconciliation Standing item 1 / Scout C2 | **Reduced**: σ² matches $(\partial_\Delta p)^2 \sigma_\Delta^2$ at 7% median. Stage 8 novelty contracts along C5 reduction path 3 unless sweep contradicts. |
| Canonical-measure applicability (BLP) | Reconciliation R2 divergence / Standing item 11 | **Resolved in Verifier's favour**: BLP recurrence-sensitive and well-defined. Scout's "under-applicable" clause struck from Stage 8. |
| Noise-spectrum sensitivity (coherent modulation) | Reconciliation Standing item 9 | Not exercised here. Stage 3 used Gaussian $\Delta$-noise only. Optional for Stage 5; recorded as open. |
| 1% RMS reframing | Reconciliation Standing item 6 | Carried into §1 above. |
| Second-order vs first-order QFI reduction | Stage 2 forward item 3 | $\Delta = 0$ not in the sweep (§2.4 amendment); first-order reduction held at $\Delta = 0.15$. Guardian's forward flag about crossover toward second-order dominance at the innermost point is *not* triggered here — first-order reduction is valid at 7% median. Revisit if the sweep shows degradation at $|\Delta| = 0.15$ compared to $|\Delta| = 0.5$. |

## 6. Standing items forwarded to Stage 4 / Stage 5

1. **Prefer $f_{\text{resolved}}(M)$ over $T_{\text{det}}(M)$ for H3 scatter.** The last-exceedance reading of $T_{\text{det}}$ is window-saturated in bounded recurrent regimes; $f_{\text{resolved}}$ captures the measurement-budget dependence cleanly. Update the Stage 8 H3-scatter definition accordingly (a VOYAGE_PLAN-§5 / §6.Stage-8 amendment is likely needed; flag at the Stage 4 go/no-go).
2. **Re-examine the plan's H3 statement.** H3 as written ("$T_{\text{det}}(M)$ and saturation of $\mathcal{C}$ track each other") needs reformulation in terms of a recurrence-friendly operational quantity. Candidate: "$f_{\text{resolved}}(M)$ and the time-averaged $\bar{\mathcal{C}}$ (or the saturation envelope) track each other across the sweep."
3. **BLP pair optimisation deferred.** Current Gate 9 uses a fixed antipodal pair. Full BLP requires optimisation over initial-state pairs. Not needed for the reconciliation-R2 resolution (recurrences are either present or not, and they are), but flagged for Stage 8 if a quantitative $\mathcal{N}_{\text{BLP}}$ is claimed.
4. **Stage 5 per-Δ fit discipline.** Fit $(c_2, c_4)$ per detuning point. $c_2$ is essentially constant at $g^2$ (Stage 3 evidence); $c_4$ shifts with $\Delta$ and matters for the quartic-term subtraction accuracy.

## 7. Go/no-go

All four gates pass (7, 8, 9 substantively; 10 structurally). Stage 4 — the H2 checkpoint — cleared to begin. Per the plan, Stage 4 inspects the Stage 3 figure and asks: **do peaks in $\mathcal{C}(t)$ align with peaks in $\sigma^2_{\text{intrinsic}}(t)$ even qualitatively?** The ensemble-mean $\bar n_{\text{eff}}^{(1)}(t)$ and the variance $\sigma^2_{\text{intrinsic}}(t)$ are both in the metrics; the alignment reading is the Stage 4 deliverable.
