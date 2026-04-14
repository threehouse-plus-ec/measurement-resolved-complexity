# Stage 4 notes — H2 checkpoint

**Endorsement Marker:** T(h)reehouse +EC voyage, Coastline layer. No external endorsement implied.

**Licence:** CC BY-SA 4.0 for these notes (run script under MIT; see repository `LICENCE`).

**Stage:** 4 — H2 checkpoint (peak alignment of complexity and ensemble variance).
**Run date:** 2026-04-14.
**Run script:** `run.py`.
**Figure:** `../../figures/stage4_h2_checkpoint.pdf`.

---

## 1. Scope

Stage 4 is the voyage's H2 go/no-go (VOYAGE_PLAN §Stage 4, §5):
if peaks in $\mathcal{C}(t)$ align even qualitatively with peaks in $\sigma^2_{\text{intrinsic}}(t)$, proceed to Cut A; if not, stop and consult. The H2 text is

> *H2 (moderate): temporal alignment of peaks/shoulders in $\mathcal{C}(t)$ and $\sigma^2_{\text{intrinsic}}(t)$. Moments of rapid complexity growth coincide with moments of large ensemble variance.*

Run is inspection-only: re-uses the Stage 3 ensemble deterministically (same seed 20260414, $\Delta_{\text{nom}} = 0.15$, $\sigma_\Delta = 0.01$, $R = 100$, $n_{\max} = 18$).

## 2. Two H2-reading tests

**Direct series test** (a literal reading of "peaks in $\mathcal{C}(t)$"): compute peaks in $\mathcal{C}(t) = \log n_{\text{eff}}^{(1)}(t)$ and in $\sigma^2_{\text{intrinsic}}(t)$, compare their locations.

**Growth test** (the plan's *actual* text, "moments of *rapid* complexity growth"): compute $|\dot{\mathcal{C}}(t)|$, find its peaks, compare locations with the $\sigma^2$ peaks.

The two tests coincide only if $\mathcal{C}(t)$ is oscillatory. At $N=1$ it is not — $\mathcal{C}$ rises nearly monotonically to its Schmidt-rank-2 bound. So only the growth test carries weight here; the series test is structurally compromised.

## 3. Findings

### Signal structure (resolvable window, 474/500 pts)

| Quantity | Range |
|---|---|
| $\sigma^2_{\text{intrinsic}}(t)$ | $[1.06 \times 10^{-8},\; 1.79 \times 10^{-2}]$ |
| $\mathcal{C}(t)$ | $[0.2198,\; 0.6926]$ |
| $|\dot{\mathcal{C}}(t)|$ | $[1.93 \times 10^{-7},\; 1.20 \times 10^{-1}]$ |
| $\log 2$ (Schmidt-rank-2 bound at $N=1$) | $0.6931$ |
| $\mathcal{C}(t)_{\max} / \log 2$ | 0.9993 — **bound essentially saturated** |

### Growth-test alignment (the load-bearing one)

| Metric | Value |
|---|---:|
| number of $\sigma^2$ peaks (5% prominence) | 2 |
| number of $|\dot{\mathcal{C}}|$ peaks (5% prominence) | 2 |
| mean $|\text{lag}|$ ($\sigma^2$ peak to nearest $|\dot{\mathcal{C}}|$ peak) | $1.60\,\omega_{\text{ref}}^{-1}$ |
| mean $\sigma^2$ peak spacing | $10.92\,\omega_{\text{ref}}^{-1}$ |
| lag as fraction of spacing | $0.147$ |
| Pearson $r(\sigma^2, |\dot{\mathcal{C}}|)$ | $0.497$ |
| cross-correlation lag at max | $-1.30\,\omega_{\text{ref}}^{-1}$ ($\sigma^2$ leads $|\dot{\mathcal{C}}|$) |
| max normalised cross-correlation | $0.527$ |

**Reading.** Peaks in $|\dot{\mathcal{C}}|$ sit within 15% of the typical $\sigma^2$ peak spacing of the nearest $\sigma^2$ peak. Pearson correlation 0.50 confirms sustained co-variation. Cross-correlation lag of $-1.3\,\omega_{\text{ref}}^{-1}$ (small relative to the 10.9 peak spacing) indicates near-synchronous behaviour with $\sigma^2$ leading slightly. H2 holds in its growth-framing.

### Series test (secondary diagnostic)

| Metric | Value |
|---|---:|
| number of $\mathcal{C}(t)$ peaks (5% prominence) | 1 |
| Pearson $r(\sigma^2, \mathcal{C})$ | $-0.593$ |

**Reading.** Anti-correlation at $-0.59$. This is *not* a failure of H2 — it is a structural artefact: $\mathcal{C}(t)$ climbs monotonically to its $\log 2$ ceiling at $N=1$ (Schmidt bound), while $\sigma^2$ oscillates on top of a rising-then-saturating envelope. Once $\mathcal{C}$ is pinned at $\log 2$, any further "complexity dynamics" has no room at $N=1$ — the signal is carried entirely by $\sigma^2$. The negative correlation is the trace of this geometry, not evidence against H2.

### N=1 structural saturation

$\mathcal{C}(t)_{\max} / \log 2 = 0.9993$ — the N=1 Schmidt bound is reached to sub-percent. This is the dominant N=1-specific finding. H2, as a hypothesis about "complexity" having room to grow while variance witnesses that growth, is structurally *underdetermined* at $N=1$: complexity is capped at $\log 2$ by the $2$-dim spin partner, and the real test requires $N \geq 2$ where the bound loosens to $\log \min\bigl(n_{\max}+1,\, 2(n_{\max}+1)^{N-1}\bigr)$.

## 4. Verdict

**Proceed to Stage 5 (Cut A) with the following qualifications:**

1. **H2 is not cleanly testable at $N=1$.** The growth-framing gives positive co-variation ($r \approx 0.5$, peak-lag 15% of peak spacing), but the structural saturation of $\mathcal{C}$ to the Schmidt bound means the hypothesis is under-tested — the *magnitude* of co-variation, and whether it scales with $\Delta$ across Cut A, is the informative signal.
2. **H2 becomes genuinely testable at $N \geq 2$.** Stage 6 is where the Schmidt bound loosens enough for $\mathcal{C}$ to have non-trivial dynamical range. The Stage 4 verdict is therefore "proceed, but read H2 at Cut A as *pattern consistency across the sweep*, not *proof of concept at a single point*."
3. **Do not declare H2 failed from Stage 3 / 4 data alone.** The Stage 4 figure (top panel, red vs green vertical markers) shows growth-peaks sitting right next to variance-peaks, consistent with the growth-framing. A declaration of H2-failure would require either (a) absence of any peak alignment across the full sweep, or (b) Stage 6 showing no correspondence once the Schmidt cap is lifted. Neither condition is met.

## 5. Plan amendments flagged for v0.2

Two substantive amendments surface from Stages 3 and 4. Combined with the two uncommitted strike-through amendments from Stage 1 prep (see `../../PLAN_AMENDMENTS.md`), this trips the v0.2 tripwire Guardian set during Stage 1.

**Amendment flag A — H3 scalar reformulation ($T_{\text{det}}$ → $f_{\text{resolved}}$).**
From Stage 3: $T_{\text{det}}(M)$ as "last exceedance" is window-saturated in bounded recurrent regimes. The triple $(t_{\text{rise}}, T_{\text{det}}, f_{\text{resolved}})$ is the right characterisation; $f_{\text{resolved}}(M)$ is the cleanest scalar for the Stage 8 scatter. §5 H3 should be rewritten as:

> *H3 (strong, Ordinans-native): as detuning is swept through resonance, both $f_{\text{resolved}}(M)$ and the saturation envelope of $\mathcal{C}(t)$ (or a time-averaged $\bar{\mathcal{C}}$) scale in a correlated way across the sweep.*

The H3 scatter in §Stage 8 follows suit: $f_{\text{resolved}}(M = 1000)$ vs $\bar{\mathcal{C}}$, across all Cut A/B/C parameter points.

**Amendment flag B — H2 growth-framing and N=1 structural caveat.**
§5 H2 should be rewritten to make the growth-framing explicit (matching the plan's own words) and to acknowledge the N=1 Schmidt-bound caveat:

> *H2 (moderate): temporal co-variation between rapid complexity growth $|\dot{\mathcal{C}}(t)|$ and large ensemble variance $\sigma^2_{\text{intrinsic}}(t)$. At $N=1$ the Schmidt-rank-2 bound caps $\mathcal{C}$ at $\log 2$; H2 is under-tested at $N=1$ and becomes genuinely testable at $N \geq 2$. Stage 4 provides a pre-sweep confirmation that growth-peaks and variance-peaks align, not a full H2 verdict.*

Per Guardian's Stage 1 tripwire, these two amendments (plus the two uncommitted from Stage 1 prep) are the cue to issue **v0.2 of `VOYAGE_PLAN.md`** absorbing all four cleanly and archiving v0.1 per CD §0.8. Stage 4 flags the amendment; the v0.2 rewrite is a discrete task before Stage 5 launches.

## 6. Standing items forwarded to Stage 5

1. Report $f_{\text{resolved}}(M)$, $t_{\text{rise}}(M)$, and $T_{\text{det}}(M)$ per Cut A point (all three; $T_{\text{det}}$ as a diagnostic rather than a headline scalar).
2. Record $\bar{\mathcal{C}}$ (time-average over the resolvable window) and the saturation envelope per Cut A point. Stage 8's H3 scatter will use $\bar{\mathcal{C}}$ or the envelope, not instantaneous $\mathcal{C}$.
3. Continue the $|\dot{\mathcal{C}}|$ vs $\sigma^2$ Pearson tracking per Cut A point — the cross-sweep trend of this correlation is the real H2 evidence.
4. Per-Δ $(c_2, c_4)$ short-time fit per Cut A point (Guardian Stage 2 → 3 forward note, refined by Stage 3 finding that $c_2$ is Δ-constant at leading order but $c_4$ is not).

## 7. Go/no-go

Stage 4 clears Stage 5 to begin **subject to v0.2 of the plan being issued first**, so that Cut A runs against an H2/H3 formulation that actually matches the N=1 / bounded-recurrent physics. Stage 5 against the current v0.1 text is possible but would force a silent Stage-8 reframing of the same kind we committed not to do; v0.2 now, Stage 5 after.
