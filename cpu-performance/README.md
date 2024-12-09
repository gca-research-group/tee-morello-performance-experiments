## 4.1. Results

The results collected from the execution inside a compartment are available from [cpu-in-experiment-result.csv](https://github.com/gca-research-group/tee-morello-performance-experiments/blob/main/cpu-performance/inside-tee-execution/cpu_in-experiment-result.csv). Similarly, the results collected from the execution without a compartment are available from [cpu-out-experiment-result.csv](https://github.com/gca-research-group/tee-morello-performance-experiments/blob/main/cpu-performance/outside-tee-exection/cpu-out-experiment-result.csv).

Table 5 compares the average execution times of different operations in both executions.

<div align="center">
<p><em>Table 5: Times to execute CPU operations inside and without a compartment.</em></p>

| Test Type                     | CPU Time (ms) - Normal | CPU Time (ms) - Secure |
|-------------------------------|------------------------|-------------------------|
| Maths (trigon. and exp. func) | 46,759                | 70,780                 |
| Int                           | 922                   | 993                    |
| Float                         | 830                   | 804                    |
| Array                         | 1,407                 | 1,443                  |

</div>


The results show that complex mathematical operations (trigonometric and exponential functions) executed within a compartment took 70,780 ms on average. In contrast, the execution of the same operations without a compartment took only 46,759 ms. This represents a performance cost of approximately 51.33%. However, the execution of arithmetic operations with integers without a compartment takes 922 ms. This figure is similar to the 993 ms that it takes to execute the same operation inside a compartment. The difference is only 7.70%. Unexpectedly, the execution of floating point operations inside a compartment took 804 ms, which is slightly higher than the execution without a compartment, which took 830 ms. The difference is 3.13%. Finally, the execution of array manipulation operations took 1,443 ms inside a compartment. This is not very different from the 1,407 ms that it takes to execute the same operation without a compartment; precisely, the difference is only 2.56%.

As visualised in Fig. 7, these results indicate that there is a noticeable performance cost in the execution of complex math operations inside compartments. However, in the execution of int, float and array operations, the performance is similar with and without compartments; strikingly, the float is is slightly better in the run inside a compartment.

<p align="center">
  <img src="./figs/CPUperformance.png" alt="CPU performance in executions within and without compartments" width="100%"/>
</p>
<p align="center"><em>Figure 7: CPU performance in executions within and without compartments.</em></p>
