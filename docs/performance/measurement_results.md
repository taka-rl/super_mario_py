
# Measurement Results

## Measurement Conditions

### Scenarios for the measurements
Please refer to [this documents](https://www.xxxx/docs/performance/measurement_scenarios.md)


### Environments
- Power: Not plugged in. 
- FPS is 30 (Default value).

| OS | Python version  | RAM | CPU |
|---------|----------- | --- | --- |
| Windows 10 | Python 3.10.11 | 16GB | 11th Intel Core i-7 - 1165G7 | 
| Macbook Air M2 | Python 3.10.11 | 16GB | M2 |

### Code optimaization


## How to run
Run the following commands: 

```cmd
# Editable install (first time)
pip install -e .

# Perf run (logs to CSV)
mario-perf --fps 30 --perf-csv logs/perf_<label>.csv
# Example labels: before_win, before_mac, after_win, after_mac

# CSV to Plot
perf-plot logs/perf_<label>.csv --out logs/plot_<label>.png

# Compare results


```

## Result list

| Metrics | Before updates on Windows | After updates on Windows | Before updates on Mac | After updates on Mac |
| --- | --- | --- | --- | --- |
| FPS
| Mean CPU%
| Mean RSS
| init_ms
| reset_ms (S1)
| reset_ms (S2)
| gameover_ms (S3)

## Compare results 
### Windows
| Metrics | Differences |
|---------|-----------|
| Mean CPU%
| Mean RSS
| init_ms
| reset_ms (S1)
| reset_ms (S2)
| gameover_ms (S3)

### Mac
| Metrics | Differences |
|---------|-----------|
| Mean CPU%
| Mean RSS
| init_ms
| reset_ms (S1)
| reset_ms (S2)
| gameover_ms (S3)

