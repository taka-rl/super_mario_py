"""
Compare two perf CSVs (before vs. after). Prints a summary and can plot overlays.

Usage:
  python -m tools.compare_perf logs/before.csv logs/after.csv \
      --plot-out logs/compare.png --no-show

Requires:
  matplotlib (pip install matplotlib)
"""

import argparse
import csv
import math
import statistics
from typing import List, Dict, Tuple
import matplotlib.pyplot as plt


def _to_float(v: str) -> float:
    if v is None or v == "":
        return math.nan
    try:
        return float(v)
    except Exception:
        return math.nan


def _read_csv(path: str) -> List[Dict[str, str]]:
    with open(path, newline="") as f:
        r = csv.DictReader(f)
        return list(r)


def _filter_phase(rows: List[Dict[str, str]], phase: str) -> List[Dict[str, str]]:
    return [r for r in rows if (r.get("phase") or "") == phase]


def _col_floats(rows: List[Dict[str, str]], key: str) -> List[float]:
    vals = []
    for r in rows:
        vals.append(_to_float(r.get(key, "")))
    # keep NaNs; we'll ignore them in aggregations
    return vals


def _nan_stats(vals: List[float]) -> Dict[str, float]:
    xs = [v for v in vals if not math.isnan(v)]
    if not xs:
        return {"mean": math.nan, "median": math.nan, "p95": math.nan, "min": math.nan, "max": math.nan, "count": 0}
    xs_sorted = sorted(xs)
    p95_idx = max(0, int(0.95 * (len(xs_sorted)-1)))
    return {
        "mean": statistics.fmean(xs),
        "median": statistics.median(xs),
        "p95": xs_sorted[p95_idx],
        "min": xs_sorted[0],
        "max": xs_sorted[-1],
        "count": len(xs),
    }


def _event_values(rows: List[Dict[str, str]], event_name: str, field: str) -> List[float]:
    out = []
    for r in rows:
        if (r.get("event") or "") == event_name:
            out.append(_to_float(r.get(field, "")))
    return out


def summarize(rows: List[Dict[str, str]]) -> Dict[str, Dict[str, float]]:
    """
    Returns a structured summary:
      {
        "init_ms": {mean/median/...},
        "reset_ms": {...},
        "gameover_ms": {...},
        "play_fps": {...},
        "play_cpu": {...},
        "play_rss_mb": {...},
      }
    """
    s = {}

    # Events (init/reset/gameover) -> take all occurrences if any
    s["init_ms"]     = _nan_stats(_event_values(rows, "init_done", "init_ms"))
    s["reset_ms"]    = _nan_stats(_event_values(rows, "reset_done", "reset_ms"))
    s["gameover_ms"] = _nan_stats(_event_values(rows, "gameover_done", "gameover_ms"))

    # Play loop aggregates
    play_rows = _filter_phase(rows, "play")
    s["play_fps"]    = _nan_stats(_col_floats(play_rows, "fps"))
    s["play_cpu"]    = _nan_stats(_col_floats(play_rows, "cpu"))
    s["play_rss_mb"] = _nan_stats(_col_floats(play_rows, "rss_mb"))

    return s


def _print_side_by_side(title: str, before: Dict[str, float], after: Dict[str, float], unit: str = ""):
    def fmt(v):
        return "nan" if math.isnan(v) else f"{v:.3f}"

    print(f"\n=== {title} ===")
    headers = ["stat", "before", "after", "delta (after - before)"]
    print(f"{headers[0]:<10}  {headers[1]:>12}  {headers[2]:>12}  {headers[3]:>20}")
    for k in ("mean", "median", "p95", "min", "max", "count"):
        b = before.get(k, math.nan)
        a = after.get(k, math.nan)
        d = (a - b) if (not math.isnan(a) and not math.isnan(b)) else math.nan
        print(f"{k:<10}  {fmt(b):>12}  {fmt(a):>12}  {fmt(d):>20} {unit}")


def _overlay_plot(before_rows: List[Dict[str, str]], after_rows: List[Dict[str, str]], out: str, dpi: int, no_show: bool):
    def extract(rows, key):
        x = [_to_float(r.get("t_rel_s", "")) for r in rows]
        y = [_to_float(r.get(key, "")) for r in rows]
        # Normalize t to start at 0 for each run, to make comparison fair
        if x and not math.isnan(x[0]):
            t0 = x[0]
            x = [xi - t0 for xi in x]
        return x, y

    fig = plt.figure(figsize=(12, 8))
    ax1 = fig.add_subplot(2, 1, 1)  # CPU
    ax2 = fig.add_subplot(2, 1, 2)  # RSS

    bx_cpu_x, bx_cpu_y = extract(before_rows, "cpu")
    ax_cpu_x, ax_cpu_y = extract(after_rows, "cpu")

    bx_rss_x, bx_rss_y = extract(before_rows, "rss_mb")
    ax_rss_x, ax_rss_y = extract(after_rows, "rss_mb")

    ax1.plot(bx_cpu_x, bx_cpu_y, label="CPU% (before)")
    ax1.plot(ax_cpu_x, ax_cpu_y, label="CPU% (after)")
    ax1.set_ylabel("CPU %")
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    ax2.plot(bx_rss_x, bx_rss_y, label="RSS MB (before)")
    ax2.plot(ax_rss_x, ax_rss_y, label="RSS MB (after)")
    ax2.set_ylabel("RSS (MB)")
    ax2.set_xlabel("time since start (s)")
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    fig.tight_layout()
    if out:
        fig.savefig(out, dpi=dpi)
        print(f"Saved comparison plot to {out}")
    if not no_show:
        plt.show()


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("before_csv")
    p.add_argument("after_csv")
    p.add_argument("--plot-out", default=None, help="Optional PNG to save overlay (CPU & RSS vs time).")
    p.add_argument("--dpi", type=int, default=120)
    p.add_argument("--no-show", action="store_true")
    args = p.parse_args(argv)

    before = _read_csv(args.before_csv)
    after  = _read_csv(args.after_csv)

    s_before = summarize(before)
    s_after  = summarize(after)

    print("\n########## PERF COMPARISON ##########")
    _print_side_by_side("INIT (ms)", s_before["init_ms"], s_after["init_ms"], "ms")
    _print_side_by_side("RESET (ms)", s_before["reset_ms"], s_after["reset_ms"], "ms")
    _print_side_by_side("GAMEOVER (ms)", s_before["gameover_ms"], s_after["gameover_ms"], "ms")
    _print_side_by_side("PLAY FPS", s_before["play_fps"], s_after["play_fps"])
    _print_side_by_side("PLAY CPU %", s_before["play_cpu"], s_after["play_cpu"], "%")
    _print_side_by_side("PLAY RSS MB", s_before["play_rss_mb"], s_after["play_rss_mb"], "MB")

    if args.plot_out or not args.no_show:
        _overlay_plot(before, after, out=args.plot_out, dpi=args.dpi, no_show=args.no_show)


if __name__ == "__main__":
    main()
