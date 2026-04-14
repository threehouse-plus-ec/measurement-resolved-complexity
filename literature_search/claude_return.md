# Claude Scout Return — Background Literature Search

**Endorsement Marker:** T(h)reehouse +EC voyage, Coastline layer. No external endorsement implied.

**Licence:** CC BY-SA 4.0 (see repository `LICENCE`).

**Role:** Scout — conceptual mapping, cross-field synthesis, gap identification.
**Stance:** Maps the landscape; does not adjudicate novelty.
**Task card:** `TASK_CARD.md` v2 (this folder).
**Companion return:** `perplexity_return.md` (pending).
**Reconciliation note:** `reconciliation.md` (pending, Harbourmaster).

**Scope notice:** this is a single Scout pass. Citations are not fabricated but are referenced in short form; Perplexity's return is authoritative on bibliography. Where this document names a concept ("OTOC", "BLP", "reaction coordinate mapping"), the canonical primary reference should be supplied in reconciliation from Perplexity's P-returns.

---

## C1 — Conceptual family tree of the voyage's central construct

The voyage's construct is a *measurement-resolved complexity diagnostic*: track $n_{\text{eff}}^{(k)}(t)$ alongside ensemble variance $\sigma^2_{\text{intrinsic}}(t)$ under controlled parameter noise, and declare a detectability horizon $T_{\text{det}}(M)$ where $\sigma^2_{\text{intrinsic}}$ exceeds the projection-noise floor $\sigma^2_{\text{QPN}}(t; M)$. Each layer has a distinct conceptual home.

### Quantum chaos
**Imports:** the intuition that "complexity" is a quantifier of state-space exploration, and that complexity has early-time universal behaviour plus late-time system-specific saturation.

**Adjacent tools:**
- OTOCs / scrambling diagnostics — operator-level complexity; the voyage's construct is state-level, but the saturation phenomenology rhymes.
- Spectral form factor — long-time signature; requires spectral-level access, not directly portable to the voyage.
- Krylov (spread) complexity — closest direct analogue: growth of support of $|\psi(t)\rangle$ in the Krylov basis. $n_{\text{eff}}^{(k)}$ has family resemblance to an effective Schmidt rank, which in turn family-resembles spread complexity.
- Loschmidt echo / fidelity decay — sensitivity under perturbations; conceptually sibling to $\sigma^2_{\text{intrinsic}}$ under detuning noise.

**Scout flag:** the voyage does *not* import OTOCs or spectral form factor directly; it imports the genre of "dynamical complexity as monotone-then-saturating quantity". The mapping to Krylov complexity is worth a reconciliation check — if the single-mode reduced entropy and Krylov dimension give correlated signals in this Hamiltonian, the voyage's intrinsic measure has a second independent identity and the novelty claim contracts.

### Open quantum systems
**Imports:** the information-backflow logic — $\sigma^2_{\text{intrinsic}} > \sigma^2_{\text{QPN}}$ at late times is operationally equivalent to "information is coming back from the environment into the observable".

**Adjacent tools:**
- BLP trace-distance non-Markovianity — direct ancestor of the $T_{\text{det}}$ logic; differs in that BLP optimises over state pairs, while $T_{\text{det}}$ fixes the observable and ensemble-averages over parameter noise.
- RHP CP-divisibility — structural rather than operational; under-applicable for a bounded bosonic environment with recurrence structure (see C2).
- Reaction coordinate / polaron mappings — highly relevant: they are the standard technology for reducing a bounded bosonic environment to "primary mode + residual bath" and have been used to study non-Markovian signatures in similar Hamiltonians.
- Collision models — not directly applicable (the voyage has continuous unitary dynamics, no collision structure).

**Scout flag:** the voyage's bounded-environment-with-recurrence setting is precisely the regime where canonical non-Markovianity measures are hardest to interpret — recurrences generate "backflow" that is a kinematic artefact of the bounded spectrum, not a dynamical memory effect in the usual sense. This is a feature of the voyage, not a bug: it forces an operational rather than structural reading of memory.

### Quantum metrology
**Imports:** the projection-noise floor logic — $\sigma^2_{\text{QPN}} = p(1-p)/M$ as the irreducible shot-noise-limited uncertainty for a projective spin measurement at shot budget $M$.

**Adjacent tools:**
- Quantum Fisher information (QFI) / Cramér-Rao bound — the voyage's $\sigma^2_{\text{intrinsic}}$ is closely related to (classical) Fisher information about $\Delta$ evaluated on the spin observable, scaled by $M^{-1}$.
- Shot-noise-limited vs Heisenberg-limited scaling — not the voyage's concern, but lives in the same notational space.
- Parameter-estimation trade-offs under realistic noise — the broader framing in which $T_{\text{det}}(M)$ is legible.

**Scout flag:** the voyage is not doing metrology in the usual sense (it is not estimating $\Delta$). It is using metrology-style bookkeeping to declare when dynamics is resolvable. This is a *borrowing* of the framework, not a claim within it. Reconciliation with P3 will establish whether this borrowing has precedent.

### Many-body dynamics / quantum information
**Imports:** single-mode reduced von Neumann entropy as a standard dynamical observable. This is textbook machinery; the voyage does not invent it.

**Adjacent tools:**
- Entanglement entropy after quantum quench (linear growth → volume-law saturation) — standard Calabrese-Cardy phenomenology; the voyage's early-time ~$t^2$ regime is the *short-time* analogue.
- Page curve / subsystem entanglement in bounded systems — directly relevant; predicts the saturation value of $n_{\text{eff}}^{(k)}$ under random-state assumptions.
- ETH — predicts thermalisation of local observables; less directly relevant to the entropy object.
- Entanglement tsunami / Lieb-Robinson bounds — mostly lattice-native; here we have a 1-spin + few-boson system, so Lieb-Robinson speed is not the operative bound.

**Scout flag:** the entropy-of-reduced-state is the voyage's *least novel* component. Its use as a dynamical observable in spin-boson contexts will likely have direct precedent (P2). The question is whether it has been used at $g/\omega = 0.1$, $\Delta/\omega \in [-0.5, 0.5]$, no-RWA, 1–3 radial modes — the specific parameter region of this voyage — rather than at ultrastrong ($g/\omega \gtrsim 1$) or weak ($g/\omega \ll 0.1$) coupling where most of the literature sits.

### Trapped-ion simulation
**Imports:** the Hamiltonian structure directly ($\sigma_x$ × displacement coupling on one or a few radial modes), the experimental context for realistic $\Delta$-noise statistics (P4), and the semantics of $p(t)$ as a directly measured observable.

**Adjacent tools:**
- Sideband-resolved spectroscopy — the JC/anti-JC limit against which Stage 1 will be validated.
- Porras-Cirac-Solano spin-boson proposals — the voyage's Hamiltonian is a near-neighbour of these; they have been extensively analytically studied.
- Variance-based parameter estimation in ion traps — reference implementations of "measure $p$, compute variance, extract $\Delta$" protocols.

**Scout flag:** if Perplexity surfaces a trapped-ion study that already runs exact propagation of this Hamiltonian at these parameters and tracks reduced-state entropy *and* ensemble variance, the voyage's novelty contracts to the specific $T_{\text{det}}(M)$ construction and the cross-walk framing. If no such study exists, the operational recombination claim stands.

### Apparent conceptual gap (flagged apparent, pending Perplexity)

Each of the three layers — reduced-state entropy as complexity proxy, ensemble variance as sensitivity proxy, QPN as detectability floor — is individually standard. The *three-way conjunction* as an analysis methodology, applied to a bounded spin + few-mode bosonic system with $T_{\text{det}}(M)$ as the operational anchor, may be without direct precedent. This is the candidate novelty region the voyage should own or disown based on Perplexity's P2/P3 returns.

---

## C2 — Relationship between $T_{\text{det}}(M)$ and existing information-backflow measures

**Setup.** BLP non-Markovianity measure:
$$\mathcal{N}_{\text{BLP}} = \max_{\rho_1, \rho_2} \int_{\dot D > 0} \frac{dD(\rho_1, \rho_2)}{dt}\, dt, \quad D = \tfrac{1}{2}\|\rho_1 - \rho_2\|_1.$$
$T_{\text{det}}(M)$ construction: $T_{\text{det}}(M) = \sup\{\,t : \sigma^2_{\text{intrinsic}}(t) > \sigma^2_{\text{QPN}}(t; M)\,\}$ (or, equivalently, the last $t$ at which the inequality holds within a finite time window).

### Structural differences
1. **Domain of optimisation.** BLP optimises over state pairs of the reduced system. $T_{\text{det}}$ fixes the observable ($p = \langle \sigma_z \rangle$ or similar) and the noise channel (ensemble distribution over $\Delta$); there is no state-pair optimisation.
2. **Object of comparison.** BLP compares two reduced-state trajectories. $T_{\text{det}}$ compares two *scalar time series* on the same trajectory ensemble.
3. **Budget dependence.** BLP has no measurement-budget parameter; it is a property of the dynamical map. $T_{\text{det}}(M)$ is explicitly parametrised by $M$. Doubling $M$ halves the QPN floor and typically extends $T_{\text{det}}$.
4. **Bounded-environment behaviour.** BLP in bounded bosonic environments is dominated by recurrences; $\mathcal{N}_{\text{BLP}}$ can be unbounded as the integration window grows. $T_{\text{det}}(M)$ has a finite, monotone-in-$M$ interpretation even in recurrent regimes — it reports *when* signal is above noise, not *how much* information backflows in total.

### Reduction conditions (partial analysis)
**Scout flag — speculative.** Consider fixing the observable to $\sigma_z$ and letting parameter noise be Gaussian with variance $s^2$ about the nominal $\Delta$. For small $s$:
$$\sigma^2_{\text{intrinsic}}(t) \approx \left(\frac{\partial \langle \sigma_z \rangle(t)}{\partial \Delta}\right)^2 s^2 + O(s^4).$$
The partial derivative is the Fisher-information-carrying quantity. Therefore $T_{\text{det}}(M)$ in the small-noise limit is equivalent to:
$$\left(\frac{\partial \langle \sigma_z \rangle}{\partial \Delta}\right)^2 s^2 > \frac{p(1-p)}{M}.$$
This is a *classical-Fisher-information × measurement-budget* criterion. It is *not* a BLP-reduction; it is a reduction to a metrological witness.

**Partial answer to the task (a/b/c).** The answer is closer to **(b)** than (a): $T_{\text{det}}(M)$ is a distinct, measurement-budget-dependent witness, not a direct reduction of BLP. However, the reduction noted above — to a Fisher-information-thresholded-against-QPN criterion — should be checked against Perplexity P5's canonical-measures list, particularly if any Fisher-based non-Markovianity witness is surfaced there. If so, the voyage's construct is a trapped-ion-specific, ensemble-noise-parametrised implementation of that line of work. If not, the construct is a novel operational recombination.

**Residual ambiguity (flagged).** Whether the identification of $\sigma^2_{\text{intrinsic}}$ with Fisher-information-times-noise-variance holds robustly across the voyage's parameter region (non-small $s$, recurrent regime) requires a numerical check at Stage 3. Do not inscribe the reduction in the Stage 8 writeup without that check.

---

## C3 — Pitfalls in interpreting $n_{\text{eff}}^{(k)}(t)$ dynamically

A short, ordered list. Each pitfall has been observed in at least one adjacent literature; specific primary references are Perplexity's responsibility.

1. **Fock-truncation entropy ceiling.**
$n_{\text{eff}}^{(k)} \leq n_{\max}^{(k)}$ exactly, so the numerical ceiling is hard. If the dynamical curve approaches $\log(n_{\max})$ by a factor of order unity, you are reporting the truncation, not the physics. **Mitigation:** run with $n_{\max}$ and $2 n_{\max}$; physical saturation is truncation-independent. This is the voyage's H1 convergence requirement and Stage 1's explicit checkpoint.

2. **Mode-labelling ambiguity when modes are near-degenerate.**
$\rho^{(k)}(t)$ is basis-independent for fixed $k$, but the labelling "mode 1 vs mode 2" is an analyst choice. Near commensurability ($\omega_1 \approx \omega_2$), a symplectic reshuffling of the bosonic subspace changes which mode is "1" without altering the total state. Per-mode $n_{\text{eff}}^{(k)}$ curves can therefore be rotated between modes; the aggregate $\mathcal{C}(t) = \sum_k \log n_{\text{eff}}^{(k)}(t)$ is the more invariant quantity. **Mitigation:** report aggregate complexity as primary; per-mode only as decomposition.

3. **Early-time universal $t^2$ growth.**
For product initial states, $S_{\text{vN}}(\rho^{(k)}(t)) \sim c_k t^2$ at short times is generic — it is a consequence of the initial commutator structure, not of any specific dynamics. The *informative* signal is deviation from $t^2$: linear growth indicates ballistic entanglement build-up, sub-quadratic indicates constrained dynamics, super-quadratic indicates cascading. **Mitigation:** plot $n_{\text{eff}}(t) - n_{\text{eff}}^{\text{short-time}}(t)$ or fit and subtract the $t^2$ coefficient before reading saturation structure.

4. **Entropy is not complexity (semantic pitfall).**
High single-mode entropy can arise from unstructured thermal-like mixing as well as from structured multi-mode coherence. $n_{\text{eff}}^{(k)} = \exp(S_{\text{vN}})$ does not distinguish the two. The voyage's "effective orbital count" reading presumes that the single-mode reduced state is approximately a mixture over a small number of pure modes, which is a stronger claim than entropy alone licenses. **Mitigation:** in Stage 2, inspect the eigenvalue spectrum of $\rho^{(k)}$ directly, not only its entropy. If the spectrum is peaked on few eigenvalues, the "effective count" reading is licensed; if it is broadly spread, the reading is rhetorical.

5. **MCTDH-adjacent lessons that apply without running MCTDH.**
- Natural-orbital populations are often near-degenerate, making $n_{\text{eff}}$ numerically jittery even when dynamics is smooth.
- "False saturation" plateaus at intermediate times can break at longer times — trust saturation only if it persists across a factor-2 extension of the window.
- Single-particle-function convergence in MCTDH is not equivalent to observable convergence. The voyage does not run MCTDH, but the analogous point is: $n_{\text{eff}}$ convergence is not equivalent to $p(t)$ convergence. Both must be checked.

6. **Normalisation drift.**
Non-unitary integrators (Krylov-based, adaptive-step RK) accumulate norm drift at long times. A 1% norm loss contaminates entropy at the 0.01-ish level, which matters for saturation reading. **Mitigation:** log $\|\psi(t)\|^2$ at every inspection point; reject runs where drift exceeds a stated tolerance (voyage plan already specifies this).

7. **Initial-state dependence of the complexity curve.**
$n_{\text{eff}}^{(k)}(t)$ for (coherent × spin-up) initial state differs structurally from (thermal × spin-superposition). The detuning-sweep curves are not "the complexity of the Hamiltonian" — they are "the complexity of this Hamiltonian acting on this initial state". Not a pitfall if held fixed, but it must be held fixed and documented. **Voyage-specific risk:** if Stage 1's JC validation uses a different initial state than Stage 2's complexity measurement, comparisons across stages are invalid.

---

## C4 — The Ordinans-framework adjacency question

**Scout flag — this section depends on my reading of Ordinans; Harbourmaster should verify against the canonical Ordinans statement.**

### What Ordinans, as I understand it, asserts
Complexity in a quantum dynamical system can be read off from *regime cycling*: the system traverses through phases where the dominant correlation length scales differently (short-range / intermediate / long-range / back to short-range), and the traversal itself is the complexity signature. The framework is meant to be substrate-independent: applicable to lattice spin systems, continuous quantum fields, and — in principle — bounded spin-boson models.

### What the voyage tests about Ordinans
- Whether a bounded spin + few-mode bosonic system at intermediate coupling exhibits *any* observable regime structure under the chosen complexity proxies.
- Whether the voyage's $n_{\text{eff}}^{(k)}(t)$ is a serviceable proxy for "regime structure" in the Ordinans sense, or whether it is orthogonal.
- Whether such regime structure — if present — is resolvable within realistic $M$ (i.e. whether Ordinans-style claims have experimental purchase in this platform).

### What the voyage does not test
- Whether correlation-length traversal has the specific topology Ordinans predicts. The voyage works at a single Hamiltonian class and does not map correlation-length cycling in configuration space.
- Whether Ordinans applies to thermodynamic-limit systems. The voyage is explicitly bounded (1 spin + 1–3 bosonic modes, hard Fock cutoff).
- Whether the regime structure — if present — is universal across Hamiltonians, or specific to this parameter region.

### Where the framework needs the voyage vs. where it is independent
**Framework needs the voyage:** Ordinans, as an operational claim, requires that "complexity measures track each other under realistic finite-$M$ observation". The voyage tests this prerequisite in one specific system. If complexity measures do *not* track each other here, Ordinans faces a local counterexample at a platform it would want to operationalise on.

**Voyage is independent of the framework:** the empirical question — do $n_{\text{eff}}$ saturation and $T_{\text{det}}(M)$ track each other across a detuning sweep — is well-posed without Ordinans. If Ordinans is wrong or unneeded, the voyage's measurements still answer a sharp methodological question about measurement-resolved complexity in trapped-ion-accessible regimes.

### Honest scoping statement
**The voyage stands alone and Ordinans is separately worth testing.** Framing the voyage as an Ordinans validation would overclaim in two directions: (i) it would treat a single parameter region as a framework-wide test, and (ii) it would tether the methodological question ("can measurement-resolved complexity be read within $M$?") to a framework-adoption question. The voyage should be presented as a *methodological study* whose results are legible to Ordinans-believers and Ordinans-sceptics alike.

---

## C5 — Draft novelty statement (pre-reconciliation)

**Scout flag — this draft is pre-reconciliation. Harbourmaster revises against Perplexity's P1–P5 return. If direct precedent is surfaced, the claim contracts further. This draft is calibrated to the operational-recombination register per the task card.**

---

> **Draft novelty paragraph (Stage 8 candidate, pre-reconciliation).**
>
> We combine three established constructs — (i) the von Neumann entropy of the single-mode reduced density matrix as a dynamical complexity proxy (standard in many-body dynamics and MCTDH-adjacent literatures); (ii) ensemble variance of a projective spin observable under controlled parameter noise (standard in trapped-ion sensitivity analysis and parameter estimation); and (iii) quantum projection noise as a finite-shot detectability floor (standard in quantum metrology) — into a single measurement-resolved complexity diagnostic for a bounded spin + few-mode bosonic system at intermediate coupling ($g/\omega = 0.1$, no RWA). The operational recombination, not any single component, is what is plausibly novel: we introduce $T_{\text{det}}(M)$ as a measurement-budget-dependent horizon explicitly anchored to the saturation of $n_{\text{eff}}^{(k)}$ across a detuning sweep, in a regime where canonical non-Markovianity measures are under-applicable due to the bounded environment's recurrence structure. We claim neither a new observable nor new physics; we claim a specific operational crosswalk that connects what a theorist sees (intrinsic-complexity saturation) to what an experimentalist can resolve (variance above projection noise) in a parameter region of direct relevance to trapped-ion quantum simulation.

---

**Contraction conditions (what shrinks this claim):**

- If Perplexity P2 surfaces a direct spin-boson or multimode-Rabi study that tracks single-mode reduced entropy dynamically at $g/\omega \approx 0.1$, no RWA: the "dynamical complexity proxy" component is fully precedented — expected — and the novelty rests on (ii)+(iii)+operational-crosswalk.
- If Perplexity P3 surfaces a study that uses ensemble-variance-above-projection-noise as an operational threshold for resolving late-time dynamical structure: the core $T_{\text{det}}(M)$ construction is precedented, and the voyage's claim contracts to "a trapped-ion-parameterised implementation of [cited] construction at intermediate coupling with no RWA".
- If Perplexity P5 surfaces a Fisher-information-based non-Markovianity measure under which $T_{\text{det}}(M)$ is a direct shot-noise thresholding: the claim contracts to "an operational ion-trap-legible restatement of [cited] measure".
- If *all three* contract, the voyage is a well-scoped methodological replication in a specific platform — not zero value, but not a novelty claim. This would reframe Stage 8 as a calibration study.

**Expansion conditions (what strengthens this claim):**

- If P2 finds precedent only outside the $g/\omega \sim 0.1$ / no-RWA region, the "at intermediate coupling, no RWA" hedge becomes a legitimate scoping claim.
- If P3 finds only near-neighbours (shot-noise-limited non-Markovianity without the explicit $T_{\text{det}}(M)$-horizon construction), the operational-recombination claim is preserved.
- If P5 finds canonical measures that are all under-applicable to bounded environments with recurrence, the voyage's "under-applicability of canonical measures" clause is justified and its own witness is substantively useful.

---

## Summary and handoff

- **Family tree (C1):** the voyage imports from quantum chaos (complexity-as-saturation intuition), open quantum systems (backflow semantics), quantum metrology (QPN floor), many-body dynamics (reduced-state entropy), and trapped-ion simulation (Hamiltonian + noise statistics). No single parent field owns the construct; the apparent gap is the three-way cross-walk.
- **$T_{\text{det}}$ vs BLP (C2):** distinct, measurement-budget-dependent witness. Candidate reduction to a Fisher-information-thresholded-against-QPN criterion in the small-noise limit — needs Stage 3 numerical check and P5 reconciliation.
- **Pitfalls (C3):** seven items, ordered by severity. The most serious for Stage 8 reading are (1) Fock-truncation ceiling, (3) $t^2$ early-time masking, and (4) entropy-is-not-complexity semantic overclaim.
- **Ordinans (C4):** voyage stands alone; framework benefits if the voyage succeeds, but voyage does not depend on framework. Do not frame the voyage as an Ordinans validation.
- **Novelty draft (C5):** operational-recombination register. Contraction conditions and expansion conditions enumerated; Harbourmaster reconciles against Perplexity.

**Outstanding dependencies on Perplexity:** P2 (direct precedent for reduced-state entropy as time-resolved diagnostic in this coupling region), P3 (direct precedent for $T_{\text{det}}$-style operational thresholding), P5 (canonical non-Markovianity measures that may absorb $T_{\text{det}}$ as a special case).

---

*End of Scout return. Reconciliation note awaited.*
