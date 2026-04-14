# Stage 2 notes — Observables layer

**Endorsement Marker:** T(h)reehouse +EC voyage, Coastline layer. No external endorsement implied.

**Licence:** CC BY-SA 4.0 for these notes (run script under MIT; see repository `LICENCE`).

**Stage:** 2 — reduced-state diagonalisation, von Neumann entropy, $n_{\text{eff}}^{(1)}(t)$.
**Run date:** 2026-04-14.
**Run script:** `run.py` (reproduces metrics below; writes `metrics.json`).
**Figure:** `../../figures/stage2_p_and_neff.pdf`.

---

## 1. Scope

Extends the Stage 1 propagator with the voyage's intrinsic complexity observable:

$$n_{\text{eff}}^{(k)}(t) \;=\; \exp\!\bigl(S_{\text{vN}}[\rho^{(k)}(t)]\bigr),\qquad \rho^{(k)}(t) = \mathrm{Tr}_{\bar k}|\Psi(t)\rangle\langle\Psi(t)|$$

At $N=1$ the bipartition is spin $\otimes$ mode. The spin partner is $2$-dimensional, so the Schmidt rank is bounded above by $2$ at all times; $n_{\text{eff}}^{(1)}(t) \in [1, 2]$. The bound saturates at $2$ (maximally-mixed spin reduced state, $\log 2$ entropy) when the spin-mode state is maximally entangled across the bipartition.

Per VOYAGE_PLAN §Stage 2 and reconciliation §R3 Standing items carried forward from Stage 1:

- Initial state fixed at $|\uparrow\rangle \otimes |0\rangle$, identical to Stage 1 (Standing item 7 — initial-state invariance across stages).
- Aggregate complexity $\mathcal{C}(t) = \sum_k \log n_{\text{eff}}^{(k)}(t)$ reported as the primary invariant (Standing item 2). Trivial at $N=1$ ($\mathcal{C}(t) = \log n_{\text{eff}}^{(1)}(t)$), but the reporting discipline is in place for Stage 6/7 where it becomes non-trivial.
- Convergence re-verified at the $n_{\text{eff}}$ observable (Standing item 1 / C3.5) — $p(t)$-converged does not imply $n_{\text{eff}}$-converged.

## 2. Runs

| Run | Δ/ω_ref | n_max | Purpose |
|---|---:|---:|---|
| A | 0.00 | 60 | Analytic anchor: closed-form $n_{\text{eff}}$ from Schmidt eigenvalues $\lambda_{1,2}(t) = (1 \pm e^{-2 g^2 t^2})/2$. Code-anchor, not a sweep point. |
| B12 | 0.15 | 12 | Innermost Cut A point, homogeneous default n_max. |
| B18 | 0.15 | 18 | Same point, convergence check cutoff. |

Parameters shared with Stage 1: $g/\omega_{\text{ref}} = 0.1$, simulation window $t \in [0, 50\,\omega_{\text{ref}}^{-1}]$, 500 uniform steps.

## 3. Gate results

| Gate | Test | Result | Target | Verdict |
|---|---|---:|---:|:---:|
| 4 | max $\|n_{\text{eff}}^{n_{\max}=12} - n_{\text{eff}}^{n_{\max}=18}\|$ at $\Delta=0.15$ | $1.74 \times 10^{-6}$ | $\leq 10^{-4}$ | **PASS** |
| 4a | max $\|n_{\text{eff}} - n_{\text{eff}}^{\text{analytic}}\|$ at $\Delta=0$, $n_{\max}=60$ | $8.88 \times 10^{-16}$ | $\leq 10^{-4}$ | **PASS** |
| 5 | rank $\rho^{(1)}(t=25)$ above $10^{-10}$ tolerance | 2 (both runs) | = 2 (Schmidt bound at $N=1$) | **PASS** |
| 6 | early-time fit $|c_2 - g^2|$, $\lambda_2 = c_2 t^2 + c_4 t^4$ | $1.81 \times 10^{-8}$ | $\leq 10^{-6}$ | **PASS** |

### Gate 4 — convergence at the observable

Gate 4a confirms the $n_{\text{eff}}$ machinery is exact at Δ=0 (matches the closed-form Schmidt-eigenvalue expression at machine precision). Gate 4 confirms that $p(t)$-converged is also $n_{\text{eff}}$-converged at the innermost Cut A detuning for the homogeneous $n_{\max}=12/18$ budget — the Standing-item-3 concern does not bite here at $N=1$.

### Gate 5 — spectrum inspection

Representative time $t = 25\,\omega_{\text{ref}}^{-1}$. Top eigenvalues:

| Run | $\lambda_1$ | $\lambda_2$ | $\lambda_3$ | $\lambda_4$ |
|---|---:|---:|---:|---:|
| A ($\Delta=0$, $n_{\max}=60$) | $5.00\times 10^{-1}$ | $5.00\times 10^{-1}$ | $9.25\times 10^{-17}$ | $7.36\times 10^{-17}$ |
| B18 ($\Delta=0.15$, $n_{\max}=18$) | $5.19\times 10^{-1}$ | $4.81\times 10^{-1}$ | $1.81\times 10^{-16}$ | $3.46\times 10^{-17}$ |

**Reading.** At $N=1$ the Schmidt rank is structurally bounded by the spin dimension (two). The spectrum is therefore literally two-peaked at every time, and the "effective orbital count" reading of $n_{\text{eff}}^{(1)}$ is literal rather than rhetorical — Scout's C3.4 concern does not apply at $N=1$. This is *not* a discovery; it is a structural property of the bipartition.

**Forward flag for Stage 6/7.** At $N \geq 2$ the Schmidt rank can grow up to $\min(n_{\max}+1,\, 2(n_{\max}+1)^{N-1})$, which is comfortably above two. Scout's C3.4 concern bites there: the spectrum's *shape* (peaked vs. spread) becomes informative about whether $n_{\text{eff}}$ can be read as an "effective count" or only as a summary scalar. Stage 6 should reinstate the spectrum-inspection gate with a non-trivial shape test (e.g. participation ratio $\bigl(\sum_j \lambda_j^2\bigr)^{-1}$ compared against $n_{\text{eff}}$).

### Gate 6 — short-time fit

Fit model $\lambda_2(t) = c_2 t^2 + c_4 t^4$, least-squares on $t \in (0.1, 0.5]\,\omega_{\text{ref}}^{-1}$ (first 1% of the simulation window).

| Coefficient | Fit | Analytic ($\Delta=0$ expansion) | Agreement |
|---|---:|---:|---:|
| $c_2$ | $9.99998 \times 10^{-3}$ | $g^2 = 1.00 \times 10^{-2}$ | $1.81 \times 10^{-8}$ |
| $c_4$ | $-9.976 \times 10^{-5}$ | $-g^4 = -1.00 \times 10^{-4}$ | $2.37 \times 10^{-7}$ |

Relative residual on the fit window: $1.78 \times 10^{-7}$.

**Stage 3 subtraction reference.** The short-time form of $\lambda_2$ at $\Delta = 0$ is $\lambda_2(t) = g^2 t^2 - g^4 t^4 + O(t^6)$ to machine precision. This is the "generic short-time behaviour" that Scout C3.3 recommends subtracting to read non-generic dynamical features. Stage 3 can subtract $c_2 t^2 + c_4 t^4$ with the numerical $(c_2, c_4)$ above (or analytic $g^2, -g^4$, equivalent) and expect any residual to be genuinely dynamical. A caveat: this coefficient pair is anchored at $\Delta=0$. At non-zero detuning the short-time expansion remains $\lambda_2 \sim g^2 t^2 + O(t^4, \Delta t^3)$ to leading order (as expected — $\alpha_\pm(t) \approx \mp i g t$ for $|\Delta t| \ll 1$ regardless of $\Delta$), but the sub-leading structure has $\Delta$-dependence. Stage 3's on-sweep data can re-fit per-Δ if the subtraction residual is sensitive.

Observation from the Gate 6 fit: the naive pure-$t^2$ fit (no $t^4$ term) with a wider window gave $c_2 = 9.58 \times 10^{-3}$, a four-percent deviation from $g^2$ driven by the truncated $t^4$ correction. The two-coefficient fit on a tighter window recovers both $c_2$ and $c_4$ at near-machine precision. This is recorded here because the same care will be needed in Stage 3's ensemble-variance subtractions.

## 4. Physics readings

- $n_{\text{eff}}^{(1)}(0) = 1$ (pure product initial state). Confirmed at machine precision.
- At $\Delta=0$: $n_{\text{eff}}^{(1)}(t) \to 2$ as $t \to \infty$, monotonic. Matches the Schmidt-rank-2 saturation ($\lambda_1 = \lambda_2 = 1/2$, entropy $\log 2$).
- At $\Delta=0.15$: $n_{\text{eff}}^{(1)}(t)$ oscillates with a bounded envelope $\leq 2$, consistent with the bounded mode amplitude $|\alpha|_{\max} = 2g/|\Delta|$ at this detuning. The reduced-state spectrum at $t=25$ sits at $(0.52, 0.48)$ — close to but not quite at the equal-weight limit, as expected.
- Aggregate complexity $\mathcal{C}(t) = \log n_{\text{eff}}^{(1)}(t)$: peaks near $\log 2 = 0.693$ at the maximally-entangled configuration.

**On Guardian's prediction (spectrum "not peaked on few eigenvalues").** The Guardian-hypothesised scatter-across-many-Fock-components reading applies to the *Fock-basis representation* of $\rho^{(1)}$, which is indeed spread across $\sim (g t)^2 / \Delta^2$ components. The *eigenvalue spectrum* of $\rho^{(1)}$, however, is bounded to rank $2$ at $N=1$ by the Schmidt decomposition against the $2$-dim spin partner. The two views do not contradict — they measure different things. For the voyage's $n_{\text{eff}}^{(k)}$ definition (which uses the eigenvalue spectrum), the structural bound dominates at $N=1$. The Fock-spread view becomes observable-relevant at Stage 6/7 when per-mode bipartitions expose $(n_{\max}+1)$-dimensional partner spaces.

## 5. Standing items forwarded to Stage 3

1. **Short-time subtraction reference.** Use $\lambda_2(t) \approx c_2 t^2 + c_4 t^4$ with $(c_2, c_4) \approx (g^2, -g^4)$ as the Δ=0 baseline. Re-fit per-Δ if subtraction residual shows Δ-dependence (§4 caveat).
2. **Convergence invariant at $\sigma^2_{\text{intrinsic}}$.** Stage 3 introduces the ensemble observable $\sigma^2_{\text{intrinsic}}(t)$. $n_{\text{eff}}$-converged does not imply $\sigma^2$-converged: the ensemble observable depends on derivatives of $p$ with respect to Δ, which concentrates numerical error at points of rapid change. Run Stage 3's own convergence check at Δ=0.15, $n_{\max}=12$ vs $18$ on $\sigma^2_{\text{intrinsic}}(t)$ before the Cut A ensemble launches (§10 items 1, 5).
3. **Symmetry-forced vanishing of $\partial_\Delta p$ at $\Delta=0$.** The VOYAGE_PLAN Stage 3 amendment already flags this (the leading small-noise contribution at Δ=0 is second-order in the noise width). Stage 3's QFI-reduction check on the on-resonance cut must compute $\partial_\Delta^2 p$, not $\partial_\Delta p$. At the sweep points $|\Delta| = 0.15, 0.3, 0.5$ the first-order expression is the right object.
4. **BLP cross-check planning.** The reduced spin state $\rho^{(\text{spin})}(t)$ is 2x2 and trivially traced; Stage 3's BLP computation (Standing Q 11) needs a second trajectory with a distinct initial spin state (e.g. $|\downarrow\rangle|0\rangle$ or a superposition) to form the antipodal pair. Budget for one extra propagation run at the Stage 3 sample point.

## 6. Go/no-go

All four gates pass. Stage 3 cleared to begin.
