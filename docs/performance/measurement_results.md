
# Measurement Results

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

- Each result contains medium and IQR (Inter-Quartile range) including Q1–Q3 of the 5 run values.
 
### Steady-state (play phase only)
| Metrics | Before updates on Windows | After updates on Windows | Δ(abs/%) | Before updates on Mac | After updates on Mac | Δ(abs/%) |
| --- | --- | --- | --- | --- | --- | --- |
| FPS (median) | 29.830 [29.825–29.850] | | | 29.426 |
| FPS (p1 — worst 1%) | 27.187 [26.790–27.751] | | | 24.179 | 
| CPU% (median) | 3.000 [3.000–3.100] | | | 12.200 | 
| CPU% (p95) | 6.200 [6.200–6.200] | | | 14.100 |  
| RSS MB (median) | 58.622 [58.548–58.651] | | | 163.545 |
| RSS MB (max) | 60.555 [60.535–60.559] | | | 166.068 |
 

### Phase timings
| Metrics | Before updates on Windows | After updates on Windows | Δ(abs/%) | Before updates on Mac | After updates on Mac | Δ(abs/%) |
| --- | --- | --- | --- | --- | --- | --- |
| init_ms | 43.350 [43.163–45.285] | | | 33.574 |
| reset_ms (S1) |0.101 [0.097–0.105] | | | 0.273 |
| reset_ms (S2) | 0.099 [0.064–0.099] | | | 0.154 |
| gameover_ms (S3) | 26.618 [23.976–26.653] | | | 17.369 |

