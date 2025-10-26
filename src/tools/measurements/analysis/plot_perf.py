"""
Plot a single perf CSV (from PerfCSVLogger).

Usage:
    python -m tools.measurements.plot_perf logs/perf.csv --out logs/perf_plot.png
    perf-plot logs/perf.csv --out logs/plot.png

Requires:
  matplotlib (pip install matplotlib)
"""

import argparse, csv, math
from typing import List, Dict, Tuple

import matplotlib.pyplot as plt


def _to_float(v: str) -> float:
    """
    Convert string to float, return NaN if not possible.
    
    Returns:
        float value or NaN
    """
    if v is None or v == "":
        return math.nan
    try:
        return float(v)
    except Exception:
        return math.nan


def _read_csv(path: str) -> List[Dict[str, str]]:
    """
    Read CSV file into list of rows (dict).
    Each row is a dict of column name to string value.
    
    Returns:
        List of rows (dict)
    """
    with open(path, newline="") as f:
        r = csv.DictReader(f)
        return list(r)


def _extract_series(rows: List[Dict[str, str]], key: str) -> Tuple[list, list]:
    """
    Extract (x, y) series for the given key. x is t_rel_s. y is the value for 'key'.
    Skip rows with non-numeric or missing values. 
    
    Returns:
        (x, y) where x and y are lists of floats.
    """
    x, y = [], []
    for row in rows:
        t = _to_float(row.get("t_rel_s", ""))  # robust to column order
        v = _to_float(row.get(key, ""))
        if not math.isnan(t):
            x.append(t)
            y.append(v)
    return x, y


def _phase_spans(rows: List[Dict[str, str]]) -> List[Tuple[float, float, str]]:
    """
    Create phase spans from rows. 
    Return [(start_t, end_t, phase), ...] contiguous spans by 'phase'.
    
    Returns:
        List of (start_t, end_t, phase) tuples.
    """
    spans: List[Tuple[float, float, str]] = []
    if not rows:
        return spans

    cur_phase = rows[0].get("phase", "") or ""
    start_t = _to_float(rows[0].get("t_rel_s", "0"))
    last_t = start_t

    for row in rows[1:]:
        t = _to_float(row.get("t_rel_s", "0"))
        ph = row.get("phase", "") or ""
        if ph != cur_phase:
            spans.append((start_t, last_t, cur_phase))
            cur_phase = ph
            start_t = t
        last_t = t

    spans.append((start_t, last_t, cur_phase))
    return spans


def _event_positions(rows: List[Dict[str, str]]) -> List[Tuple[float, str]]:
    """
    Extract event positions from rows. 
    Return [(t_rel_s, event_name), ...] for rows with non-empty 'event'.
    
    Returns:
        List of (t_rel_s, event_name) tuples.
    """
    pos = []
    for row in rows:
        name = (row.get("event") or "").strip()
        if name:
            pos.append((_to_float(row.get("t_rel_s", "0")), name))
    return pos


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("csv", help="Path to perf CSV")
    p.add_argument("--out", default=None, help="Optional PNG to save")
    p.add_argument("--dpi", type=int, default=120)
    p.add_argument("--no-show", action="store_true")
    p.add_argument("--include-cache", action="store_true",
                   help="Also plot cache_count and cache_mb on the bottom axis.")
    args = p.parse_args(argv)

    rows = _read_csv(args.csv)

    # Build figure: three stacked axes
    # Top: FPS, Middle: CPU%, Bottom: RSS (and optionally cache)
    fig = plt.figure(figsize=(12, 8))
    ax1 = fig.add_subplot(3, 1, 1)  # FPS
    ax2 = fig.add_subplot(3, 1, 2)  # CPU
    ax3 = fig.add_subplot(3, 1, 3)  # RSS + cache

    # Series
    x_fps, y_fps = _extract_series(rows, "fps")
    x_cpu, y_cpu = _extract_series(rows, "cpu")
    x_rss, y_rss = _extract_series(rows, "rss_mb")

    ax1.plot(x_fps, y_fps)
    ax1.set_ylabel("FPS")
    ax1.grid(True, alpha=0.3)

    ax2.plot(x_cpu, y_cpu)
    ax2.set_ylabel("CPU %")
    ax2.grid(True, alpha=0.3)

    ax3.plot(x_rss, y_rss, label="RSS MB")
    ax3.set_ylabel("RSS (MB)")
    ax3.set_xlabel("t_rel_s (s)")
    ax3.grid(True, alpha=0.3)

    if args.include_cache:
        x_cc, y_cc = _extract_series(rows, "cache_count")
        x_cb, y_cb = _extract_series(rows, "cache_mb")
        # Plot on twin axes for scale clarity
        ax3b = ax3.twinx()
        ax3b.plot(x_cc, y_cc, linestyle="--", label="cache_count")
        ax3b.plot(x_cb, y_cb, linestyle=":", label="cache_mb")
        ax3b.set_ylabel("cache_count / cache_mb")
        lines, labels = ax3.get_legend_handles_labels()
        lines2, labels2 = ax3b.get_legend_handles_labels()
        ax3b.legend(lines + lines2, labels + labels2, loc="upper right")
    else:
        ax3.legend(loc="upper right")

    # Shade phases & mark events
    spans = _phase_spans(rows)
    colors = {
        "init_startup": (0.8, 0.9, 1.0, 0.4),
        "play":         (0.9, 1.0, 0.9, 0.3),
        "reset":        (1.0, 0.95, 0.8, 0.3),
        "gameover":     (1.0, 0.8, 0.8, 0.3),
        "":             (0.95, 0.95, 0.95, 0.2),
    }
    for (s, e, ph) in spans:
        for ax in (ax1, ax2, ax3):
            ax.axvspan(s, e, color=colors.get(ph, colors[""]), lw=0)

    for (t, name) in _event_positions(rows):
        for ax in (ax1, ax2, ax3):
            ax.axvline(t, linestyle="--", alpha=0.5)
        ax1.text(t, ax1.get_ylim()[1]*0.9, name, rotation=90, va="top", ha="right", fontsize=8)

    fig.tight_layout()

    if args.out:
        fig.savefig(args.out, dpi=args.dpi)
        print(f"Saved plot to {args.out} ({args.dpi} dpi)")
    if not args.no_show:
        plt.show()


if __name__ == "__main__":
    main()
