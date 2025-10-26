
# Measurement Results

## Measurement Conditions

### Scenarios for the measurements
Please refer to [this document](https://www.xxxx/docs/performance/measurement_scenarios.md)


### Environments
- Power: Not plugged in. 
- FPS is 30 (Default value).
#### Libraries
| Libraries | Version  |
|---------|----------- |
| pygame | 2.6.1 |
| numpy | 2.2.6 |
| psutil | 7.1.0 |
| Matplotlib | 3.10 |

#### Hardware
| OS | Python version  | RAM | CPU |
|---------|----------- | --- | --- |
| Windows 10 | Python 3.10.11 | 16GB | 11th Intel Core i-7 - 1165G7 | 
| MacBook Air M2 | Python 3.10.11 | 16GB | M2 |

### Code optimization


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
perf-summarize logs/perf_<label>.csv

# Compare results

# Example labels: before_win, before_mac, after_win, after_mac
```

## Result Tables

What “FPS (p1 — worst 1%)” means:  
Percentile basics: the p1 (1st percentile) is the value that 1% of samples are at or below.
- FPS (p1 — worst 1%):
Higher is better for FPS. Therefore, the 1st percentile FPS represents the worst 1% of frames-i.e., 
how bad things get during the worst 1% of time. It’s much more robust than the absolute minimum (which can be a single hiccup).
- CPU% (p95):
The 95th percentile is often used to represent spikes, since higher values are worse for these metrics.
p95 tells you how high the CPU% gets during the worst 5% of the time. 

### Measurement csv files
[perf_before_win.csv](https://www.xxxx/logs/perf_before_win.csv)  
[perf_before_win.png](https://www.xxxx/logs/perf_before_win.png)  
[perf_before_mac.csv](https://www.xxxx/logs/perf_before_mac.csv)  
[perf_before_mac.png](https://www.xxxx/logs/perf_before_mac.png)  

 
### Steady-state (play phase only)

| Metrics | Before updates on Windows | After updates on Windows | Δ(abs/%) | Before updates on Mac | After updates on Mac | Δ(abs/%) |
| --- | --- | --- | --- | --- | --- | --- |
| FPS (median) | 29.721 | | | 29.426 |
| FPS (p1 — worst 1%) | 24.353 | | | 24.179 | 
| CPU% (median) | 3.000 | | | 12.200 | 
| CPU% (p95) | 6.200 | | | 14.100 |  
| RSS MB (median) | 57.842 | | | 163.545 |
| RSS MB (max) | 59.965 | | | 166.068 |
| samples (play rows) | 178 | | | 181 |
 

### Phase timings
| Metrics | Before updates on Windows | After updates on Windows | Δ(abs/%) | Before updates on Mac | After updates on Mac | Δ(abs/%) |
| --- | --- | --- | --- | --- | --- | --- |
| init_ms | 112.798 | | | 33.574 |
| reset_ms (S1) | 0.116 | | | 0.273 |
| reset_ms (S2) | 0.111 | | | 0.154 |
| gameover_ms (S3) | 29.971 | | | 17.369 |

