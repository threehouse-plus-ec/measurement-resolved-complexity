# When Does the Experiment Still See Something Happening?

**A short essay on measurement-resolved complexity in bounded quantum systems**

**Endorsement Marker:** T(h)reehouse +EC Sail. Local candidate framework under T(h)reehouse +EC stewardship. No external endorsement implied.

**Licence:** CC BY-SA 4.0 (see repository `LICENCE`).

**Companion repository:** [`measurement-resolved-complexity`](https://github.com/threehouse-plus-ec/measurement-resolved-complexity) — a bounded numerical exploration (8 stages, ~3 hours compute, April 2026) that produced the findings described here.

---

## The question

A trapped ion coupled to a few motional modes is a small quantum system whose dynamics can be tracked exactly — in a computer, at least. A theorist can compute the full wavefunction, diagonalise reduced density matrices, and quantify exactly how entangled the ion's spin is with its motional environment at every instant.

An experimentalist cannot. What the experimentalist sees is a binary outcome: spin up or spin down, repeated many times to build statistics. The variance of that outcome across experimental runs — how much the measured spin population fluctuates from shot to shot — is the raw signal. And that signal sits on top of an irreducible noise floor: quantum projection noise, the fundamental sampling uncertainty of a two-level measurement at finite shot budget.

The question this essay explores is simple: **when, and over how much of the observation window, does the experimentalist's variance signal stay above the projection-noise floor?** And does the pattern of that visibility bear any relationship to the theorist's entanglement complexity?

## Two clocks, one system

Define two time-resolved quantities on the same dynamics.

The **intrinsic complexity** $\mathcal{C}(t)$ is built from the von Neumann entropy of each motional mode's reduced density matrix. It counts, roughly, how many effective quantum states each mode participates in at time $t$. When the spin is maximally entangled with the modes — when the spin's reduced state is closest to a featureless coin flip — $\mathcal{C}$ peaks.

The **operational variance** $\sigma^2_{\text{intrinsic}}(t)$ is the shot-to-shot spread of the spin-up probability across an ensemble of experimental runs, each with slightly different trap parameters (a controlled stress-test level of frequency jitter). When the spin population is most sensitive to those parameter fluctuations — at moments of rapid state transition — $\sigma^2$ peaks.

These two quantities do not peak at the same time. They are, in a precise sense, complementary.

## The complementarity

At the moment of maximum entanglement, the spin's reduced state is near-maximally mixed: $p \approx 1/2$. But $p \approx 1/2$ is also the flattest part of the curve $p(\Delta)$ as a function of the detuning parameter. The derivative $\partial_\Delta p$ is small there. So the variance under parameter fluctuations — which, to first order in the small-noise regime, scales as $(\partial_\Delta p)^2$ times the noise variance — is *minimal* precisely when entanglement is maximal.

Conversely, when entanglement is low and the spin is near-pure ($p$ close to 0 or 1), the $p(\Delta)$ curve bends steeply, the derivative is large, and the experimental variance peaks.

The theorist's complexity and the experimentalist's sensitivity thus probe conjugate aspects of the dynamics. They are two clocks running on the same system, ticking at complementary moments.

## What the numerics show

A bounded numerical exploration — a single spin coupled to one, two, and three radial motional modes at intermediate coupling ($g/\omega = 0.1$), swept across a range of detunings — tested whether the complementarity is robust.

It is. At $N = 1$ and $N = 3$, where the per-mode decomposition was directly recorded, the correlation between rapid complexity growth and ensemble variance is consistently positive for the dominantly coupled mode: when that mode's complexity is changing fastest, the experimental variance is also large. At $N = 2$, the committed aggregate evidence is consistent with the same picture, but the per-mode decomposition was not recorded in the voyage metrics. Across all three mode counts, however, the *levels* of the two quantities are anti-correlated: high complexity coincides with low variance, and vice versa. The growth-framing catches the derivative co-variation; the anti-correlation catches the phase offset.

The original hypothesis — that a single scalar summarising complexity ($\bar{\mathcal{C}}$, the time-averaged entanglement entropy) and a single scalar summarising operational visibility ($f_{\text{resolved}}$, the fraction of time the variance exceeds projection noise) would track each other across a parameter sweep — was empirically falsified. The two scalars have independent drivers: $\bar{\mathcal{C}}$ tracks proximity to resonance and multi-mode participation; $f_{\text{resolved}}$ tracks how many oscillation cycles fit within the measurement window. They do not correlate.

The complementarity finding replaced the correlation hypothesis. It was not predicted in advance.

## A boundary in parameter space

A secondary finding maps where a standard theoretical shortcut works and where it doesn't.

In the small-noise limit, the ensemble variance reduces to a Fisher-information expression: $\sigma^2 \approx (\partial_\Delta p)^2 \sigma_\Delta^2$. This is a first-order linearisation — it says the variance is just the squared sensitivity times the noise level. When this reduction holds, the experimentalist's signal contains no information beyond what the standard metrological framework already captures.

At outer detunings (far from resonance) and with a single motional mode, the reduction holds to about 10%. At inner detunings (near resonance) or with two coupled modes (the tested multimode cases; three-mode QFI was not directly measured in the voyage), it breaks — deviations reach 20–30%. The boundary between these regimes is a clean physics finding: it marks where the system's dynamics is complex enough that the linearised Fisher-information picture stops being sufficient, and the full variance signal carries independent information about the underlying entanglement structure.

## What this does not say

The complementarity between theorist-visible complexity and experimentalist-visible variance is a structural observation at one coupling strength, one initial state, up to three motional modes, in a closed quantum system with no decoherence. It may or may not generalise to stronger coupling, larger mode counts, different initial states, or systems with dissipation. The numerical exploration that produced it was a scoping study — roughly three hours of computation on a standard machine — not a comprehensive survey.

The complementarity is descriptive, not inequality-bounded. A speculative test for a quantitative uncertainty-relation form ($\mathcal{C} \cdot \sigma^2 \geq \text{const}$) returned null: the product varies too much across configurations to support a universal lower bound.

The commensurability of mode frequencies — whether they stand in golden-ratio, irrational, or rational relationships — did not produce any distinguishable signature at the tested scope. If such signatures exist, they live at larger mode counts or different parameter regions than those explored here.

## Why it might matter

In a trapped-ion experiment, the question "is there still something happening that I can see?" is not academic. It determines how long to run an interrogation sequence, how many shots to budget, and whether the dynamics visible in the data reflects genuine quantum correlations or has already been washed out by projection noise.

The complementarity finding suggests that the answer depends on *which aspect* of the dynamics you're looking at. Entanglement complexity and measurement sensitivity peak at different moments. An experimentalist tuning the measurement window to catch maximum variance is not catching maximum entanglement — and vice versa. This is not a limitation of the measurement; it is a feature of the physics.

For numerical methods like MCTDH that can handle larger mode counts than exact diagonalisation, the per-mode decomposition of the complexity signal ($r_k$ per mode, rather than the aggregate $\mathcal{C}$) is a natural diagnostic. MCTDH-style methods can access analogous per-mode occupation and reduced-state information, making them a natural way to test whether the per-mode complementarity survives at $N = 4, 5, 6$ — where exact propagation becomes impractical — as a bounded, testable question that requires no framework adoption.

For open-quantum-systems theory, the QFI-reduction boundary is a parameter-space map that connects to established non-Markovianity witnesses. Where the first-order Fisher linearisation holds, the operational variance witness is equivalent to a QFI-flow non-Markovianity witness dressed in trapped-ion language. Where it breaks, the operational witness carries independent information — and understanding *why* it breaks (higher-order parameter sensitivity, multi-mode interference, or both) is a question the existing formalism can address.

## The short version

Two measures of what's happening in a small quantum system — one accessible to a theorist with the full wavefunction, one accessible to an experimentalist with finite shots — turn out to probe complementary moments of the dynamics. They do not track each other as single numbers across a parameter sweep. But their per-mode derivative structure is correlated, and the boundary where the standard linearised connection between them breaks is itself a physics result.

The question "when does the experiment still see something happening?" has a richer answer than "until decoherence kills it." In a closed bounded system, the answer is: the experiment sees something happening at *different moments* than the theorist sees maximum complexity — and the interplay between those moments is where the interesting structure lives.

---

## Anchor references

Seven starting points for readers who want to follow the threads this essay touches. These are entry-level anchors, not a literature review; the companion repository's [`literature_search/`](https://github.com/threehouse-plus-ec/measurement-resolved-complexity/tree/main/literature_search) folder contains the full prior-art audit.

1. **D. Braak, "Integrability of the Rabi Model," *Phys. Rev. Lett.* 107, 100401 (2011).** Exact analytical solution of the quantum Rabi model (single spin + single bosonic mode, no RWA). Establishes that the Hamiltonian class used in this essay is integrable at $N = 1$ and provides the spectral framework against which counter-rotating-term effects are understood.

2. **H.-P. Breuer, E.-M. Laine, and J. Piilo, "Measure for the Degree of Non-Markovian Behavior of Quantum Processes in Open Systems," *Phys. Rev. Lett.* 103, 210401 (2009).** The BLP trace-distance non-Markovianity measure. The voyage tested this in its bounded-environment regime and found it well-defined and recurrence-sensitive — settling an internal divergence about whether canonical measures apply to bounded mode sets.

3. **V. Alba and P. Calabrese, "Entanglement and Thermodynamics after a Quantum Quench in Integrable Systems," *Phys. Rev. Lett.* 119, 010601 (2017); and "Entanglement Dynamics after Quantum Quenches in Integrable Systems," *SciPost Phys.* 4, 017 (2018).** Canonical treatment of reduced-state von Neumann entropy as a time-resolved dynamical observable after quantum quenches. Establishes the quasiparticle picture for entropy growth that the essay's "intrinsic complexity" measure is a bounded-system relative of.

4. **A. F. Kockum, A. Miranowicz, S. De Liberato, S. Savasta, and F. Nori, "Ultrastrong coupling between light and matter," *Nat. Rev. Phys.* 1, 19–40 (2019).** Review of the ultrastrong-coupling regime in circuit-QED and cavity-QED platforms. Covers the breakdown of the rotating-wave approximation and the role of counter-rotating terms — the regime the voyage operates at the boundary of ($g/\omega = 0.1$).

5. **A. Stokes and A. Nazir, "Gauge ambiguities imply Jaynes-Cummings physics remains valid in ultrastrong coupling QED," *Nat. Commun.* 10, 499 (2019).** Demonstrates that the presence of counter-rotating terms depends on the choice of gauge (Coulomb vs. dipole). The voyage fixes dipole gauge throughout; this reference is the reason why "no RWA" requires a gauge statement to be unambiguous.

6. **X.-M. Lu, X. Wang, and C. P. Sun, "Quantum Fisher information flow and non-Markovian processes of open systems," *Phys. Rev. A* 82, 042103 (2010).** Fisher-information flow as a non-Markovianity witness. The voyage's QFI-reduction check — testing whether the ensemble variance reduces to a Fisher-information expression — is a direct descendant of this framework, and the essay's "boundary in parameter space" maps where the first-order reduction to this framework holds and where it breaks.

7. **D. Leibfried, R. Blatt, C. Monroe, and D. Wineland, "Quantum dynamics of single trapped ions," *Rev. Mod. Phys.* 75, 281–324 (2003).** Comprehensive review of trapped-ion quantum dynamics, including spin-motion coupling, Rabi and Jaynes–Cummings models, and quantum-projection-noise-limited measurement — the experimental substrate the essay's Hamiltonian and noise model are drawn from.

---

*This Sail is part of the T(h)reehouse +EC open-science harbour. It describes findings from a bounded numerical exploration; the companion repository contains the full code, data, and audit trail. The essay is designed to be readable without the repository and without adoption of any framework.*