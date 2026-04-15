"""Stage 8 synthesis figure (per VOYAGE_PLAN v0.2 + PA-05).

Assembles the voyage's cross-stage findings into one headline figure:

  (TL) Complementarity phase-space loop at N=2 B1 (C(t), sigma^2(t))
       parametric-in-t, re-generated here for visual crispness.
  (TR) Per-mode r_k across all Cut A / B / C points: H2 per-mode
       holds for the dominantly-coupled (innermost) mode; aggregate
       dilutes at N >= 2 by mode-decoupling.
  (BL) f_resolved vs C_bar scatter across all Cut A/B/C points.
       The honest H3 null: no monotone trend -- the two scalars have
       independent drivers. Retained as reporting auxiliary, not
       headline.
  (BR) QFI reduction vs |Delta|_min across all points: the regional
       contraction -- reduction holds (~10%) at outer detunings, breaks
       (22-30%) at inner / multi-mode configurations.

All data drawn from committed Stage 5, 6, 7 metrics.json except the
phase-space trajectory, which is re-propagated here (cheap at N=2).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SRC = REPO / "src"
FIGURES = REPO / "figures"
sys.path.insert(0, str(SRC))


def load_metrics():
    stages = {
        "stage5": REPO / "stages" / "stage5_cut_a" / "metrics.json",
        "stage6": REPO / "stages" / "stage6_cut_b" / "metrics.json",
        "stage7": REPO / "stages" / "stage7_cut_c" / "metrics.json",
    }
    return {k: json.loads(v.read_text()) for k, v in stages.items()}


def regen_n2_phase_space():
    """Short ensemble at Stage 6 B1 for the phase-space loop."""
    from ensemble import (
        ensemble_mean,
        ensemble_variance,
        run_ensemble_two_mode,
        sample_detunings,
    )
    g = 0.1
    sigma_Delta = 0.01
    R = 100
    t_max = 50.0
    n_times = 500
    times = np.linspace(0.0, t_max, n_times)
    # Reproduce Stage 6 B1 exactly. Stage 6 used:
    #   parent = SeedSequence(20260416), child_ss = parent.spawn(4),
    #   then run_config derived a second rng from the first via
    #   rng.bit_generator.random_raw() so d1 and d2 are INDEPENDENT
    #   draws. B1 is child index 0.
    child_ss = np.random.SeedSequence(2026_04_16).spawn(4)
    ss_B1 = child_ss[0]
    rng1 = np.random.default_rng(ss_B1)
    d1 = sample_detunings(0.15, sigma_Delta, R, rng=rng1)
    rng2 = np.random.default_rng(rng1.bit_generator.random_raw())
    d2 = sample_detunings(0.15, sigma_Delta, R, rng=rng2)
    assert not np.allclose(d1, d2), "d1 and d2 must be independent draws"
    ens = run_ensemble_two_mode(d1, d2, g=g, n_max=18, times=times)
    p_var = ensemble_variance(ens["p"])
    C = ensemble_mean(ens["C"])
    return times, C, p_var


def main():
    metrics = load_metrics()

    # ---- (TL) phase-space loop at N=2 B1 ----
    print("regenerating N=2 B1 ensemble for phase-space loop...", flush=True)
    t_n2, C_n2, sigma2_n2 = regen_n2_phase_space()

    # ---- (TR) per-mode r_k across points ----
    # Stage 5 (N=1): only aggregate r(sigma^2, |dC/dt|); at N=1, C=log n_eff^(1),
    # so aggregate = mode-1 r. Use pearson_sigma2_absDCdt.
    stage5_per_point = metrics["stage5"]["per_point"]
    stage5_points = []
    for key, rec in stage5_per_point.items():
        Delta = float(key)
        stage5_points.append((f"N=1 Δ={Delta:+.2f}", rec["pearson_sigma2_absDCdt"],
                              rec["qfi_median_rel_dev"], abs(Delta),
                              rec["timing_by_M"]["1000"]["f_resolved"],
                              rec["C_bar"]))

    # Stage 6 (N=2): only AGGREGATE growth-framing Pearson is committed in
    # metrics (per-mode r_k at N=2 was not decomposed -- audit gap, see
    # novelty_statement.md §Scope caveats). The figure labels these bars
    # "N=2 aggregate" and colours them accordingly; the top-right panel's
    # per-mode claim is specifically about N=1 and N=3 where per-mode was
    # measured.
    stage6_cfgs = metrics["stage6"]["configs"]
    stage6_points = []
    for label, rec in stage6_cfgs.items():
        Delta_min = min(abs(rec["Delta_1"]), abs(rec["Delta_2"]))
        stage6_points.append((f"N=2 {label}", rec["pearson_growth_framing"],
                              rec["qfi_median_rel_dev"], Delta_min,
                              rec["timing_by_M"]["1000"]["f_resolved"],
                              rec["C_bar"]))

    # Stage 7 (N=3): has pearson_growth_per_mode -- use mode 1 (innermost).
    # NB: QFI reduction was not recorded per-point in Stage 7 metrics (oversight;
    # extrapolation from Stage 6 is in notes but not measured). Use NaN as
    # placeholder so those points are omitted from the QFI panel but still
    # contribute to the H2 and H3 panels.
    stage7_results = metrics["stage7"]["results"]
    stage7_points_mode1 = []
    stage7_points_agg = []
    for key, rec in stage7_results.items():
        Delta_min = min(abs(d) for d in rec["Delta_triplet"])
        r_mode1 = rec["pearson_growth_per_mode"][0]
        r_agg = rec["pearson_growth_aggregate"]
        stage7_points_mode1.append((f"N=3 {key}", r_mode1,
                                     float("nan"), Delta_min,
                                     rec["timing_by_M"]["1000"]["f_resolved"],
                                     rec["C_bar"]))
        stage7_points_agg.append((f"N=3 agg {key}", r_agg))

    # ---- figure ----
    FIGURES.mkdir(exist_ok=True)
    fig, axes = plt.subplots(2, 2, figsize=(12.5, 9.5))
    ax_ps, ax_rk = axes[0]
    ax_scatter, ax_qfi = axes[1]

    # (TL) phase-space loop parametric in t
    sc = ax_ps.scatter(C_n2, sigma2_n2, c=t_n2, cmap="viridis", s=10, alpha=0.8)
    ax_ps.plot(C_n2, sigma2_n2, "-", color="0.6", lw=0.4, alpha=0.5)
    cbar = plt.colorbar(sc, ax=ax_ps, label=r"$t\,\omega_{\mathrm{ref}}$",
                        shrink=0.85, pad=0.02)
    ax_ps.set_xlabel(r"$\mathcal{C}(t) = \log n_{\mathrm{eff}}^{(1)} + \log n_{\mathrm{eff}}^{(2)}$")
    ax_ps.set_ylabel(r"$\sigma^2_{\mathrm{intrinsic}}(t)$")
    ax_ps.set_title(
        r"(TL) Complementarity phase-space, N=2 B1 ($\Delta_1 = \Delta_2 = 0.15$)"
        + "\n$\mathcal{C}$-peaks and $\sigma^2$-peaks sit on different loop branches"
    )
    ax_ps.grid(alpha=0.3)

    # (TR) H2 growth-framing Pearson across stages, honest-label variant.
    # N=1 bars ARE per-mode (aggregate=mode-1 trivially at N=1).
    # N=2 bars are AGGREGATE only (Stage 6 metrics did not commit per-mode
    # decomposition; see audit, novelty_statement.md §Scope caveats).
    # N=3 bars: show both per-mode-1 and aggregate separately.
    labels = []
    r_values = []
    colors = []
    for lab, r, *_ in stage5_points:
        labels.append(lab.replace("N=1 ", "N=1 mode-1 "))
        r_values.append(r); colors.append("C0")
    for lab, r, *_ in stage6_points:
        labels.append(lab.replace("N=2 ", "N=2 agg "))
        r_values.append(r); colors.append("C1")
    for lab, r, *_ in stage7_points_mode1:
        labels.append(lab.replace("N=3 ", "N=3 mode-1 "))
        r_values.append(r); colors.append("C2")
    for lab, r in stage7_points_agg:
        labels.append(lab.replace("N=3 agg ", "N=3 agg "))
        r_values.append(r); colors.append("C3")

    x = np.arange(len(labels))
    ax_rk.bar(x, r_values, color=colors, alpha=0.85, edgecolor="k", lw=0.4)
    ax_rk.axhline(0, color="k", lw=0.6)
    ax_rk.set_xticks(x)
    ax_rk.set_xticklabels(labels, rotation=55, ha="right", fontsize=7)
    ax_rk.set_ylabel(
        r"$r(\sigma^2,\,|\dot{\mathcal{C}}|)$"
        "\n(mode-1 where decomposed; aggregate otherwise)"
    )
    ax_rk.set_title(
        "(TR) H2 growth-framing Pearson across stages\n"
        "measured per-mode at $N=1, 3$; $N=2$ aggregate only (audit gap)"
    )
    ax_rk.set_ylim(-0.4, 0.7)
    ax_rk.grid(alpha=0.3, axis="y")
    # Legend proxy distinguishing per-mode vs aggregate
    from matplotlib.patches import Patch
    ax_rk.legend(handles=[
        Patch(facecolor="C0", label="N=1 per-mode (Stage 5; aggregate = mode-1)"),
        Patch(facecolor="C1", label="N=2 aggregate only (Stage 6)"),
        Patch(facecolor="C2", label="N=3 mode-1 (Stage 7)"),
        Patch(facecolor="C3", label="N=3 aggregate (Stage 7)"),
    ], loc="upper right", frameon=False, fontsize=7)

    # (BL) f_resolved vs C_bar scatter — the H3 null
    all_points = stage5_points + stage6_points + stage7_points_mode1
    # Split by N for colouring
    for pts, col, marker, lab in [
        (stage5_points, "C0", "o", "N=1"),
        (stage6_points, "C1", "s", "N=2"),
        (stage7_points_mode1, "C2", "^", "N=3"),
    ]:
        xs = [p[5] for p in pts]  # C_bar
        ys = [p[4] for p in pts]  # f_resolved
        ax_scatter.scatter(xs, ys, c=col, marker=marker, s=90, alpha=0.85,
                            edgecolors="k", lw=0.5, label=lab)
    ax_scatter.set_xlabel(r"$\bar{\mathcal{C}}$")
    ax_scatter.set_ylabel(r"$f_{\mathrm{resolved}}(M = 10^3)$")
    ax_scatter.set_title(
        r"(BL) H3-as-correlation: empirical null (PA-05)"
        + "\n"
        + r"$\bar{\mathcal{C}}$ and $f_{\mathrm{resolved}}$ have independent drivers"
    )
    ax_scatter.grid(alpha=0.3)
    ax_scatter.legend(loc="best", frameon=False, fontsize=8)

    # (BR) QFI reduction vs |Delta|_min (Stage 7 N=3 not measured; omitted)
    for pts, col, marker, lab in [
        (stage5_points, "C0", "o", "N=1 (Stage 5)"),
        (stage6_points, "C1", "s", "N=2 (Stage 6)"),
    ]:
        xs = [p[3] for p in pts]  # |Delta|_min
        ys = [100 * p[2] for p in pts]  # QFI median rel dev (%)
        ax_qfi.scatter(xs, ys, c=col, marker=marker, s=90, alpha=0.85,
                        edgecolors="k", lw=0.5, label=lab)
    ax_qfi.axhline(10, color="k", ls=":", alpha=0.6,
                   label="Gate 8 target (10%)")
    ax_qfi.set_xlabel(r"$|\Delta|_{\min} / \omega_{\mathrm{ref}}$")
    ax_qfi.set_ylabel(r"QFI median rel. dev. (%)")
    ax_qfi.set_title(
        "(BR) Physics finding: QFI-reduction boundary"
        + "\n"
        + r"first-order $F$-linearisation breaks at inner / multi-mode"
    )
    ax_qfi.set_ylim(0, 35)
    ax_qfi.grid(alpha=0.3)
    ax_qfi.legend(loc="best", frameon=False, fontsize=8)

    fig.suptitle(
        "Voyage synthesis — measurement-resolved complexity in a bounded "
        "spin-boson system",
        fontsize=12,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig_path = FIGURES / "stage8_synthesis.pdf"
    fig.savefig(fig_path, bbox_inches="tight")
    print(f"Figure: {fig_path.relative_to(REPO)}", flush=True)

    # ---- cross-stage summary metrics ----
    summary = {
        "H2_per_mode_growth_r": {
            "N1_by_Delta": {lab: r for lab, r, *_ in stage5_points},
            "N2_by_config": {lab: r for lab, r, *_ in stage6_points},
            "N3_mode1_by_config_D": {lab: r for lab, r, *_ in stage7_points_mode1},
            "N3_aggregate_by_config_D": {lab: r for lab, r in stage7_points_agg},
        },
        "QFI_median_rel_dev_vs_Delta_min": [
            {"stage": "N=1", "Delta_min": p[3], "qfi_rel_dev": p[2]}
            for p in stage5_points
        ] + [
            {"stage": "N=2", "Delta_min": p[3], "qfi_rel_dev": p[2]}
            for p in stage6_points
        ] + [
            {"stage": "N=3", "Delta_min": p[3], "qfi_rel_dev": p[2]}
            for p in stage7_points_mode1
        ],
        "H3_null_scatter": [
            {"stage": "N=1", "C_bar": p[5], "f_resolved_1e3": p[4]}
            for p in stage5_points
        ] + [
            {"stage": "N=2", "C_bar": p[5], "f_resolved_1e3": p[4]}
            for p in stage6_points
        ] + [
            {"stage": "N=3", "C_bar": p[5], "f_resolved_1e3": p[4]}
            for p in stage7_points_mode1
        ],
    }
    (HERE / "cross_stage_summary.json").write_text(
        safe_json_dumps(summary, indent=2)
    )
    return summary


def safe_json_dumps(obj, **kwargs):
    """JSON-dump with non-finite floats replaced by null (RFC 8259 compliant).

    Python's ``json.dumps`` emits bare ``NaN`` / ``Infinity`` by default,
    which are invalid JSON. Walk the object and replace non-finite floats
    with None before serialising.
    """
    import math

    def _clean(x):
        if isinstance(x, float):
            if not math.isfinite(x):
                return None
            return x
        if isinstance(x, dict):
            return {k: _clean(v) for k, v in x.items()}
        if isinstance(x, (list, tuple)):
            return [_clean(v) for v in x]
        return x

    return json.dumps(_clean(obj), **kwargs)


if __name__ == "__main__":
    main()
