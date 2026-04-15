# Collaborator handoff notes

**Endorsement Marker:** T(h)reehouse +EC voyage, Coastline layer. No external endorsement implied.

**Licence:** CC BY-SA 4.0 (see repository `LICENCE`).

Short notes on what is worth bringing from the voyage to specific external collaborators. Each note is a single page; each assumes the reader has the voyage writeup in front of them.

---

## For the MCTDH-numerics collaborator

**Context.** The voyage ran exact dense-eigh propagation of a bounded spin + 1–3 radial-mode Hamiltonian. This is tractable at $N \leq 3$ with $n_{\max} \leq 18$; at $N \geq 4$ or $n_{\max} \geq 30$ the dense approach stops scaling and a compressed-representation method (MCTDH or Krylov-based time propagation) becomes necessary.

**What Stage 6 and 7 suggest as worth an MCTDH-based follow-up:**

1. **Per-mode complementarity at $N \geq 4$.** The per-mode growth-framing $r(\sigma^2, |\dot{\mathcal{C}}^{(k)}|)$ is positive at the dominantly-coupled mode at $N = 1, 2, 3$ in the voyage's regime. Whether this extends to $N = 4, 5, 6$ is a legitimate question MCTDH can answer and the voyage cannot. If the per-mode signature survives, the complementarity finding gains $N$-scope; if it degrades past some $N^*$, the crossover is itself informative about where single-mode coupling structure dissolves.

2. **MCTDH self-calibration against the voyage at $N = 3$.** The Stage 7 metrics (at reduced statistics, $R = 30$, $n_{\max} = 10$) provide a cheap benchmark: running MCTDH on C-Ra / C-Rb / C-Rc at $D = +0.15$ and comparing $\mathcal{C}(t)$, $\sigma^2_{\text{intrinsic}}(t)$, and the per-mode $r_k$ values against [`stages/stage7_cut_c/metrics.json`](../stage7_cut_c/metrics.json) would validate the MCTDH implementation for this Hamiltonian class before extending it.

3. **Scope caveats to respect.** The voyage's findings are at $g/\omega_{\text{ref}} = 0.1$, $|\Delta|/\omega \geq 0.15$, vacuum initial state, closed system, Gaussian $\Delta$-noise only. MCTDH at different coupling strengths or with alternative initial states is a genuine extension, not a replication.

4. **Not useful from MCTDH for this voyage.** The voyage deliberately did not run MCTDH (see VOYAGE_PLAN §7). The value from the collaborator is $N \geq 4$ extension, not $N \leq 3$ cross-check — the exact-propagation in the voyage is already machine-precision at those mode counts.

**Concrete ask.** If interested, pick one of:

- Repeat C-Ra at $D = +0.15$ at $N = 4, 5$ with MCTDH, full statistics ($R = 100$), compare per-mode $r_k$ trend.
- Check whether the rational-commensurate null at Stage 7 (C-Rc does not cleanly separate from incommensurate configurations) persists at $N = 4, 5$ or whether a fourth mode breaks the degeneracy.

---

## For the open-systems / non-Markovianity collaborator

**Context.** The voyage's $T_{\text{det}}(M)$-family operational witness ($t_{\text{rise}}, T_{\text{det}}, f_{\text{resolved}}$) was designed as a candidate non-Markovianity-adjacent signature that explicitly includes the finite-shot measurement budget $M$. Scout's C2 / reconciliation Standing item 1 raised whether this reduces to a Fisher-information-thresholded-against-QPN criterion; Stage 3 confirmed the reduction at one parameter point; Stage 5 showed the reduction holds at outer detunings and breaks at inner. Stage 6 confirmed systematic breakdown across all $N = 2$ multi-mode configurations.

**What the voyage settles:**

1. **BLP trace distance is well-defined and recurrence-sensitive in the bounded-environment regime** (Stage 3 Gate 9 at $\Delta = 0.15$, $N = 1$, fixed antipodal pair: 2 sign changes in $\dot D$, $N_{\text{BLP}} = 0.97$). Scout's earlier "canonical measures under-applicable due to recurrence structure" (reconciliation §R2) is settled in Verifier's favour. BLP need not be avoided in this regime.

2. **The QFI-reduction regime boundary is a clean physics finding.** At outer single-mode detunings ($|\Delta| \geq 0.3$), the voyage's operational witness reduces to a first-order Fisher-information criterion scaled by measurement budget ($\sigma_\Delta^2 / M$-style); at inner or multi-mode, it carries independent information. This delineates a region where standard QFI-flow machinery suffices (and the voyage is redundant) from a region where the operational-crosswalk novelty lives.

3. **Complementarity is structural, not inequality-bounded.** The Stage 7 $\mathcal{C}(t) \cdot \sigma^2(t)$ test returned null — no universal lower bound. This is an honest scoping of the claim: the voyage has a descriptive complementarity structure, not a quantitative uncertainty relation.

**What is worth an open-systems follow-up:**

1. **$T_{\text{det}}(M)$-style witnesses are alternatives to BLP in the inner/multi-mode regime, not replacements.** A comparison study running both witnesses on the same bounded spin-boson dynamics would clarify whether $T_{\text{det}}$-family witnesses contain information that BLP-family witnesses do not, or whether they are linearisable into each other after parameter-space change of variable.

2. **Does the per-mode complementarity structure survive under explicit decoherence channels?** The voyage is closed-system by scope (§7). Adding Lindblad dissipation at the spin or mode level would test whether the complementarity is a closed-system artefact or a more general feature. Prediction: the growth-framing $r(\sigma^2, |\dot{\mathcal{C}}^{(k)}|)$ should weaken as dissipation rate grows, with a crossover where it vanishes — an interesting quantitative scaling.

3. **Memory-kernel non-Markovianity formalism cross-check.** Verifier P5 / E5 listed memory-kernel / time-local master equation approaches as a distinct non-Markovianity formalism. The voyage did not exercise this; a cross-check on a Stage 3 trajectory (computing the memory kernel numerically from exact propagation) would further settle whether the voyage's operational witness sits inside or outside the formalism-choice range (reconciliation Standing item 10).

**Concrete ask.** If interested, pick one of:

- Rerun Stage 3 at $\Delta = 0.15$ with a full BLP pair-optimisation (the voyage used a fixed antipodal pair; quantitative $\mathcal{N}_{\text{BLP}}$ requires optimisation over all state pairs).
- Add Lindblad dissipation to Stage 5's Cut A setup (one dissipation rate, $\gamma / \omega = 10^{-3}$) and track how the per-mode $r_k$ trend degrades.
- Cross-check the Stage 3 BLP trace distance against an RHP CP-divisibility computation on the same trajectory — Scout C5 reduction-path 3 may have a second-order analogue here.

---

## For the steward (voyage owner)

**Voyage verdict in one line.** H3-as-correlation falsified, complementarity confirmed per-mode, QFI-reduction boundary mapped, commensurability null — total compute $\sim 3$ hours, total elapsed $\sim 28$ hours.

**Decision the voyage informs.** Whether to commit MCTDH-collaborator time to the $N \geq 4$ extension depends on whether the per-mode complementarity finding is worth extending. My read: yes, it is — it's a structural finding that survived three $N$-values, and the extension is cheap for the collaborator (single MCTDH run at C-Ra $D=0.15$ at $N = 4, 5$).

**What the voyage does not licence.** Publication claims. The complementarity finding is descriptive-structural with a null on the quantitative uncertainty-relation form; the Stage 7 scope is reduced; Ordinans-adjacency is a null at the tested scope. A publishable paper would need wider scope, quantitative complementarity bounds, and ideally the MCTDH-extension result.

**What the voyage does licence.** Bringing the per-mode complementarity result to both named collaborators with the above concrete asks. Committing small amounts of follow-up time (voyage-sized) on the deferred items in [`novelty_statement.md`](novelty_statement.md) §Scope caveats.
