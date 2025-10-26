
# Measurement Results

## Overview of the results
- Init got a bit slower on both Windows and Mac (small absolute cost) — expected because more work happens once at startup (class-level images() + cache warmup).
- Game over/reset paths are much faster on both OSes (big win), especially **gameover_ms (−64% Win, −48% Mac)**.
  > The cache shifts work from resets/death to startup—higher `init_ms` but much faster `gameover_ms` and stable/lower RSS during play.
- Steady-state memory (RSS) improved on both OSes (modest but consistent drops in median and max).
- Steady-state CPU: essentially flat on **Windows (3.0 → 3.1%** median; I’d treat as noise), meaningfully lower on **Mac (median −9%, p95 −14%)**.

## Measurement Conditions
### Scenarios for the measurements
Please refer to [this document](https://www.xxxx/docs/performance/measurement_scenarios.md)

### Environments
| Conditions | Windows 10  | Macbook Air M2 |
|---------|----------- |----------- |
| Power state | plugged in | plugged in |
| Background | only VS code and Pygame window | only VS code and Pygame window |
| FPS | 30 | 30 |

### Libraries
| Libraries | Version  |
|---------|----------- |
| pygame | 2.6.1 |
| numpy | 2.2.6 |
| psutil | 7.1.0 |
| Matplotlib | 3.10 |

### Hardware
| OS | Python version  | RAM | CPU |
|---------|----------- | --- | --- |
| Windows 10 | Python 3.10.11 | 16GB | 11th Intel Core i-7 - 1165G7 | 
| MacBook Air M2 | Python 3.10.11 | 16GB | M2 |

### Code Optimization

1. Introduced a class-level image cache (assets.get_images) so entities reuse the same master Surface objects across instances.  
Each entity now keeps references to shared, immutable “master” surfaces. When per-instance alpha/transforms are needed we copy (surf.copy()) to avoid mutating the shared surface.

2. Replaced unnecessary pygame.Rect() with rect.topleft, rect.update()

- Benchmark for pygame.Rect() vs rect.update(x,y,w,h) and rect.topleft = (x,y):  
update() in Mario class in Windows 10  
Result:
per call on Windows 10(Mario update()): 0.00360 ms saved (pygame.Rect time - update time = 0.00879 - 0.00519 = 0.00360 ms)  
Example total:   
1 episode: 0.00360 ms * 1 entity(Mario) * 3000 times = ~10.8 ms 
1K episodes: 10.8 ms * 1K = 10800 ms = ~10.8 s  
100K episodes: 10.8 ms * 100K = 1080000 ms = 1080 s = ~0.3 h
1M episodes: 10.8 ms * 1M = 10800000 ms = 10800 s = ~3.0 h
  - Which one should be used: 
    - rect.topleft = (x, y) – fastest when size doesn’t change.
    - rect.update(x, y, w, h) – fastest when position and size change.

```bash
t0 = time.perf_counter()
self.rect = pygame.Rect(self.__map.get_drawx(self.__rawrect), self.__rawrect.y, self.__rawrect.width, self.__rawrect.height)
used_rect = (time.perf_counter() - t0) * 1000.0

t2 = time.perf_counter()
self.rect.update(self.__map.get_drawx(self.__rawrect), self.__rawrect.y, self.__rawrect.width, self.__rawrect.height)
update_rect = (time.perf_counter() - t2) * 1000.0

t3 = time.perf_counter()
self.rect.topleft = (self.__map.get_drawx(self.__rawrect), self.__rawrect.y)
topleft_rect = (time.perf_counter() - t3) * 1000.0

print(f"pygame.Rect time: {used_rect} ms, update time: {update_rect} ms, topleft time: {topleft_rect} ms") 

pygame.Rect time: 0.008799999704933725 ms, update time: 0.005199999577598646 ms, topleft time: 0.0037999998312443495 ms

```

## How to run
Run the following commands: 

```bash
# Editable install (first time)
pip install -e .

# Perf run (logs to CSV)
mario-perf --fps 30 --perf-csv logs/perf_<label>.csv

# CSV to Plot
perf-plot logs/perf_<label>.csv --out logs/plot_<label>.png

# Print data from perf_<label>.csv
perf-summarize --label "Win • Before" logs/perf_before_win*.csv --format md
perf-summarize --label "Win • After" logs/perf_after_win*.csv --format md
perf-summarize --label "Mac • Before" logs/perf_before_mac*.csv --format md
perf-summarize --label "Mac • After" logs/perf_after_mac*.csv --format md

# Compare the results between before and after
perf-summarize --compare "Win・Before:logs/perf_before_win*.csv" --compare "Win・After:logs/perf_after_win*.csv" --format md
perf-summarize --compare "Mac・Before:logs/perf_before_mac*.csv" --compare "Mac・After:logs/perf_after_mac*.csv" --format md

# Example labels: before_win, before_mac, after_win, after_mac
```

## Result Tables

- What “FPS (p1 — worst 1%)” means:  
Percentile basics: the p1 (1st percentile) is the value that 1% of samples are at or below.
  - FPS (p1 — worst 1%):
Higher is better for FPS. Therefore, the 1st percentile FPS represents the worst 1% of frames-i.e., 
how bad things get during the worst 1% of time. It’s much more robust than the absolute minimum (which can be a single hiccup).
  - CPU% (p95):
The 95th percentile is often used to represent spikes, since higher values are worse for these metrics.
p95 tells you how high the CPU% gets during the worst 5% of the time. 

- Each result contains median and IQR (Inter-Quartile range) including Q1–Q3 of the 5 run values.
 
### Steady-state (play phase only)
| Metrics | Before updates on Windows | After updates on Windows | Δ(abs/%) | Before updates on Mac | After updates on Mac | Δ(abs/%) |
| --- | --- | --- | --- | --- | --- | --- |
| FPS (median) | 29.830 [29.825–29.850] |  29.841 [29.821–29.855] | +0.010 (+0.0%) | 29.407 [29.407–29.424] | 29.431 [29.409–29.449] | +0.023 (+0.1%) |
| FPS (p1 — worst 1%) | 27.187 [26.790–27.751] | 26.949 [26.520–27.030] | **-0.238 (-0.9%)** | 24.992 [24.642–25.056] | 24.601 [24.527–24.943] | **-0.391 (-1.6%)** | 
| CPU% (median) | 3.000 [3.000–3.100] | 3.100 [3.000–3.100] | +0.100 (+3.3%) | 13.200 [12.100–13.700] | 12.000 [11.650–12.100] | **-1.200 (-9.1%)** |
| CPU% (p95) | 6.200 [6.200–6.200] | 6.200 [6.200–6.200] | +0.000 (+0.0%) |15.500 [13.700–15.500] | 13.300 [13.200–13.800] | **-2.200 (-14.2%)** |  
| RSS MB (median) | 58.622 [58.548–58.651] | 58.376 [58.360–58.438] | **-0.246 (-0.4%)** | 161.841 [161.645–162.111] | 161.202 [156.828–161.513] | **-0.639 (-0.4%)** |
| RSS MB (max) | 60.555 [60.535–60.559] | 60.178 [60.170–60.285] | **-0.377 (-0.6%)** | 164.282 [163.676–164.413] | 163.414 [160.104–163.594] | **-0.868 (-0.5%)** |
 

### Phase timings
| Metrics | Before updates on Windows | After updates on Windows | Δ(abs/%) | Before updates on Mac | After updates on Mac | Δ(abs/%) |
| --- | --- | --- | --- | --- | --- | --- |
| init_ms | 43.350 [43.163–45.285] | 50.120 [49.657–52.977] | +6.769 (+15.6%) | 20.188 [19.258–20.571] | 22.095 [21.899–22.172] | +1.907 (+9.4%) |
| reset_ms (S1) |0.101 [0.097–0.105] | 0.113 [0.101–0.119] | +0.012 (+11.5%) | 0.204 [0.196–0.225] | 0.157 [0.148–0.161] | **-0.046 (-22.8%)** |
| reset_ms (S2) | 0.099 [0.064–0.099] | 0.101 [0.098–0.102] | +0.003 (+2.6%) | 0.162 [0.149–0.164] | 0.096 [0.092–0.115] | **-0.066 (-40.6%)** |
| gameover_ms (S3) | 26.618 [23.976–26.653] | 9.616 [9.205–10.364] | **-17.001 (-63.9%)** | 21.676 [20.865–23.141] | 11.252 [10.220–11.304] | **-10.423 (-48.1%)** |


### Asset cache
| Metrics | Windows 10 Cache count | Windows 10 Cache MB | Mac Cache count | Mac Cache MB |
| --- | --- | --- | --- | --- | 
| after_init | 35.000 [35.000–35.000] | 0.051 [0.051–0.051] | 35.000 [35.000–35.000] | 0.051 [0.051–0.051] |
| after_S1_reset | 41.000 [41.000–41.000] | 0.058 [0.058–0.058] | 41.000 [41.000–41.000] | 0.058 [0.058–0.058] |
| after_S2_reset | 41.000 [41.000–41.000] | 0.058 [0.058–0.058] | 41.000 [41.000–41.000] | 0.058 [0.058–0.058] |
| after_S3_gameover | 49.000 [48.000–49.000] | 0.065 [0.065–0.065] | 48.000 [48.000–49.000] | 0.065 [0.065–0.065] |

> **Note:** Some metrics exist only in one condition:
> - Only in **Win・After**, **Mac・After**: cache.after_S1_reset.cache_mb, cache.after_S2_reset.cache_mb, cache.after_S3_gameover.cache_mb
