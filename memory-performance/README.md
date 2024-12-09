## 3.1. Results

The metrics collected are stored in two separate CSV files: [cpu-in-experiment-result.csv](https://github.com/gca-research-group/tee-morello-performance-experiments/blob/main/cpu-performance/inside-tee-execution/cpu_in-experiment-result.csv) for the run inside a compartment. The file [cpu-out-experiment-result.csv](https://github.com/gca-research-group/tee-morello-performance-experiments/blob/main/cpu-performance/outside-tee-exection/cpu-out-experiment-result.csv) collects metrics of the run without compartments. We calculate the average time that it takes to allocate, write, read and free for  each block size of 100 MB, 200 MB, 300 MB, etc.).The results are summarised in Tables 3 and 4.

<div align="center">
<p><em>Table 3: Metrics of runs inside a compartment, including mean and standard deviation.</em></p>

| **Block Size (MB)** | **Allocation Time (ms)** | **Write Time (ms)** | **Read Time (ms)** | **Free Time (ms)** |
|---------------------|--------------------------|---------------------|--------------------|--------------------|
| 100                 | 93 ± 171.27             | 283,239 ± 58.31     | 283,133 ± 28.83    | 89 ± 180.05        |
| 200                 | 98 ± 221.17             | 566,458 ± 82.10     | 566,269 ± 65.02    | 214 ± 397.35       |
| 300                 | 99 ± 295.44             | 849,705 ± 131.43    | 849,396 ± 87.16    | 222 ± 452.92       |
| 400                 | 127 ± 430.92            | 1,132,983 ± 189.58  | 1,132,550 ± 106.44 | 430 ± 788.02       |
| 500                 | 159 ± 599.09            | 1,416,190 ± 189.97  | 1,415,698 ± 123.68 | 217 ± 420.54       |
| 600                 | 151 ± 648.00            | 1,699,454 ± 255.41  | 1,698,795 ± 174.82 | 439 ± 921.59       |
| 700                 | 195 ± 880.05            | 1,982,654 ± 245.07  | 1,981,909 ± 122.70 | 453 ± 979.92       |
| 800                 | 216 ± 1,084.49          | 2,265,901 ± 235.38  | 2,265,075 ± 139.94 | 818 ± 1,513.98     |
| 900                 | 288 ± 1,536.92          | 2,549,115 ± 258.37  | 2,548,205 ± 196.83 | 816 ± 1,579.74     |
| 1000                | 248 ± 1,543.50          | 2,832,372 ± 337.74  | 2,831,332 ± 167.56 | 444 ± 1,003.29     |

</div>


<div align="center">
<p><em>Table 4: Metrics of runs outside a compartment, including mean and standard deviation.</em></p>

| **Block Size (MB)** | **Allocation Time (ms)** | **Write Time (ms)** | **Read Time (ms)** | **Free Time (ms)** |
|---------------------|--------------------------|---------------------|--------------------|--------------------|
| 100                 | 2 ± 4.77                | 282,584 ± 13.86     | 282,581 ± 12.79    | 6 ± 4.52           |
| 200                 | 4 ± 4.19                | 565,164 ± 17.12     | 565,163 ± 18.85    | 10 ± 4.03          |
| 300                 | 4 ± 1.77                | 847,755 ± 21.18     | 847,752 ± 64.89    | 13 ± 3.66          |
| 400                 | 5 ± 3.09                | 1,130,330 ± 21.00   | 1,130,328 ± 28.20  | 14 ± 2.27          |
| 500                 | 5 ± 3.07                | 1,412,907 ± 31.49   | 1,412,903 ± 28.92  | 15 ± 2.37          |
| 600                 | 5 ± 1.56                | 1,695,493 ± 32.97   | 1,695,493 ± 30.19  | 16 ± 1.28          |
| 700                 | 5 ± 1.52                | 1,978,083 ± 52.24   | 1,978,098 ± 79.47  | 17 ± 0.86          |
| 800                 | 5 ± 1.73                | 2,260,662 ± 41.09   | 2,260,660 ± 53.11  | 18 ± 0.62          |
| 900                 | 5 ± 0.54                | 2,543,249 ± 47.19   | 2,543,234 ± 42.16  | 18 ± 0.97          |
| 1000                | 5 ± 0.50                | 2,825,823 ± 47.72   | 2,825,818 ± 41.68  | 18 ± 0.64          |


<p align="center">
  <img src="./figs/performancememOperations.png" alt="Time to execute allocate, write, read and release memory operations" width="100%"/>
</p>
<p align="center"><em>Figure 5: Time to execute allocate, write, read and release memory operations.</em></p>


- **Allocation time:** A comparison of Table 3 against Table 4 reveals that it takes longer to allocate memory blocks inside compartments. For example, the allocation of 100 MB takes 2 ms without a compartment, while it takes 93 ms inside a compartment. Allocation times vary from 2 to 5 ms without a compartment but from 93 to 288 ms inside a compartment. In contrast, the time to allocate memory within a compartment varies significantly from 93 to 288 ms and depends on the size of the block. Times range from 93 ms for 100 MB blocks to 248 ms for 1000 MB blocks. In contrast, the time to allocate memory without compartments is shorter; it ranges from 2 to 5 ms for all block sizes.

- **Write time:** Both tables show a linear increase in write time as the block size increases. However, execution inside a compartment takes longer. The difference becomes more evident when the sizes of the blocks increases.

- **Read time:** The time to execute read operations increases linearly in both executions. However, execution within a compartment takes longer than execution without compartments.

- **Free time:** The metrics in the tables show contrasting performances. Table 3 shows that it takes significantly longer to free memory in executions inside a compartment. The times range from 89 to 818 ms. In contrast, Table 4 shows times that range from 6 to 18 ms in executions without compartments.
