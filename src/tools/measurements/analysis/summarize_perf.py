import argparse
import csv
import glob
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

    Returns: list[(label, cache_count, cache_mb)]
    """
    snaps = []

    # After init
    for r in rows:
        if r.get("_event_base") == "init_done":
            snaps.append(("after_init", r.get("_cc"), r.get("_cmb")))
            break

    # After each scenario reset
    for r in rows:
        if r.get("_event_base") == "reset_done":
            s = r.get("_scenario")
            label = f"after_S{s}_reset" if s is not None else "after_reset"
            snaps.append((label, r.get("_cc"), r.get("_cmb")))

    # After each scenario gameover
    for r in rows:
        if r.get("_event_base") == "gameover_done":
            s = r.get("_scenario")
            label = f"after_S{s}_gameover" if s is not None else "after_gameover"
            snaps.append((label, r.get("_cc"), r.get("_cmb")))

    return snaps


def _snap_list_to_map(snaps):
    """
    Convert snapshots list into a dict:
      { "after_init": {"cache_count": v, "cache_mb": v}, "after_S1_reset": {...}, ... }
    """
    out = {}
    for label, cc, cmb in snaps:
        out[label] = {"cache_count": cc, "cache_mb": cmb}
    return out


def summarize_run(csv_path) -> dict:
    """
    Summarize a single run (one CSV) into a nested dict:
      {
        "play": {...},
        "phase": {...},
        "cache": { label: {cache_count, cache_mb}, ... },
        "_source": <filename>
      }
    """
    rows = load_csv(csv_path)
    play = summarize_play_phase(rows)
    phase = summarize_phase_timings(rows)
    cache = _snap_list_to_map(summarize_cache_snapshots(rows))
    return {"play": play, "phase": phase, "cache": cache, "_source": str(csv_path)}


def _flatten_run_summary(run):
    """
    Flatten nested run summary into dotted keys for aggregation.
    Returns dict[str, float]
    """
    flat = {}
    for k, v in run.get("play", {}).items():
        if k == "n_samples":
            continue  # not aggregating counts as stats
        flat[f"play.{k}"] = v
    for k, v in run.get("phase", {}).items():
        flat[f"phase.{k}"] = v
    for label, d in run.get("cache", {}).items():
        for ck, cv in d.items():
            flat[f"cache.{label}.{ck}"] = cv
    return flat


def _aggregate_metric(values: list[float], drop_p: float | None):
    """
    Aggregate a list of numeric values into median/IQR/min/max/n.
    Optionally drop top/bottom p% as outliers.
    """
    vals = [v for v in values if v is not None]
    n_all = len(vals)
    if n_all == 0:
        return None

    vals.sort()
    if drop_p and drop_p > 0:
        k = int(math.floor((drop_p / 100.0) * n_all))
        vals = vals[k: n_all - k] if n_all - 2 * k > 0 else vals  # avoid empty

    n = len(vals)
    med = median(vals)
    q1 = percentile(vals, 25)
    q3 = percentile(vals, 75)
    mn = vals[0]
    mx = vals[-1]
    return {"median": med, "iqr_low": q1, "iqr_high": q3, "min": mn, "max": mx, "n_runs": n, "n_runs_raw": n_all}


def aggregate_runs(run_summaries: list[dict], drop_outliers_p: float | None):
    """
    Aggregate many per-run summaries into a condition summary.
    Returns:
      {
        "metrics": { dotted_key: agg_dict, ... },
        "present_keys": set[str],   # all dotted keys seen
      }
    """
    key_to_values = {}
    for run in run_summaries:
        flat = _flatten_run_summary(run)
        for k, v in flat.items():
            key_to_values.setdefault(k, []).append(v)

    out_metrics = {}
    for k, vals in key_to_values.items():
        agg = _aggregate_metric(vals, drop_outliers_p)
        if agg is not None:
            out_metrics[k] = agg

    return {"metrics": out_metrics, "present_keys": set(key_to_values.keys())}


def _delta(after: float | None, before: float | None):
    """
    Compare the results between before and after. 
    
    For each metric present in both:
        Δ_abs = median_after - median_before
        Δ_pct = 100 * (median_after / median_before - 1) (guard division by zero → “n/a”)
    
    Returns:
        d_abs: float or None
        d_pct: float or None
    """
    if after is None or before is None:
        return None, None
    d_abs = after - before
    d_pct = None if before == 0 else (100.0 * (after / before - 1.0))
    return d_abs, d_pct


def compare_conditions(cond_before: dict, cond_after: dict):
    """
    Compare two aggregated condition summaries on the medians.
    Returns dict[dotted_key] = {"before": {...}, "after": {...}, "delta_abs": x, "delta_pct": y}
    """
    kb = set(cond_before["metrics"].keys())
    ka = set(cond_after["metrics"].keys())
    common = sorted(kb & ka)

    out = {}
    for k in common:
        mb = cond_before["metrics"][k]["median"]
        ma = cond_after["metrics"][k]["median"]
        d_abs, d_pct = _delta(ma, mb)
        out[k] = {
            "before": cond_before["metrics"][k],
            "after": cond_after["metrics"][k],
            "delta_abs": d_abs,
            "delta_pct": d_pct,
        }

    extras_before = sorted(kb - ka)
    extras_after  = sorted(ka - kb)
    return out, extras_before, extras_after


def _fmt_val(v, digits=3):
    if v is None:
        return "n/a"
    return f"{v:.{digits}f}"


def _fmt_band(med, lo, hi, digits=3):
    if med is None:
        return "n/a"
    if lo is None or hi is None:
        return f"{med:.{digits}f}"
    return f"{med:.{digits}f} [{lo:.{digits}f}–{hi:.{digits}f}]"


def render_text_single(label, per_runs, cond_summary, quiet=False):
    if not quiet:
        print(f"== Per-run ({label}) ==")
        for i, r in enumerate(per_runs, start=1):
            src = Path(r.get("_source", f"run{i}")).name
            p = r["play"]
            line = (f"Run {i} ({src}) | FPS med={_fmt_val(p.get('fps_median'))}, p1={_fmt_val(p.get('fps_p1'))} | "
                    f"CPU med={_fmt_val(p.get('cpu_median'))}, p95={_fmt_val(p.get('cpu_p95'))} | "
                    f"RSS med={_fmt_val(p.get('rss_median'))}, max={_fmt_val(p.get('rss_max'))}")
            phase = r["phase"]
            if "init_ms" in phase:
                line += f" | init_ms={_fmt_val(phase['init_ms'])}"
            for k in sorted([k for k in phase if k.startswith("reset_ms_S")]):
                line += f" | {k}={_fmt_val(phase[k])}"
            for k in sorted([k for k in phase if k.startswith("gameover_ms_S")]):
                line += f" | {k}={_fmt_val(phase[k])}"
            print(line)
        print()

    print(f"== Condition summary ({label}) ==")
    M = cond_summary["metrics"]

    def g(k): return M.get(k, {})

    # Play table (text)
    print("A. Steady-state (play)")
    print(f"- FPS (median): {_fmt_band(g('play.fps_median').get('median'), g('play.fps_median').get('iqr_low'), g('play.fps_median').get('iqr_high'))}")
    print(f"- FPS (p1 — worst 1%): {_fmt_band(g('play.fps_p1').get('median'), g('play.fps_p1').get('iqr_low'), g('play.fps_p1').get('iqr_high'))}")
    print(f"- CPU% (median): {_fmt_band(g('play.cpu_median').get('median'), g('play.cpu_median').get('iqr_low'), g('play.cpu_median').get('iqr_high'))}")
    print(f"- CPU% (p95): {_fmt_band(g('play.cpu_p95').get('median'), g('play.cpu_p95').get('iqr_low'), g('play.cpu_p95').get('iqr_high'))}")
    print(f"- RSS MB (median): {_fmt_band(g('play.rss_median').get('median'), g('play.rss_median').get('iqr_low'), g('play.rss_median').get('iqr_high'))}")
    print(f"- RSS MB (max): {_fmt_band(g('play.rss_max').get('median'), g('play.rss_max').get('iqr_low'), g('play.rss_max').get('iqr_high'))}")
    print()

    # Phase timings
    print("B. Phase timings")
    if "phase.init_ms" in M:
        agg = M["phase.init_ms"]
        print(f"- init_ms: {_fmt_band(agg['median'], agg['iqr_low'], agg['iqr_high'])}")
    for k in sorted([k for k in M if k.startswith("phase.reset_ms_S")]):
        agg = M[k]
        print(f"- {k.split('.',1)[1]}: {_fmt_band(agg['median'], agg['iqr_low'], agg['iqr_high'])}")
    for k in sorted([k for k in M if k.startswith("phase.gameover_ms_S")]):
        agg = M[k]
        print(f"- {k.split('.',1)[1]}: {_fmt_band(agg['median'], agg['iqr_low'], agg['iqr_high'])}")
    print()

    # Cache snapshots
    print("C. Asset cache snapshot")
    cache_keys = sorted([k for k in M if k.startswith("cache.")])
    if not cache_keys:
        print("(no cache stats recorded)")
    else:
        # group by label
        buckets = {}
        for k in cache_keys:
            _, label, field = k.split(".", 2)
            buckets.setdefault(label, {})[field] = M[k]
        for label in sorted(buckets):
            cc = buckets[label].get("cache_count")
            cm = buckets[label].get("cache_mb")
            cc_s = _fmt_band(cc.get("median") if cc else None,
                             cc.get("iqr_low") if cc else None,
                             cc.get("iqr_high") if cc else None)
            cm_s = _fmt_band(cm.get("median") if cm else None,
                             cm.get("iqr_low") if cm else None,
                             cm.get("iqr_high") if cm else None)
            print(f"- {label}: cache_count={cc_s} | cache_mb={cm_s}")
    print()


def render_md_compare(label_before, cond_before, label_after, cond_after, deltas, extras_before, extras_after):
    # Build Markdown tables like your README

    def row_play(metric_key, label):
        b = cond_before["metrics"].get(metric_key)
        a = cond_after["metrics"].get(metric_key)
        def s(agg):
            return "-" if not agg else f"{agg['median']:.3f} [{agg['iqr_low']:.3f}–{agg['iqr_high']:.3f}]"
        d = deltas.get(metric_key)
        if d is None:
            delta_s = "-"
        else:
            da = d["delta_abs"]
            dp = d["delta_pct"]
            if da is None:
                delta_s = "-"
            elif dp is None:
                delta_s = f"{da:+.3f} (n/a)"
            else:
                delta_s = f"{da:+.3f} ({dp:+.1f}%)"
        return f"| {label} | {s(b)} | {s(a)} | {delta_s} |"

    print(f"### Steady-state (play phase only)")
    print(f"| Metrics | {label_before} | {label_after} | Δ(abs/%) |")
    print(f"| --- | --- | --- | --- |")
    print(row_play("play.fps_median", "FPS (median)"))
    print(row_play("play.fps_p1", "FPS (p1 — worst 1%)"))
    print(row_play("play.cpu_median", "CPU% (median)"))
    print(row_play("play.cpu_p95", "CPU% (p95)"))
    print(row_play("play.rss_median", "RSS MB (median)"))
    print(row_play("play.rss_max", "RSS MB (max)"))
    print()

    # Phase timings
    print(f"### Phase timings")
    print(f"| Metrics | {label_before} | {label_after} | Δ(abs/%) |")
    print(f"| --- | --- | --- | --- |")
    phase_keys = sorted([k for k in set(cond_before["metrics"]) | set(cond_after["metrics"])
                         if k.startswith("phase.")])
    for k in phase_keys:
        if k.endswith("init_ms") or "reset_ms_S" in k or "gameover_ms_S" in k:
            d = deltas.get(k)
            b = cond_before["metrics"].get(k)
            a = cond_after["metrics"].get(k)
            lab = k.split(".", 1)[1]
            def s(agg):
                return "-" if not agg else f"{agg['median']:.3f} [{agg['iqr_low']:.3f}–{agg['iqr_high']:.3f}]"
            if d is None:
                delta_s = "-"
            else:
                da = d["delta_abs"]; dp = d["delta_pct"]
                delta_s = "-" if da is None else (f"{da:+.3f} ({dp:+.1f}%)" if dp is not None else f"{da:+.3f} (n/a)")
            print(f"| {lab} | {s(b)} | {s(a)} | {delta_s} |")
    print()

    # Notes about non-common
    if extras_before or extras_after:
        print("> **Note:** Some metrics exist only in one condition:")
        if extras_before:
            print(f"> - Only in **{label_before}**: {', '.join(extras_before)}")
        if extras_after:
            print(f"> - Only in **{label_after}**: {', '.join(extras_after)}")
        print()


def _expand_globs(patterns):
    out = []
    if isinstance(patterns, (list, tuple)):
        pats = patterns
    else:
        pats = [patterns]
    for pat in pats:
        out.extend(sorted(glob.glob(pat)))
    return out


def main():
    ap = argparse.ArgumentParser(description="Summarize perf CSVs (single condition or compare two).")
    # Mode A: single condition (label + many csvs)
    ap.add_argument("--label", help="Condition label, e.g. 'Windows • Before'.")
    ap.add_argument("--drop-outliers", type=float, default=0.0,
                    help="Drop top/bottom p%% per-run when aggregating medians (default 0).")
    ap.add_argument("--format", choices=["text", "md"], default="text",
                    help="Output format.")
    ap.add_argument("--quiet-per-run", action="store_true",
                    help="Hide per-run quick lines in single-condition mode.")
    # Mode B: compare two conditions
    ap.add_argument("--compare", action="append",
                    help='Two entries of the form "Label:glob_pattern". Example: '
                         '--compare "Before:logs/perf_before_*.csv" --compare "After:logs/perf_after_*.csv"')

    # Positional CSVs (single mode)
    ap.add_argument("csv", nargs="*", help="CSV files or globs (single-condition mode).")
    args = ap.parse_args()

    if args.compare:
        if len(args.compare) != 2:
            raise SystemExit("Provide exactly two --compare entries (Before and After).")
        specs = []
        for spec in args.compare:
            if ":" not in spec:
                raise SystemExit(f"--compare needs 'Label:pattern' format: {spec}")
            label, pat = spec.split(":", 1)
            files = _expand_globs(pat.strip())
            if not files:
                raise SystemExit(f"No files match pattern for {label!r}: {pat}")
            runs = [summarize_run(p) for p in files]
            cond = aggregate_runs(runs, args.drop_outliers)
            specs.append((label.strip(), runs, cond))

        (label_b, runs_b, cond_b), (label_a, runs_a, cond_a) = specs
        deltas, extras_b, extras_a = compare_conditions(cond_b, cond_a)

        if args.format == "text":
            # Show each condition summary in text, then a compact MD compare table
            render_text_single(label_b, runs_b, cond_b, quiet=True)
            render_text_single(label_a, runs_a, cond_a, quiet=True)
            print("== Comparison (Markdown table) ==\n")
            render_md_compare(label_b, cond_b, label_a, cond_a, deltas, extras_b, extras_a)
        else:
            # Directly emit markdown tables
            render_md_compare(label_b, cond_b, label_a, cond_a, deltas, extras_b, extras_a)

        return

    # Single-condition mode
    if not args.label:
        raise SystemExit("Single-condition mode requires --label.")
    files = []
    for item in (args.csv or []):
        files.extend(_expand_globs(item))
    if not files:
        raise SystemExit("Provide one or more CSV files (or globs).")

    runs = [summarize_run(p) for p in files]
    cond = aggregate_runs(runs, args.drop_outliers)

    if args.format == "text":
        render_text_single(args.label, runs, cond, quiet=args.quiet_per_run)
    else:
        # produce markdown tables similar to the text one (single column)
        # Reuse text renderer for content; in future, add a full MD single-column table if needed.
        render_text_single(args.label, runs, cond, quiet=args.quiet_per_run)


if __name__ == "__main__":
    main()
