# Plan Amendments Register

**Endorsement Marker:** T(h)reehouse +EC voyage, Coastline layer. No external endorsement implied.

**Licence:** CC BY-SA 4.0 (see repository `LICENCE`).

Tracks structural amendments to `VOYAGE_PLAN.md` made after Stage 0 lock. The Harbour convention through v0.1 was *superseding note + dated strikethrough* rather than silent edit, so anyone reading the plan cold encountered the correction in place. At v0.2 all such amendments are absorbed as coherent design with in-text citations back to the originating stage; v0.1 is preserved in `archive/` per CD §0.8.

## Convention

Each amendment is one row: date, section amended, short description, driving document, style. The Guardian tripwire inscribed at the Stage 1 commit (2026-04-14): *if three or more structural amendments accrue before a stage launches, the next move is a clean v0.2 of `VOYAGE_PLAN.md`* — stacking strikethroughs past that point turns the plan into a palimpsest. The tripwire fired at amendment 4 and triggered v0.2 on 2026-04-14.

## Register

| # | Date | Section(s) | Amendment | Driver | Style (v0.1) | Absorbed in v0.2 at |
|---|---|---|---|---|---|---|
| PA-00 | 2026-04-14 | §Stage 1 go/no-go, §Stage 3 scope, §2.1 (gauge), §2.4 (1% RMS rationale), §10 | Pre-Stage-1 plan patches from Harbourmaster reconciliation: gauge convention documented, 1% RMS reframed as stress-test, Stage 1 gate 3 added, Stage 3 scope extended with QFI + BLP cross-checks, §10 Standing Questions populated with reconciliation-derived pitfalls. | `literature_search/reconciliation.md` | Inline, no strikethrough | §2.1 gauge paragraph; §2.4 noise row; §3 Stage-3-scope items now canonical; §6 Stages 1/3 gate structures; §10 full 12-item register |
| PA-01 | 2026-04-14 | §Stage 1 (JC-phrasing) | Stage-1-prep analytic check: the "$2g$ Rabi" phrasing in §Stage 1 was JC-folklore inapplicable to the unbiased Rabi model. Correct target is $p(t) = \tfrac12(1 + e^{-2g^2t^2})$. | Stage 1 preparation; Guardian adjudication | Strikethrough + superseding note | §6 Stage 1 anchor descriptions use the correct analytic form from the outset; §Stage 1 gates correspondingly. |
| PA-02 | 2026-04-14 | §2.4 (detuning range), §2.5 (Fock justification), §5 (H3 reading), §10 (Standing Q #12) | Stage-1-prep convergence scan: $\Delta=0$ drives unbounded coherent-amplitude growth with $\|\uparrow\rangle\|0\rangle$; the correct bound is $\langle n\rangle_{\max} = 4(g/\|\Delta\|)^2$ (factor of 4 from drive-vs-free-oscillation interference); innermost accessible point under homogeneous $n_{\max} = 12$ is $\|\Delta\|/\omega_{\text{ref}} = 0.15$. Cut A reset to the six-point set $\{-0.5,-0.3,-0.15,+0.15,+0.3,+0.5\}$. H3 becomes a limit claim. | Stage 1 prep numerical check; Guardian option III-b | Strikethrough + superseding note | §2.4 detuning row; §2.5 full rewrite with measured convergence table; §5 H3 reformulated; §10 Q 12. |
| PA-03 | 2026-04-14 | §3 (observables), §5 (H3 scalar), §6 (Stage 8 scatter) | Stage 3 finding: $T_{\text{det}}$ "last exceedance" is dissipative-environment intuition and window-saturates in bounded recurrent regimes. The triple $(t_{\text{rise}}, T_{\text{det}}, f_{\text{resolved}})$ is the right characterisation; $f_{\text{resolved}}(M)$ is the headline scalar for the H3 scatter. | Stage 3 Gate 9 resolution and timing analysis; Guardian endorsement in Stage 3 review | Flagged in Stage 3 / 4 notes for v0.2 | §3.2 items 7 and 8; §5 H3; §6 Stage 8 artifact redefined. |
| PA-04 | 2026-04-14 | §5 (H2), §6 (Stage 4 verdict structure; Stage 6 Gate 13) | Stage 4 finding: $\mathcal{C}(t)$ saturates to the Schmidt-rank-2 bound $\log 2$ at $N=1$ (99.93% of bound). H2-as-"peak alignment of $\mathcal{C}$ and $\sigma^2$" is under-tested at $N=1$ by structural saturation; the growth-framing ($|\dot{\mathcal{C}}|$ vs $\sigma^2$) is the informative test at $N=1$; full H2 lives at $N \geq 2$. | Stage 4 inspection; Guardian v0.2 go-ahead | Flagged in Stage 4 notes for v0.2 | §5 H2 with N=1 caveat; §6 Stage 4 verdict structure; §6 Stage 6 Gate 13 full H2 test. |

## v0.2 closure

On 2026-04-14 the four amendments PA-01..PA-04 (plus the pre-amendment reconciliation patches PA-00) were absorbed into v0.2 of `VOYAGE_PLAN.md`. v0.1 is preserved verbatim at `archive/VOYAGE_PLAN-v0.1.md` with a deprecation note at `archive/2026-04-14-VOYAGE_PLAN-v0.1-deprecated.md`. v0.2 carries source citations in-text (PA-01..PA-04, C3.n, P#, HM) so the amendment lineage is auditable from either the plan or this register. The tripwire has reset: further amendments to v0.2 during Stage 5 onward resume the strikethrough-+-dated-supersede convention until a further three accumulate.

## Post-v0.2 amendments

| # | Date | Section(s) | Amendment | Driver | Style |
|---|---|---|---|---|---|
| PA-05 | 2026-04-15 | §3 (observables), §5 (H2/H3), §6 (Stage 8) | **H2 reformulated per-mode; H3 retired-as-correlation and replaced by complementarity.** Four-stage convergent evidence (Stages 4–7) across $N = 1, 2, 3$: aggregate H2 breaks at $N = 3$ while per-mode H2 holds for the dominantly-coupled mode at all $N$; $f_{\text{resolved}}$–$\bar{\mathcal{C}}$ correlation is non-monotone across the sweep (Stages 5, 6, 7), with $f_{\text{resolved}}$ tracking beat-frequency / oscillation-cycle count and $\bar{\mathcal{C}}$ tracking resonance proximity — independent drivers, no single-scalar rescaling. The replacement hypothesis: $\mathcal{C}$ and $\sigma^2_{\text{intrinsic}}$ probe **complementary** moments of the dynamics ($\mathcal{C}$ at maximum entanglement, $\sigma^2$ at maximum purity / $(\partial_\Delta p)^2$-large state-transition moments). Speculative quantitative uncertainty-relation test $\mathcal{C}\cdot\sigma^2$ returned null at Stage 7; the finding stays structural-descriptive. Scope: $g/\omega = 0.1$, $|\Delta|/\omega \in [0.15, 0.5]$, $|\uparrow\rangle|0\rangle$ initial state, $N \leq 3$, closed system. Not a universal physics claim. | Stages 4–7 convergent evidence; Stage 6/7 notes; Guardian Stage 7 sign-off | Strikethrough + superseding note in-place |
| PA-06 | 2026-04-15 | Sail (`when-does-the-experiment-still-see.md`) | Sail addendum naming platform-independence solo follow-up; no scope change to v1.0 voyage findings. | Stage 8 post-synthesis; author-initiated documentation | Additive insertion (new section) |

## Tripwire status (post-v0.2)

- Amendments committed since v0.2 reset: **2** (PA-05, PA-06).
- Buffer before next v0.3 consideration: **1** further amendment.
- Pending candidates: none at PA-06 commit. PA-06 is documentation-only (Sail addendum), not a plan change.

## What v0.2 does not claim resolved

- Krylov / spread-complexity identity check — deferred to TASK_CARD v3; Stage 8 cannot claim novelty on the intrinsic-complexity component until addressed.
- Sweep-wide QFI reduction confirmation — Stage 3 confirmed at $\Delta = 0.15$; Stage 5 reports across Cut A.
- Full BLP pair optimisation — Stage 3 used a fixed antipodal pair; quantitative $\mathcal{N}_{\text{BLP}}$ requires optimisation.
- Noise-spectrum (coherent-modulation) sensitivity — Stage 5 optional cut.
- All four Scout C5 reduction paths remain live pending Stage 5–8 evidence.
