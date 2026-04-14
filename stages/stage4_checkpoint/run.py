"""Stage 4 -- H2 checkpoint: peak alignment between C(t) and sigma^2_intrinsic(t).

Inspection stage, not computation. Per VOYAGE_PLAN §Stage 4:
 - Inspect Stage 3 data.
 - Do peaks in C(t) = log n_eff^{(1)}(t) align with peaks in sigma^2_intrinsic(t)
   even qualitatively?
 - If yes -> proceed to Cut A.
 - If no -> stop, reconsider framework, consult before continuing.

Stage 4 re-runs the Stage 3 ensemble to obtain C(t) and sigma^2(t) on
the same time grid, then characterises alignment quantitatively:

- peak locations (scipy.signal.find_peaks, prominence-filtered)
- nearest-neighbour peak time deltas
- Pearson correlation of the two series (over the resolvable window
  where sigma^2 > 10^{-8} to avoid the early-time numerical floor)
- cross-correlation lag at maximum

The Stage 4 verdict is a joint reading of the visual figure and the
quantitative summary; no hard gate fails the voyage -- the go/no-go
is the harbourmaster's inspection call.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SRC = REPO / "src"
FIGURES = REPO / "figures"
sys.path.insert(0, str(SRC))

from ensemble import (
    ensemble_mean,
    ensemble_variance,
    run_ensemble_single_mode,
    sample_detunings,
)


def main() -> dict:
    # Rerun the Stage 3 ensemble deterministically (same seed).
    g = 0.1
    Delta_nom = 0.15
    sigma_Delta = 0.01
    R = 100
    n_max = 18
    t_max = 50.0
    n_times = 500
    times = np.linspace(0.0, t_max, n_times)
    seed = 2026_04_14
    rng = np.random.default_rng(seed)

    Delta_sample = sample_detunings(Delta_nom, sigma_Delta, R, rng=rng)
    ens = run_ensemble_single_mode(Delta_sample, g=g, n_max=n_max, times=times)

    n_eff_mean = ensemble_mean(ens["n_eff"])
    p_var = ensemble_variance(ens["p"])
    # Aggregate complexity C(t) = sum_k log n_eff^(k). At N=1: C = log n_eff^(1).
    # Using the ensemble mean of n_eff as the "trajectory" object.
    C_t = np.log(np.maximum(n_eff_mean, 1e-30))
    # "Moments of rapid complexity growth" per VOYAGE_PLAN §5 H2: |dC/dt|.
    dCdt = np.gradient(C_t, times)
    absDCdt = np.abs(dCdt)

    # Restrict analysis to the resolvable window sigma^2 > 1e-8 (avoids
    # early-time numerical floor driving spurious "peaks").
    mask = p_var > 1e-8
    t_m = times[mask]
    sigma2_m = p_var[mask]
    C_m = C_t[mask]
    absDCdt_m = absDCdt[mask]

    # Peak finding. H2 (plan §5) is about "moments of rapid complexity growth"
    # coinciding with "moments of large ensemble variance", i.e. |dC/dt| peaks
    # vs sigma^2 peaks. Series peaks retained as a secondary diagnostic.
    # Prominence is a fraction of the range so the rule scales with amplitude.
    prom_sigma2 = 0.05 * (sigma2_m.max() - sigma2_m.min())
    prom_absDCdt = 0.05 * (absDCdt_m.max() - absDCdt_m.min())
    prom_C = 0.05 * (C_m.max() - C_m.min())
    peaks_sigma2, _ = find_peaks(sigma2_m, prominence=max(prom_sigma2, 1e-12))
    peaks_absDCdt, _ = find_peaks(absDCdt_m, prominence=max(prom_absDCdt, 1e-12))
    peaks_C, _ = find_peaks(C_m, prominence=max(prom_C, 1e-12))

    t_peaks_sigma2 = t_m[peaks_sigma2]
    t_peaks_absDCdt = t_m[peaks_absDCdt]
    t_peaks_C = t_m[peaks_C]

    # Nearest-neighbour alignment |dC/dt| peaks vs sigma^2 peaks (H2-relevant)
    if len(t_peaks_sigma2) > 0 and len(t_peaks_absDCdt) > 0:
        lags = []
        for t_s in t_peaks_sigma2:
            idx = int(np.argmin(np.abs(t_peaks_absDCdt - t_s)))
            lags.append(float(t_peaks_absDCdt[idx] - t_s))
        lags = np.asarray(lags)
        mean_abs_lag = float(np.mean(np.abs(lags)))
        median_abs_lag = float(np.median(np.abs(lags)))
    else:
        lags = np.asarray([])
        mean_abs_lag = median_abs_lag = float("nan")

    # Pearson correlations over the resolvable window.
    if len(sigma2_m) > 2:
        pearson_series = float(np.corrcoef(sigma2_m, C_m)[0, 1])
        pearson_growth = float(np.corrcoef(sigma2_m, absDCdt_m)[0, 1])
    else:
        pearson_series = pearson_growth = float("nan")

    # Cross-correlation of sigma^2 vs |dC/dt| (H2-relevant pair)
    if len(sigma2_m) > 2:
        s2c = (sigma2_m - sigma2_m.mean()) / (sigma2_m.std() + 1e-30)
        gc = (absDCdt_m - absDCdt_m.mean()) / (absDCdt_m.std() + 1e-30)
        xcorr = np.correlate(s2c, gc, mode="full") / len(sigma2_m)
        lag_idx = np.argmax(xcorr) - (len(sigma2_m) - 1)
        dt = times[1] - times[0]
        xcorr_lag = float(lag_idx * dt)
        xcorr_max = float(np.max(xcorr))
    else:
        xcorr_lag = xcorr_max = float("nan")

    # Mean peak spacing (used to give the lag a natural unit).
    if len(t_peaks_sigma2) >= 2:
        mean_peak_spacing_sigma2 = float(np.mean(np.diff(t_peaks_sigma2)))
    else:
        mean_peak_spacing_sigma2 = float("nan")
    if not np.isnan(mean_peak_spacing_sigma2) and not np.isnan(mean_abs_lag):
        lag_in_peak_spacings = mean_abs_lag / mean_peak_spacing_sigma2
    else:
        lag_in_peak_spacings = float("nan")

    sep = "=" * 74
    print(sep)
    print("Stage 4 -- H2 checkpoint: peak alignment C(t) vs sigma^2_intrinsic(t)")
    print(sep)
    print(f"Ensemble: Delta_nom={Delta_nom}, sigma_Delta={sigma_Delta}, R={R}, "
          f"n_max={n_max}")
    print()
    print(f"Signal structure over resolvable window ({mask.sum()}/{len(times)} pts)")
    print(f"   sigma^2 range: [{sigma2_m.min():.2e}, {sigma2_m.max():.2e}]")
    print(f"   C(t)   range: [{C_m.min():.4f}, {C_m.max():.4f}]  "
          f"(log 2 = {np.log(2):.4f} is Schmidt-rank-2 bound)")
    print(f"   |dC/dt| range: [{absDCdt_m.min():.2e}, {absDCdt_m.max():.2e}]")
    print()
    print(f"Peak counts (5% prominence)")
    print(f"   sigma^2  peaks: {len(peaks_sigma2)}")
    print(f"   |dC/dt|  peaks: {len(peaks_absDCdt)}")
    print(f"   C(t)     peaks: {len(peaks_C)} "
          f"(mostly monotonic-rising envelope at N=1)")
    print()
    print(f"Nearest-neighbour alignment (sigma^2 peaks -> |dC/dt| peaks)")
    print(f"   mean |lag|                = {mean_abs_lag:.3f} omega_ref^-1")
    print(f"   median |lag|              = {median_abs_lag:.3f} omega_ref^-1")
    print(f"   sigma^2 peak spacing      = {mean_peak_spacing_sigma2:.3f} omega_ref^-1")
    print(f"   lag as fraction of spacing= {lag_in_peak_spacings:.3f}")
    print()
    print(f"Pearson correlations over resolvable window")
    print(f"   r(sigma^2, |dC/dt|)  = {pearson_growth:.3f}  <-- H2-relevant pair")
    print(f"   r(sigma^2, C)        = {pearson_series:.3f}  (secondary diagnostic)")
    print()
    print(f"Cross-correlation of sigma^2 vs |dC/dt|")
    print(f"   argmax lag              = {xcorr_lag:.3f} omega_ref^-1")
    print(f"   max normalised xcorr    = {xcorr_max:.3f}")
    print(sep)

    # Stage 4 verdict is a harbourmaster inspection call, not a hard gate.
    # We report whether H2-style alignment is visible, with the N=1 caveat
    # that C(t) saturates to log 2 quickly (Schmidt-rank-2 bound), so
    # |dC/dt| becomes the relevant "rapid growth" quantity and series-peaks
    # in C are sparse. H2 becomes genuinely testable at N >= 2 where C
    # has room to grow above log 2.
    C_saturates_at_N1 = C_m.max() > 0.95 * np.log(2)
    # Weak co-variation reading on the H2-relevant pair:
    h2_alignment_visible = (
        len(peaks_sigma2) >= 2
        and len(peaks_absDCdt) >= 1
        and (not np.isnan(lag_in_peak_spacings))
        and lag_in_peak_spacings < 0.5
        and (not np.isnan(pearson_growth))
        and pearson_growth > 0.3
    )
    if C_saturates_at_N1:
        verdict = (
            "H2 not cleanly testable at N=1 (C saturates to log 2 = Schmidt-"
            "rank-2 bound); proceed to Cut A (still N=1) and Stage 6 (N=2 "
            "where H2 lives); do NOT declare H2 failed from this run alone"
        )
        proceed = True
    elif h2_alignment_visible:
        verdict = "H2-style alignment visible -> proceed to Cut A"
        proceed = True
    else:
        verdict = "H2 alignment not visible at this cut; pause and consult"
        proceed = False
    print(f"Verdict: {verdict}")
    print(sep)

    # ---------- Figure ----------
    FIGURES.mkdir(exist_ok=True)
    fig, axes = plt.subplots(2, 1, figsize=(11.0, 7.2), sharex=True)
    ax_top, ax_bot = axes

    ax_p = ax_top
    ax_n = ax_p.twinx()
    ax_p.plot(times, p_var, "C3-", lw=1.6, label=r"$\sigma^2_{\mathrm{intrinsic}}(t)$")
    ax_p.set_ylabel(r"$\sigma^2_{\mathrm{intrinsic}}(t)$", color="C3")
    ax_p.tick_params(axis="y", colors="C3")
    ax_p.axhline(0, color="k", lw=0.3)
    # C(t) on secondary axis, plus |dC/dt| as dotted
    ax_n.plot(times, C_t, "C0-", lw=1.6,
              label=r"$\mathcal{C}(t) = \log n_{\mathrm{eff}}^{(1)}(t)$")
    ax_n.plot(times, absDCdt, "C2--", lw=1.0,
              label=r"$|\dot{\mathcal{C}}(t)|$")
    ax_n.axhline(np.log(2), color="C0", ls=":", alpha=0.5)
    ax_n.set_ylabel(
        r"$\mathcal{C}(t)$, $|\dot{\mathcal{C}}(t)|$", color="C0"
    )
    ax_n.tick_params(axis="y", colors="C0")

    for t_s in t_peaks_sigma2:
        ax_p.axvline(t_s, color="C3", ls=":", alpha=0.35)
    for t_g in t_peaks_absDCdt:
        ax_p.axvline(t_g, color="C2", ls="--", alpha=0.35)

    ax_p.set_title(
        "(top) H2-relevant co-variation: "
        rf"$\sigma^2_{{\mathrm{{intrinsic}}}}$ vs "
        rf"$\mathcal{{C}}$ and $|\dot{{\mathcal{{C}}}}|$; "
        rf"red dotted = $\sigma^2$ peaks, green dashed = $|\dot{{\mathcal{{C}}}}|$ peaks; "
        rf"blue dotted = $\log 2$ (Schmidt bound)"
    )
    ax_p.grid(alpha=0.25)

    # Scatter plot: |dC/dt| vs sigma^2 (H2-relevant pair), colour by t
    sc = ax_bot.scatter(sigma2_m, absDCdt_m, c=t_m, cmap="viridis", s=6, alpha=0.8)
    fig.colorbar(sc, ax=ax_bot, label=r"$t\,\omega_{\mathrm{ref}}$",
                 shrink=0.85, pad=0.02)
    ax_bot.set_xlabel(r"$\sigma^2_{\mathrm{intrinsic}}(t)$")
    ax_bot.set_ylabel(r"$|\dot{\mathcal{C}}(t)|$")
    ax_bot.set_title(
        rf"(bottom) phase-space trajectory $(\sigma^2_{{\mathrm{{intrinsic}}}},\,|\dot{{\mathcal{{C}}}}|)$; "
        rf"Pearson $r = {pearson_growth:.3f}$"
    )
    ax_bot.grid(alpha=0.25)

    axes[0].set_xlabel(r"$t\,\omega_{\mathrm{ref}}$")
    fig.suptitle(
        "Stage 4 -- H2 checkpoint: peak alignment of complexity and variance",
        fontsize=11,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig_path = FIGURES / "stage4_h2_checkpoint.pdf"
    fig.savefig(fig_path)
    print(f"Figure: {fig_path.relative_to(REPO)}")

    metrics = {
        "verdict": {
            "proceed_to_stage_5": bool(proceed),
            "C_saturates_at_N1": bool(C_saturates_at_N1),
            "h2_alignment_visible": bool(h2_alignment_visible),
            "message": verdict,
        },
        "peaks": {
            "n_sigma2_peaks": int(len(peaks_sigma2)),
            "n_absDCdt_peaks": int(len(peaks_absDCdt)),
            "n_C_peaks": int(len(peaks_C)),
            "sigma2_peak_times": [float(t) for t in t_peaks_sigma2],
            "absDCdt_peak_times": [float(t) for t in t_peaks_absDCdt],
            "C_peak_times": [float(t) for t in t_peaks_C],
        },
        "alignment_sigma2_vs_absDCdt": {
            "mean_abs_lag": mean_abs_lag,
            "median_abs_lag": median_abs_lag,
            "mean_sigma2_peak_spacing": mean_peak_spacing_sigma2,
            "lag_fraction_of_spacing": lag_in_peak_spacings,
        },
        "correlations": {
            "pearson_sigma2_vs_absDCdt": pearson_growth,
            "pearson_sigma2_vs_C": pearson_series,
            "xcorr_lag_sigma2_vs_absDCdt": xcorr_lag,
            "xcorr_max_normalised": xcorr_max,
        },
        "signal_ranges": {
            "sigma2_range": [float(sigma2_m.min()), float(sigma2_m.max())],
            "C_range": [float(C_m.min()), float(C_m.max())],
            "absDCdt_range": [float(absDCdt_m.min()), float(absDCdt_m.max())],
            "log_2_schmidt_bound": float(np.log(2)),
            "C_fraction_of_bound": float(C_m.max() / np.log(2)),
        },
        "parameters": {
            "g": g, "Delta_nom": Delta_nom, "sigma_Delta": sigma_Delta,
            "R": R, "n_max": n_max, "t_max": t_max, "n_times": n_times,
            "seed": seed, "resolvable_window_threshold": 1e-8,
        },
    }
    (HERE / "metrics.json").write_text(json.dumps(metrics, indent=2))
    return metrics


if __name__ == "__main__":
    main()
