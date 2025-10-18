import argparse
import csv
import math
import re
from pathlib import Path
from statistics import median


def _to_float(x, default=None):
    try:
        if x is None or x == "":
            return default
        return float(x)
    except Exception:
        return default


_EVENT_RE = re.compile(r"^s(\d+)_end_(reset|gameover|game_clear)_done$", re.IGNORECASE)


def parse_event(ev: str):
    """
    Normalize event strings.

    Returns: (event_base, scenario_int)
      - event_base in {"init_done","reset_done","gameover_done","game_clear_done"} or None
      - scenario_int is int (e.g., 1 for 'S1_end_reset_done') or None
    """
    if not ev:
        return None, None
    ev_l = ev.strip().lower()
    if ev_l == "init_done":
        return "init_done", None

    m = _EVENT_RE.match(ev_l)
    if not m:
        return None, None

    s_num = int(m.group(1))
    kind = m.group(2)
    base_map = {
        "reset": "reset_done",
        "gameover": "gameover_done",
        "game_clear": "game_clear_done",
    }
    return base_map.get(kind), s_num


def percentile(values: list, p: int) -> float | None:
    """
    Return the p-th percentile value from the list of values.
    What “FPS (p1 — worst 1%)” means: 
    Percentile basics: the p1 (1st percentile) is the value that 1% of samples are at or below.
    
    - FPS (p1 — worst 1%):
    Higher is better for FPS. Therefore, the 1st percentaile FPS represents the worst 1% of frames-i.e., 
    how bad things get during the worst 1% of time. It’s much more robust than the absolute minimum (which can be a single hiccup).
    
    - CPU% (p95):
    The 95th percentile is often used to represent spikes, since higher values are worse for these metrics.
    p95 tells you how high the CPU% gets during the worst 5% of the time. 
    
    Args:
        values: list of numeric values (or empty)
        p: percentile to compute (0-100)
    Returns:
        The p-th percentile value, or None if values is empty.

    """
    if not values:
        return None
    v = sorted(values)
    if len(v) == 1:
        return v[0]
    idx = max(0, min(len(v) - 1, int(math.floor((p / 100.0) * (len(v) - 1)))))
    return v[idx]


def load_csv(paths):
    """
    Load one or more CSVs and attach:
      _event_base, _scenario (normalized)
      numeric conversions for: t_rel_s, fps, cpu, rss_mb, cache_count, cache_mb, init_ms, reset_ms, gameover_ms
    """
    if isinstance(paths, (str, Path)):
        paths = [paths]

    rows = []
    for p in paths:
        with open(p, "r", newline="", encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r:
                ev = row.get("event", "")
                base, scen = parse_event(ev)
                row["_event_base"] = base
                row["_scenario"] = scen

                # numerics we care about
                row["_t_rel_s"] = _to_float(row.get("t_rel_s"))
                row["_fps"] = _to_float(row.get("fps"))
                row["_cpu"] = _to_float(row.get("cpu"))
                row["_rss_mb"] = _to_float(row.get("rss_mb"))
                row["_cc"] = _to_float(row.get("cache_count"))
                row["_cmb"] = _to_float(row.get("cache_mb"))
                row["_init_ms"] = _to_float(row.get("init_ms"))
                row["_reset_ms"] = _to_float(row.get("reset_ms"))
                row["_go_ms"] = _to_float(row.get("gameover_ms"))

                # normalize phase
                ph = row.get("phase") or ""
                row["_phase"] = ph.strip().lower()

                rows.append(row)
    return rows


def summarize_play_phase(rows) -> dict:
    """
    Summarize A. Steady-state (play phase only) metrics including:
        - FPS median
        - FPS p1 (worst 1%)
        - CPU% median
        - CPU% p95 (spikes)
        - RSS MB median
        - RSS MB max
        - number of samples
    """
    play = [r for r in rows if r.get("_phase") == "play"]
    fps = [r["_fps"] for r in play if r.get("_fps") is not None]
    cpu = [r["_cpu"] for r in play if r.get("_cpu") is not None]
    rss = [r["_rss_mb"] for r in play if r.get("_rss_mb") is not None]

    return {
        "fps_median": median(fps) if fps else None,
        "fps_p1": percentile(fps, 1) if fps else None,
        "cpu_median": median(cpu) if cpu else None,
        "cpu_p95": percentile(cpu, 95) if cpu else None,
        "rss_median": median(rss) if rss else None,
        "rss_max": max(rss) if rss else None,
        "n_samples": len(play),
    }


def summarize_phase_timings(rows):
    """
    Summarize B. Phase timings from normalized events.
    Includes:
        - init_ms (from init_done)
        - reset_ms_S{n} (from reset_done with scenario n)
        - gameover_ms_S{n} (from gameover_done with scenario n)
        
    Returns:
        A dict with keys:
            - init_ms
            - reset_ms_S{n} for each scenario n
            - gameover_ms_S{n} for each scenario n 
    """
    out = {}

    # init
    init_rows = [r for r in rows if r.get("_event_base") == "init_done"]
    if init_rows:
        # first one encountered
        r0 = init_rows[0]
        out["init_ms"] = r0.get("_init_ms")

    # resets with scenario numbers
    for r in rows:
        if r.get("_event_base") == "reset_done":
            s = r.get("_scenario")
            key = f"reset_ms_S{s}" if s is not None else "reset_ms"
            out[key] = r.get("_reset_ms")

    # gameovers with scenario numbers
    for r in rows:
        if r.get("_event_base") == "gameover_done":
            s = r.get("_scenario")
            key = f"gameover_ms_S{s}" if s is not None else "gameover_ms"
            out[key] = r.get("_go_ms")

    return out


def summarize_cache_snapshots(rows):
    """
    Summarize C. Asset cache snapshots immediately after key events.
    Includes snapshots after:
        - init_done
        - reset_done (each scenario)
        - gameover_done (each scenario)
        
    Returns:
        A list of tuples: (label, cache_count, cache_mb)
    """
    snaps = []

    # After init
    for r in rows:
        if r.get("_event_base") == "init_done":
            snaps.append(("After init", r.get("_cc"), r.get("_cmb")))
            break

    # After each scenario reset
    for r in rows:
        if r.get("_event_base") == "reset_done":
            s = r.get("_scenario")
            label = f"After S{s} reset" if s is not None else "After reset"
            snaps.append((label, r.get("_cc"), r.get("_cmb")))

    # After each scenario gameover
    for r in rows:
        if r.get("_event_base") == "gameover_done":
            s = r.get("_scenario")
            label = f"After S{s} gameover" if s is not None else "After gameover"
            snaps.append((label, r.get("_cc"), r.get("_cmb")))

    return snaps


def main():
    ap = argparse.ArgumentParser(description="Summarize perf CSV(s) produced by mario-perf.")
    ap.add_argument("csv", nargs="+", help="One or more perf CSV files.")
    args = ap.parse_args()

    rows = load_csv(args.csv)

    # A. Steady state
    a = summarize_play_phase(rows)
    print("A. Steady-state (play phase only)")
    print(f"FPS (median): {a['fps_median']:.3f}" if a['fps_median'] is not None else "FPS (median): n/a")
    print(f"FPS (p1 — worst 1%): {a['fps_p1']:.3f}" if a['fps_p1'] is not None else "FPS (p1 — worst 1%): n/a")
    print(f"CPU% (median): {a['cpu_median']:.3f}" if a['cpu_median'] is not None else "CPU% (median): n/a")
    print(f"CPU% (p95 — spikes): {a['cpu_p95']:.3f}" if a.get('cpu_p95') is not None else "CPU% (p95 — spikes): n/a")
    print(f"RSS MB (median): {a['rss_median']:.3f}" if a['rss_median'] is not None else "RSS MB (median): n/a")
    print(f"RSS MB (max): {a['rss_max']:.3f}" if a['rss_max'] is not None else "RSS MB (max): n/a")
    print(f"samples (play rows): {a['n_samples']}")
    print()

    # B. Phase timings
    b = summarize_phase_timings(rows)
    print("B. Phase timings")
    if "init_ms" in b:
        print(f"init_ms: {b['init_ms']:.3f}")
    for k in sorted([k for k in b.keys() if k.startswith("reset_ms")]):
        v = b[k]
        print(f"{k}: {v:.3f}" if v is not None else f"{k}: n/a")
    for k in sorted([k for k in b.keys() if k.startswith("gameover_ms")]):
        v = b[k]
        print(f"{k}: {v:.3f}" if v is not None else f"{k}: n/a")
    print()

    # C. Asset cache snapshot
    snaps = summarize_cache_snapshots(rows)
    print("C. Asset cache snapshot")
    if not snaps:
        print("(no cache stats recorded)")
    else:
        for label, cc, cmb in snaps:
            cc_s = "n/a" if cc is None else str(int(cc))
            cmb_s = "n/a" if cmb is None else f"{float(cmb):.3f}"
            print(f"{label}: cache_count={cc_s} | cache_mb={cmb_s}")


if __name__ == "__main__":
    main()
