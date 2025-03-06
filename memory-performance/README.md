<h1 style="font-size: 2em;">Evaluation of performance and security strengths of library-based compartments created on Morello Boards</h1>

This repository contains code, metrics collected and 
results that evaluate compartments created using the 
[library-based compartmentalisation tool](https://ctsrd-cheri.github.io/cheribsd-getting-started/features/c18n.html) available on Morello Boards running the 
[cheriBSD 24.5 operating system](https://ctsrd-cheri.github.io/cheribsd-getting-started/print.html).

**Library–based compartmentalisation:** is a programming model 
where each module (for example a dynamic library) of a given
program is executed in a separate and independent trust
domain. 


The [Library-based Compartmentalisation on CHERI](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/documents/LibraryBasedCompartmentalisationOnCHERI_Dapeng2023.pdf)
workshop paper by Dapeng Gao and Robert Watson presented at Plarch2023
discuss the architecture and basic ideas.
As of this writing (Dec 2024) Library–based compartmentalisation
is an ongoing work on the Morello Board where they are being 
implemented on the basis of cheri-capabilities. Issues of
concern are the performance cost that these compartments will 
incur and their security strenghts.

  
The discussion and results reported in this web page try 
to shed some light on these issues. It  evaluates the performance 
costs incurred by the compartments and the strengths of 
the memory isolation that they provide. The report provides links 
to documents and to the Git repositories that store the C and 
Python codes used in the evaluation and the metrics collected. 
The latter are stored in collected in csv files. 
It also includes tabless, plots of the results, a
 discussion of our interpretation and detailed instructions to 
encourage practitioners to repeat our experiments 
and compare their results against ours. 


# 1. Experiments set up

To run the experiments reported in this document, we use
four Morello Boards connected as shown in Figure 1.


*  Three local Morello Boards are physically located in 
   the William Gates building of the Computer Laboratory.
*  A remote Morello Board physically located in Toronto, 
   within the premises of [TODAQ](https://engineering.todaq.net/), 
   a non-funding partner of the [CAMB project](https://www.cl.cam.ac.uk/research/srg/projects/camb/). 


We connect to the remote Morello Board  through 
ssh from  a laptop connected 
to the network of the [Applied Computing Research Group (GCA)](http://gca.unijui.edu.br/) at Unijuí, Brazil. 

<p align="center">
  <img src="figs/experimentsetup_morelloboard.png" alt="Morello Board location" width="600"/>
</p>
<p align="center"><em>Figure 1: Morello boards used in the experiments.</em></p>


Below is the main configuration of the Morello Boards 
and additional parameters, including the CheriBSD online 
commands that can be used to output these configurations 
directly from the Morello Board. 



We specify the hardware and software configurations of 
the Morello Board used in the experiments in Table 1.

<div align="center">
<p><em>Table 1. Morello board configuration parameters used in the experiments and the online cheriBSD commands to output them.</em></p>

| **Component**       | **Specification**                                   | **Command**                                      |
|----------------------|-----------------------------------------------------|-------------------------------------------------|
| Operating System     | CheriBSD 24.5 (FreeBSD 15.0-CURRENT)                | `uname -a`                                      |
| Kernel Version       | FreeBSD 15.0-CURRENT, releng/24.05                  | `uname -v`                                      |
| Board                | Morello System Development Platform                 | `kenv \| grep smbios.system.product`             |
| RAM                  | 17 GB detected (16 GB DDR4, 2933 MT/s, ECC)         | `dmidecode --type memory`                       |
| Storage              | SSD                                                | `camcontrol identify ada0`                      |
| Architecture         | aarch64c (with CHERI support)                       | `sysctl hw.machine_arch`                        |
| Processor Model      | Research Morello SoC r0p0                           | `sysctl hw.model`                               |
| Number of CPUs       | 4                                                   | `sysctl hw.ncpu`                                |
| Compiler             | clang (with Morello support)                        | `clang-morello --version`                       |
| Tool                 | proccontrol (for CHERI compartments)                | `proccontrol -m cheric18n -s enable ./binary`   |
| Python               | Python 3 (required for Experiments 1, 5, and 6)     | `python3 --version`                             |
| Scripts used         | `cheri-cap-experiment.py`<br>`cpu-in-experiment.c`<br>`memory-in-experiment.c`<br>`pipe-in-experiment.c`<br>`pipe-trampoline-in-experiment.c`<br>`library_a.c`<br>`library_b.c`<br>`memory_reader.py`<br>`integration_process.c` | Not applicable                                  |
| Access               | Remote via SSH                                      | `ssh -i private_key user@server`               |

</div>


As shown in the csv files available in this repository,
we computed our statistical estimations (means, media, etc.)  
and plotted results from metrics produced from 100
trails; we repeted the execution of each operation, 
such as malloc, 100 times.
The choice of 100 repetitions is based in on own
experience in performance analysis.

<!-- on the Central Limit Theorem, which suggests          -->
<!-- that a sample size of 30 is often adequate to yield   -->
<!-- a statistically meaningful average                    -->
<!-- [Statistics How To 2023](https://www.statisticshowto. -->
<!-- com/probability-and-statistics/normal-distributions/  -->
<!-- central-limit-theorem-definition-examples/).          -->



# 2 Compilation and Execution


The inclusion of library-based compartments is determined 
at compilation and execution time. It is documented in:

- [CHERI Software Compartmentalization](https://www.cl.cam.ac.uk/research/security/ctsrd/cheri/cheri-compartmentalization.html), Robert Watson, 2019.
- [Cheripedia wiki](https://github.com/CTSRD-CHERI/cheripedia/wiki/Library-based-%20Compartmentalisation), Cheri team, 2022.
- [Userlevel software compartmentalization (experimental)](https://ctsrd-cheri.github.io/cheribsd-getting-started/features/c18n.html), Cheri team, 2024.
- [compartmentalization, c18n — library-based software compartmentalization](https://man.cheribsd.org/cgi-bin/man.cgi/c18n), Dapeng Gao 2024.
- [Library-based Compartmentalisation on CHERI](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/documents/LibraryBasedCompartmentalisationOnCHERI_Dapeng2023.pdf), 
  Dapeng Gao and Robert Watson, Plarch2023.
- Dapeng's [video-presentation](https://www.youtube.com/watch?v=0Zk0NzfiQJA) 
  of 2023, provides a summary of the architecture.


As explained in [User level process environments](https://ctsrd-cheri.github.io/cheribsd-getting-started/features/processes.html), in CheriBSD 24.05, a user  can compile his program to run in three 
different userspace execution environments: 


-  hybrid process: ?? 
-  CheriABI processes: use -mabi=purecap 
-  Benchmark ABI processes: use -mabi=purecap-benchmark


The example of the [compilation of helloworld.c](https://ctsrd-cheri.github.io/cheribsd-getting-started/helloworld/index.html) might be helpful.


The *root# file* command can be used to verify the ABI
targeted by the compiler.


Programs to be run in library-based compartments can
be compiled either with -mabi=purecap or -mabi=purecap-benchmark.
However, for performance evaluation,
the latter alternative is recommended.  
See [compartmentalization, c18n — library-based software compartmentalization](https://man.cheribsd.org/cgi-bin/man.cgi/c18n), Dapeng Gao 2024.  
In our experiments, we have collected metrics
from both alternatives for comparison.




## 2.1 Compilation and Execution Without Library-based Compartments

The normal compilation (without the inclusion of 
library-based compartments) is demonstrated in the 
following example:

```bash
$ clang-morello -o hello hello.c
```

To execute `helloworld`, the programmer can type:

```bash
$ ./helloworld
```

## 2.2 Compilation and Execution with Library-Based Compartments

### 2.2.1  Compilation for purecap ABI

The following command demonstrates the compilation flags 
required to enable library-based compartments:

```bash
$ clang-morello -march=morello+c64 -mabi=purecap -o helloworld helloworld.c
```

- The `-march=morello+c64` parameter defines the 64-bit 
  Morello architecture.
- The `-mabi=purecap` flag targets the Application Binary 
  Interface (ABI). With this ABI,  all memory references and 
  pointers are implemented as capabilities.

To execute the `helloworld` program within a library-based 
compartment, the programmer can type:

```bash
$ proccontrol -m cheric18n -s enable helloworld
```

The binary is executed within a libraryi-based compartment
that is enabled by the `proccontrol` command.

We follow example shown above in subsequent sections 
in the compilation and execute=ing of the programs used 
in the evaluation.


### 2.2.2  Compilation for purecap purecap-benchmark ABI

The compilation and execution with purecap-benchamark ABI are
similar to the compilation and execution with purecap ABI,
execept for the use of the -mabi=puerecap-benchmark.


```bash
$ clang-morello -march=morello+c64 -mabi=purecap-benchmark -o helloworld helloworld.c
```

```bash
$ proccontrol -m cheric18n -s enable helloworld
```





# 3. Evaluation of the Maximum Number of Library-Based Compartments

The main aim of this experiment is to measure and analyse how the memory of a Morello Board is consumed by instances (also called replicas) of attestables. To this end, we create and attestable and load it with a C program compiled with the library compartmentalisation tool. We use the enterprise application integration (see yellow box) use case implemented in - [tee-compartimentalisation-study-case](https://github.com/gca-research-group/tee-compartimentalisation-study-case) repository.

The parameter to measure is the number of attestables that can be created on a Morello Board before consuming 90% of its memory. In addition to the number of attestables, we took the opportunity to collect metrics about the time it takes the operating system to wipe the memory used by the attestable. The setup of the experiment is shown in Fig. 2.

<p align="center">
  <img src="./figs/maxnumberofatts.png" alt="Max number of attestable that can be created before exhausting memory" width="55%"/>
</p>
<p align="center"><em>Figure 2: Max number of attestables that can be created before exhausting memory.</em></p>

Imagine that user Alice is conducting the experiment. To create the attestables and collect the metrics, Alice executes the following steps:

1. **Initiation**: Alice initiates `cheri-cap-experiment.py` on a Morello Board.

2. **Launch**: Alice executes `cheri-cap-experiment.py` to launch the attestable:

   [% cheri-cap-experiment.py](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/max_num_of_compartments_performance/purecapABI_cheriOS_22.12/cheri-cap-experiment.py)

3. `% python3 cheri-cap-experiment.py` runs incrementally, creating attestable replicas until it detects that the attestables have consumed 90% of the 17118.4 MB of the Morello Board's memory, that is, about 15406.5 MB.


## 3.1. Results 

We have stored the metrics collected in scv files. To help the reader, 
the first lines of the csv files are shown in tables to be read as follows:


- **Number of Compartments:** The number of compartments created.
- **Memory Used (MB):** The amount of memory consumed by the compartments.
- **Time Elapsed:** The time elapsed from the start to completion 
    of the experiment which is assumed to start at time zero. 


We assume that the experiments start at time zero, with 0 number 
of compartments which  have consumed zero MB of memory.






### 3.1.1. Compartments created for purecap ABI in cheriOS 22.12 

The results are logged in the csv file [max_num_compart-experiment-results.csv](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/max_num_of_compartments_performance/purecapABI_cheriOS_22.12/max_num_compart-experiment-cheriOS22.12-results.csv), which contains detailed data on the number of compartments, memory usage, and elapsed time.

The first few lines of the csv file are shown in Table 2.


<div align="center">
<p><em>Table 2: Metrics of memory consumed by different numbers of 
compartments created for  purecap ABI cheriOS 22.14 and elapsed time.</em></p>

| **Number of Compartments** | **Memory Used (MB)** | **Time Elapsed (ms)** |
|-----------------------------|----------------------|-----------------------|
| 1                           | 1628.40             | 514.99               |
| 2                           | 1631.00             | 3070.37              |
| 3                           | 1634.03             | 5656.81              |
| 4                           | 1637.11             | 8222.68              |
| 5                           | 1640.39             | 10808.39             |
| ...                         | ...                 | ...                  |
| 8991                        | 13066.42            | 26773287.54          |

</div>


The first row shows that it took 514.00 ms to `cheri-cap-experiment.py` to create one compartment that consumes 1628.40 MB of memory.  
As a second example take the 5th row. It shows that after 10808.39 ms, `cheri-cap-experiment.py` has created 5 compartments that have consumed 1640.39 MB.

The blue line in the plot of Fig. 3 illustrates how memory is consumed 
as the number of compartments increases. 
The gree line indicates how many seconds takes to create 
a given  number of compartments. For example, it takes 10 000 
seconds to created 4 000 compartments,
(about 2 hrs and 46 min) seconds to created 4 000 compartments,
that is, about 2 hrs and 46 min.
 


<p align="center">
  <img src="./figs/max_num_compart_purecapABI_cheri22.12.png" alt="Memory consumed by incremental replication of compartments and time to create compartments" width="100%"/>
</p>
<p align="center"><em>Figure 3: Memory consumed by incremental replication of compartments and time to create compartments in cheriOS ver 22.12.</em></p>

We initially expected memory consumption to increase steadily from 1,628.3 MB, corresponding to a single attestable replica, to 15,406.5 MB (90% of total memory) consumed by N attestable replicas. The objective was to determine the exact value of N.

However, the results revealed unexpected behaviour: memory consumption increased consistently only until approximately 3,800 attestable replicas consumed 14,582.5 MB. After this point, memory consumption began to decrease as the number of attestable replicas continued to rise. The final data point shows that 8,991 attestable replicas consumed 13,066.4 MB, or roughly 76% of the total memory.

We did not expect the behaviours exhibited by the 
blue line of Fig. 3. We have no sound explanation for it. 
These preliminary results highlight an area for further 
exploration. Additionally, the analysis of the time 
required to wipe the memory of the attestable replicas 
remains pending.



### 3.1.2. Compartments created for purecap ABI in cheriOS 24.05

The results are logged in the csv file [max_num_compart-experiment-purecapABI-results.csv](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/max_num_of_compartments_performance/purecapABI/max_num_compart-experiment-purecapABI-results.csv), which contains detailed data on the number of compartments, memory usage, and elapsed time.

The first few lines of the csv file are shown 
in Table 3:





<div align="center">
<p><em>Table 3: Metrics of memory consumed by different numbers of
compartments created for  purecap ABI cheroOS 24.05 and elapsed time.</em></p>

| **Number of Compartments** | **Memory Used (MB)** | **Time Elapsed (ms)** |
|-----------------------------|---------------------|-----------------------|
| 1                           | 1393.11             | 522.23               |
| 2                           | 1399.96             | 1039.24              |
| 3                           | 1404.45             | 1549.57              |
| 4                           | 1411.93             | 2071.49              |
| 5                           | 1421.18             | 2595.50              |
| ...                         | ...                 | ...                  |
| 586                         | 14728.59            | 300644.67            |

</div>




<p align="center">
  <img src="./figs/max_num_compart_purecapABI.png" alt="Memory consumed by incremental replication of compartments and time to create compartments" width="100%"/>
</p>
<p align="center"><em>Figure 4: Max number of compartments created for purecap ABI created in cheriOS ver 24.05 and memory consumed.</em></p>




### 3.1.3. Compartments created for purecap-benchmark in cheriOS 24.05


The results are logged in the csv file [max_num_compart-experiment-purecap-benchmarkABI-results.csv](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/max_num_of_compartments_performance/purecap-benchmarkABI/max_num_compart-experiment-purecap-benchmarkABI-results.csv), which contains detailed data on the number of compartments, memory usage, and elapsed time.

The first few lines of the csv file are shown 
in Table 4:

<div align="center">
<p><em>Table 4: Metrics of memory consumed by different numbers of
compartments created for  purecap-benchmark ABI cheriOS 24.05 and elapsed time.</em></p>

| **Number of Compartments** | **Memory Used (MB)** | **Time Elapsed (ms)** |
|-----------------------------|---------------------|-----------------------|
| 1                           | 1353.46             | 505.44                |
| 2                           | 1357.30             | 1011.36               |
| 3                           | 1360.80             | 1517.21               |
| 4                           | 1364.79             | 2023.95               |
| 5                           | 1368.99             | 2560.19               |
| ...                         | ...                 | ...                   |
| 615                         | 14691.81            | 315171.82             |

</div>



<p align="center">
  <img src="./figs/max_num_compart_purecap-benchmarkABI.png" alt="Memory consumed by incremental replication of compartments and time to create compartments" width="100%"/>
</p>
<p align="center"><em>Figure 5: Max number of compartments created for purecap--benchmark ABI created in cheriOS ver 24.05 and memory consumed.</em></p>

 




# 4. Memory performance in the execution of allocate, release, read and write Operations

In this experiment, we use the code shown in Algorithm 1. It 
executes a list of operations on large blocks
and measaures the time as indicated  on the
right side. 

a) **malloc:**  time taken to allocate the block of memory.  
b) **write:**    time taken to write data to fill the entire memory block.  
c) **read:**     time taken to read the data from the entire memory block.  
d) **free:**     time taken to release the memory block.

As shown in Figure 6, we use blocks of `100, 200, 300,...,100 000 MB`. 
Blocks of these sizes are typical of applications that process 
images and access databases.

<p align="center">
  <img src="./figs/mem_blocks_num_trials.png" alt="Performance of memory operations on memory blocks of different sizes" width="65%"/>
</p>
<p align="center"><em>Figure 6: Number of repetitions of each memory
operation of memory blocks of different sizes.</em></p>


<pre style="border: 1px solid #ddd; padding: 10px; background-color: #f9f9f9; font-family: monospace;">
Algorithm 1: Execution of memory operations and metric collections from their executions.

1. perform_tests(log_file, total_time)
2. begin
3.     foreach block_size in MIN_BLOCK_SIZE to MAX_BLOCK_SIZE step BLOCK_STEP do
4.         foreach test_num from 1 to NUM_TESTS do
5.             allocation_time = time(malloc(block_size))
6.             write_time = time(write_to_memory(block, block_size))
7.             read_time = time(read_from_memory(block, block_size))
8.             free_time = time(free(block))
9.             log(log_file, block_size, test_num, allocation_time, write_time, read_time, free_time)
10.        endfor
11.    endfor
12. end
</pre>


The execution begins with the `perform_tests` function 
(line 1), which ias input receives the name of an svc file to
to store performance metrics, including the total time 
taken to run the tests. The for-loop (line 3) iterates over 
memory blocks of different sizes ranging from `MIN_BLOCK_SIZE` 
to `MAX_BLOCK_SIZE` with increments specified by `BLOCK_STEP`. 
The inner for-loop (line 4) repeats the test `NUM_TESTS` times 
for each block size. `NUM_TESTS` is defined by the programmer 
as a constant.

At each iteration, the memory allocation time is measured 
by the time function (line 5); the time to write to the block 
is measured in line 6, the time to read the block is measured 
in line and, finally, the time to free the memory is measured 
in line 8. The metric collected  are recorded in the log 
file along with the test number (line 9).


To collect metrics, we use a C program compiled and 
executed without compartments and within compartments:


## 4.1 Compilation and execution without compartments
  

  ```bash

   $ clang-morello -o memory-out-experiment memory-out-experiment.c -lm

   $ ./memory-out-experiment

  ```

We stored the metrics collected in the 
[memory-out-experiment-results.csv](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/memory-performance/outside-tee-execution/memory-out-experiment-results.csv) file.
We calculate the average time that it takes to allocate, write, read and free for  each block size of 100 MB, 200 MB, 300 MB, etc.). The 
results are summarised in Table 5.


<div align="center">
<p><em>Table 5: Metrics of runs outside a compartment, including mean and standard deviation.</em></p>


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

</div>

</div>





## 4.2 Compilation and execution withing compartments created to run in purecap ABI

  ```bash
  $ clang-morello -march=morello+c64 -mabi=purecap -o memory-in-experiment-purecap memory-in-experiment-purecap.c -lm
  
  $ proccontrol -m cheric18n -s enable memory-in-experiment-purecap
  ```

The metrics collected are stored in two separate csv files: [memory-in-experiment-purecap-results.csv](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/memory-performance/inside-tee-execution-purecap/memory-in-experiment-purecap-results.csv) for the run inside a compartment. 
We calculate the average time that it takes to allocate, write, 
read and free for  each block size of 100 MB, 200 MB, 300 MB, 
etc.). The results are summarised in Tables 6.


  
<div align="center">
<p><em>Table 6: Metrics of runs inside compartment created for the
purecap ABI, including mean and standard deviation (todo: allocation 
time col looks odd!).</em></p>


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




## 4.3 Compilation and execution withing compartments created to run in purecap-benchmark ABI
 
 
  ```bash
  $ clang-morello -march=morello+c64 -mabi=benchmark -o memory-in-experiment-purecap-benchmark memory-in-experiment-purecap-benchmark.c -lm
  
  $ proccontrol -m cheric18n -s enable memory-in-experiment-purecap-benchmark
  ```

The metrics collected are stored in two separate CSV files: [memory-in-experiment-purecap-benchmark-results.csv](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/memory-performance/inside-tee-execution-purecap-benchmark/memory-in-experiment-purecap-benchmark-results.csv) for the run inside a compartment. 
We calculate the average time that it takes to allocate, write, 
read and free for  each block size of 100 MB, 200 MB, 300 MB, 
etc.). The results are summarised in Table 7.

  
<div align="center">
<p><em>Table 7: Metrics of runs inside a compartment compiled for the
bechmark ABI, including mean and standard deviation (todo: allocation 
time col looks odd!).</em></p>

| **Block Size (MB)** | **Allocation Time (ms)** | **Write Time (ms)** | **Read Time (ms)** | **Free Time (ms)** |
|---------------------|--------------------------|---------------------|--------------------|--------------------|
| 100                 | 81 ± 158.99             | 40,369 ± 4.84       | 80,737 ± 7.56      | 86 ± 178.33        |
| 200                 | 92 ± 219.79             | 80,737 ± 6.36       | 161,472 ± 10.22    | 210 ± 395.51       |
| 300                 | 94 ± 295.34             | 121,105 ± 7.88      | 242,209 ± 12.70    | 219 ± 452.59       |
| 400                 | 122 ± 430.07            | 161,472 ± 8.04      | 322,946 ± 17.29    | 425 ± 783.85       |
| 500                 | 153 ± 596.27            | 201,842 ± 11.20     | 403,681 ± 14.85    | 215 ± 417.51       |
| 600                 | 146 ± 646.07            | 242,210 ± 12.87     | 484,417 ± 17.45    | 436 ± 917.23       |
| 700                 | 191 ± 879.02            | 282,579 ± 13.21     | 565,154 ± 18.71    | 453 ± 987.35       |
| 800                 | 213 ± 1,088.59          | 322,947 ± 14.35     | 645,893 ± 17.43    | 822 ± 1,529.08     |
| 900                 | 283 ± 1,535.56          | 363,315 ± 14.68     | 726,626 ± 17.13    | 818 ± 1,587.88     |
| 1000                | 246 ± 1,538.68          | 403,685 ± 15.61     | 807,368 ± 18.86    | 443 ± 1,004.74     |

</div>






## 4.4. Comparion of results



Plots of the results from Tables 5, 6 and 7 are shown in Figure and 7.  

<p align="center">
  <img src="./figs/perfor_mem_oper_compare.png" alt="Time to execute allocate, write, read and release memory operations" width="100%"/>
</p>
<p align="center"><em>Figure 7: Comparison of time to execute allocate, write, read 
   and release memory operations: no copartment, compartment for purecap and benchmark ABI.</em></p>


- **Allocation time (to update!):** A comparison of Table 1 against Table 2 reveals that it takes longer to allocate memory blocks inside compartments. For example, the allocation of 100 MB takes 2 ms without a compartment, while it takes 106 ms inside a compartment. Allocation times vary from 1 to 3 ms without a compartment but from 106 to 265 ms inside a compartment. In contrast, the time to allocate memory within  a compartment varies significantly from 106 to 265 and depends on the size of the block. Times range from 106 ms for 100 MB blocks to 251 ms for 700 MB blocks. In contrast, the time to allocate memory without compartments is shorter, it ranges from 2 to 7 ms for all block sizes.

- **Write time (to update) :** Both tables show a linear increase in write time as the block size increases. However, execution inside a compartment takes longer. The difference becomes more evident when the sizes of the blocks increases.

- **Read time (to update):** The time to execute read operations increases linearly in both executions. However, execution within a compartment takes longer than execution without compartments.

- **Free time (to update):** The metrics in the tables show contrasting performances. 
    Table 5 shows that it takes significantly longer to free memory in executions 
    inside a compartment. The times rages from 97 to 1 197 ms. In contrast, 
    Table 5 shows times that range from 3 to 9 ms in executions without compartments.



A boxplot is shown in Figure 8.

<p align="center">
  <img src="./figs/boxplot_perfor_mem_oper_compare.png" alt="Dispersion of the time to execute allocate, write, read, and free operations" width="100%"/>
</p>
<p align="center"><em>Figure 8: Comparison of dispersion of the time to execute 
   allocate, write, read, and free operations: no copartment, compartment for purecap 
   and benchmark ABI.</em></p>

 

 
 

#  5.  CPU performance in the execution of demanding arithmetic operations

We have carried out this experiment to determine if library--based compartments affect the performance of the CPU. Precisely, we have executed a program with functions that involve the execution of CPU--demanding arithmetic operations and collected metrics about execution time. The program that we have implemented for this purpose includes operations with integers (int), floating point (float), arrays, and complex mathematical functions (such as trigonometric and exponential functions) that are known to be CPU--demanding.


The choice of these operations is based on the variety of typical workloads in computer applications, covering operations that vary in CPU resource usage. Time collection was carried out in both environments, allowing a detailed comparison between performance in the compartmentalised environment and the Morello Board's normal operating environment.

Algorithm 2 contains the C code that we have run to produce metrics about the CPU performance and store them in a csv files.

<pre style="border: 1px solid #ddd; padding: 10px; background-color: #f9f9f9; font-family: monospace;">
Algorithm 2: CPUPerformance

1. perform_tests(log_file, total_time)
2. begin
3.     for test_num in NUM_TESTS do
4.         start_time = capture_time()
5.         execute_operations(WORKLOAD_SIZE)
6.         end_time = capture_time()
7.         cpu_time = calculate_cpu_time(start_time, end_time)
8.         results(log_file, test_num, cpu_time)
9.         total_time += cpu_time
10.    endfor
11. end
</pre>

The execution begins with the perform\_tests function (line 1), which receives the name of as a log file as input parameter to be used to store metrics about the execution of individual operations and the total time to complete the program. The function enters a repeat loop that is repeated the number of times specified by `NUM_TESTS` (line 3), where each iteration represents a test identified by `test_num`. In each iteration, the initial test time is recorded (line 4), followed by the execution of the computational operations determined by `WORKLOAD_SIZE` (line 5). At the end of execution, the final time is recorded (line 6), and the total CPU time elapsed is calculated by subtracting the `start_time` from the `end_time` (line 7). This time is recorded in the log file, along with the test number (line 8), and added to `total_time`, that accumulates the total time spent on all the tests (line 9).





## 5.1 Compilation and execution without a compartment

  We compile and run it as follows:
  ```bash
  $ clang-morello -o cpu-out-experiment cpu-out-experiment.c -lm
  
  $ ./cpu-out-experiment
  ```
 The source of the C program in available from [cpu-out-experiment.c](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/cpu-performance/outside-tee-exection/cpu-out-experiment.c)

The results collected from the execution are available from
from [cpu-out-experiment-results.csv](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/cpu-performance/outside-tee-exection/cpu-out-experiment-results.csv).


## 5.2  Compilation and execution inside a compartment created for the purecap ABI


  We compile and run it as follows:
  ```bash
  $ clang-morello -march=morello+c64 -mabi=purecap -o cpu-in-experiment-purecap cpu-in-experiment-purecap.c -lm
  
  $ proccontrol -m cheric18n -s enable cpu-in-experiment-purecap
  ```


 The source of the C program in available from 
  [cpu-in-experiment-purecap.c](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/cpu-performance/inside-tee-execution-purecap/cpu-in-experiment-purecap.c)

The results collected from the execution are available from 
from [cpu-in-experiment-purecap-results.csv](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/cpu-performance/inside-tee-execution-purecap/cpu-in-experiment-purecap-results.csv). 


## 5.3  Compilation and execution inside a compartment created for the purecap-benchmark ABI


  We compile and run it as follows:
  ```bash
  $ clang-morello -march=morello+c64 -mabi=purecap-benchmark -o cpu-in-experiment-purecap-benchmark cpu-in-experiment-purecap-benchmark.c -lm
  
  $ proccontrol -m cheric18n -s enable cpu-in-experiment-purecap-benchmark
  ```
  The source of the C program in available from 
  [cpu-in-experiment-purecap-benchmark.c](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/cpu-performance/inside-tee-execution-purecap-benchmark/cpu-in-experiment-purecap-benchmark.c)
  
 The results collected from the execution are available from 
from [cpu-in-experiment-purecap-benchmark-results.csv](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/cpu-performance/inside-tee-execution-purecap-benchmark/cpu-in-experiment-purecap-benchmark-results.csv).




## 5.4. Comparison of results from the three experiments

Table 8 shows a comparison of the three alternatives: no compartment,
compartment running purecap code and compartment running
purecap-benchmark code.

<div align="center">
<p><em>Table 8: Times to execute CPU operations inside and without a compartment, including benchmark results.</em></p>

| Trial Type                     | CPU Time (ms) - Normal | CPU Time (ms) –purecap-benchmark | CPU Time (ms) - purecap |
|-------------------------------|------------------------|-------------------------------------|-------------------------|
| Maths (trigon. and exp. func) | 46,759                | 52,901                              | 70,780                 |
| Int                           | 922                   | 670                                 | 993                    |
| Float                         | 830                   | 621                                 | 804                    |
| Array                         | 1,407                 | 101                                 | 1,443                  |

</div>



<p align="center">
  <img src="./figs/CPUperfor_compare_normal_purecap_purecap-benchmark.png" alt="CPU performance in executions within and without compartments" width="100%"/>
</p>
<p align="center"><em>Figure 9: CPU performance in executions: no compartment, compartments
  created for purecap and purecap-benchmark.</em></p>



The results show that complex mathematical operations (trigonometric and exponential functions) executed within a compartment took 52,901 ms on average. In contrast, the execution of the same operations without a compartment took only 46,759 ms. This represents a performance cost of approximately 13.12%. However, the execution of arithmetic operations with integers without a compartment takes 922 ms, compared to 670 ms inside a compartment. The difference is a performance gain of 27.32%. Similarly, the execution of floating point operations inside a compartment took 621 ms, which is lower than the execution without a compartment, which took 830 ms. This represents a performance gain of 25.18%. Finally, the execution of array manipulation operations took 101 ms inside a compartment, which is significantly lower than the 1,407 ms that it takes to execute the same operation without a compartment, representing a performance gain of 92.82%.

As visualized in Figure 9, these results indicate that there is a noticeable performance cost in the execution of complex math operations inside compartments. However, in the execution of int, float, and array operations, the performance is significantly better inside compartments; strikingly, the float operations and array manipulation show substantial performance gains when executed inside a compartment.


# 6. Communication performance over pipes

This experiment was conducted to evaluate how the use of compartments affects the performance of communication over Unix pipes. To collect metrics, we have implemented a C program that communicates a parent with a child process over a pipe and collects metrics about writing to and reading from a pipe that interconnected them. As shown in Figure 10, the parent process writes a message to the pipe and the child process reads it.

<p align="center">
  <img src="./figs/parent-child-pipe.png" alt="Parent-child communication over a pipe"/>
</p>
<p align="center"><em>Figure 10: Parent--child communication over a pipe.</em></p>

We run the C program within a compartment [pipe-in-experiment.c](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/pipe-performance/inside-tee-execution-purecap/pipe-in-experiment.c) and without compartments [pipe-out-experiment.c](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/pipe-performance/outside-tee-execution-purecap/pipe-out-experiment.c).

- **Compilation and execution without a compartment**

  ```bash
  $ clang-morello -o pipe-out-experiment pipe-out-experiment.c
  
  $ ./pipe-out-experiment
  ```

- **Compilation and execution inside a compartment for purecap ABI**

  ```bash
  $ clang-morello -march=morello+c64 -mabi=purecap -o pipe-in-experiment pipe-in-experiment.c
  
  $ proccontrol -m cheric18n -s enable pipe-in-experiment
  ```

- **Compilation and execution inside a compartment for purecap-benchmark ABI**

  ```bash
  $ clang-morello -march=morello+c64 -mabi=purecap-benchmark -o pipe-in-experiment pipe-in-experiment.c
  
  $ proccontrol -m cheric18n -s enable pipe-in-experiment
  ```



To collect metrics, the parent process writes a random string of 1024 bytes — a typical size widely used in inter-process communication applications.

We collected metrics about the following operations:
- **write:** Time taken by the parent process to write data to the pipe.
- **read:** Time taken by the child process to read the data from the other end of the pipe.

As with previous experiments, the code repeats each operation 100 
times to help as estimate means and other statistic parameters.
In our experience, 100 trials produce a realible sample space.


<!--- This is in line with the principles of the Central Limit     -->
<!--- Theorem, which states that a larger sample size helps to     -->
<!--- detect finer fluctuations in latency patterns [Statistics    -->
<!--- How To 2023](https://www.statisticshowto.com/probability-    -->
<!--- and-statistics/normal-distributions/central-limit-theorem-   -->
<!--- definition-examples/).                                       -->

Algorithm 3 describes the execution of the operations and the settings of timers to collect the metrics.


<pre style="border: 1px solid #ddd; padding: 10px; background-color: #f9f9f9; font-family: monospace;">
Algorithm 3: Pipe Communication Performance

1.  start_test(log_file)              
2.  begin
3.      define STRLEN  
4.      define NUM_OF_MSG 
5.      for test_num from 1 to NUM_OF_MSG do
6.          if parent_process
7.              start_timer(write_time)     
8.              write(pipe, message of size STRLEN)        
9.              stop_timer(write_time)      
10.             write(pipe, write_time)     
11.         else 
12.             read(pipe, message of size STRLEN)         
13.             read(pipe, write_time)      
14.             start_timer(read_time)      
15.             stop_timer(read_time)       
16.             log(log_file, test_num, write_time, read_time) 
17.         endif
18.     endfor
19. end
</pre>

In Algorithm 3, the `start_test` function (line 1) initiates a sequence of operations that measure the performance of pipe communication between the parent and child processes. The parameters `STRLEN` and `NUM_OF_MSG` (lines 3 and 4) establish the message size and the number of messages to be sent, respectively. For each iteration, from 1 to `NUM_OF_MSG` (line 5), the parent starts the write timer (line 7), writes a message of size `STRLEN` to the pipe (line 8), stops the write timer (line 9), and then sends the recorded `write_time` back through the pipe (line 10). The child process, in turn, reads the message and the `write_time` from the pipe (lines 12 and 13). To collect the metrics, the child process starts the read timer before reading (line 14) and stops it upon completing the reading (line 15). The test number, along with the write and read times, is logged in the log file (line 16). The procedure is repeated for each iteration until all messages are written to and read from the pipe (line 17).



## 6.1. Results

Table 9, Table 9.1 and Table 10 contain the results of each iteration, including message size, write time, read time, and total time taken for the operations.


The metrics collected from the run of the experiment 
inside a compartment for the purecap ABI are stored
in the [pipe-in-experiment-purecap-results.csv](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/pipe-performance/inside-tee-execution-purecap/pipe-in-experiment-purecap-results.csv) file.


<div align="center">
<p><em>Table 9: Time to execute write and read from a pipe inside a compartment for
                purecap ABI.</em></p>

| Test | Message Size (Bytes) | Write Time (ms) | Read Time (ms) | Total Time (ms) |
|------|-----------------------|-----------------|----------------|-----------------|
| 1    | 1024                 | 0.016           | 0.161          | 0.177           |
| 2    | 1024                 | 0.003           | 0.068          | 0.071           |
| 3    | 1024                 | 0.003           | 0.075          | 0.078           |
| 4    | 1024                 | 0.003           | 0.077          | 0.080           |
| ...  | ...                  | ...             | ...            | ...             |
| 100  | 1024                 | 0.003           | 0.079          | 0.082           |

</div>

 
The metrics collected from the execution of the
experiment inside a compartment
for the purecap-benchmark  ABI are stored in
the [pipe-in-experiment-purecap-benchmark-results.csv](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/pipe-performance/inside-tee-execution-purecap-benchmark/pipe-in-experiment-purecap-benchmark-results.csv) file.



<div align="center">
<p><em>Table 9.1: Time to execute write and read from a pipe inside a compartment for
                purecap-benchmark ABI.</em></p>

| Test | Message Size (Bytes) | Write Time (ms) | Read Time (ms) | Total Time (ms) |
|------|-----------------------|----------------|----------------|-----------------|
| 1    | 1024                 | 0.014           | 0.106          | 0.119           |
| 2    | 1024                 | 0.001           | 0.001          | 0.003           |
| 3    | 1024                 | 0.003           | 0.019          | 0.022           |
| 4    | 1024                 | 0.003           | 0.024          | 0.027           |
| ...  | ...                  | ...             | ...            | ...             |
| 100  | 1024                 | 0.003           | 0.032          | 0.035           |

</div>



The file [pipe-out-experiment-results.csv](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/pipe-performance/outside-tee-execution/pipe-out-experiment-results.csv) 
stores the results of the experiment run
without  the use of a compartment.

<div align="center">
<p><em>Table 10: Time to execute write and read from a pipe without a compartment.</em></p>

| Test | Message Size (Bytes) | Write Time (ms) | Read Time (ms) | Total Time (ms) |
|------|-----------------------|-----------------|----------------|-----------------|
| 1    | 1024                 | 0.013           | 0.059          | 0.072           |
| 2    | 1024                 | 0.001           | 0.001          | 0.003           |
| 3    | 1024                 | 0.001           | 0.001          | 0.002           |
| 4    | 1024                 | 0.001           | 0.001          | 0.002           |
| ...  | ...                  | ...             | ...            | ...             |
| 100  | 1024                 | 0.001           | 0.002          | 0.003           |

</div>


The data shows the differences in the performance of inter--process communication (through pipes) inside a compartment and without compartments.

A graphical view of the results is shown in Figure 10.

<p align="center">
  <img src="./figs/pipe_comm_perfor.png" alt="Times to write and read a 1024 byte string from a pipe executed in compartments and without compartments" width="100%"/>
</p>
<p align="center"><em>Figure 10: Times to write and read a 1024 byte string from a pipe executed in compartments and without compartments.</em></p>

The figure reveals that compartments affect performance. The write operation executed inside compartments consistently shows a higher latency that ranges from 0.016 ms to 0.003 ms. In contrast, the write time outside compartments is notably shorter, closer to 0.001 ms. This discrepancy highlights the additional computational cost introduced by the compartment.

The effect of the compartment on the performance of the read operation is less severe yet, it is visible. The first test shows a read time of 0.161 ms, compared to 0.059 ms in the execution without compartments. As the tests progress, the execution within the compartment consistently exhibits longer read times. This demonstrates that compartmentalisation introduces delays in inter-process communication.

The results suggest the compartments provide significant benefits in terms of security; yet they incur performance costs; the cost might not be negligible in applications that rely on rapid inter--process communication.





# 7. Evaluation of Trust Models in Single-Compartment Environments
We have conducted this experiment to examine the trust model that the Morello Board implements. It is documented that the current release of the Morello Board implements an asymmetric trust model where the Trusted Computing Based (TCB) is trusted by the applications but the TCB does not trust the applications. It is worth mentioning that the current Morello Board does not support the mutual distrust model where the privileged software and the applications distrust each other.

To the TCB of the current Morello Board belong the firmware and privileged software that includes the bootloader, hypervisor and operating system. The library-based compartments that we examine in this report, consider that the linker belongs to the TCB too. See [Library-based Compartmentalisation on CHERI](https://pldi23.sigplan.org/home/plarch-2023) by 
Dapeng and Robert.

In this experiment, we use an application written in C [tee-compartmentalisation-study-case](https://github.com/CAMB-DSbD/tee-compartimentalisation-study-case) and run it within a compartment and without compartments to examine memory isolation. We followed the following steps:

1. **Compilation and execution:**

    We compiled and executed the application integration within a compartment and without a compartments:
    
    - **Compilation and execution within a compartment:**
      
      The application integration is available from Git:  
      [integration-process-in-experiment.c](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/security-single-compartment-performance/inside-tee-execution/integration_process-in-experiment.c)

      We compile and run it as follows:
      ```bash
      $ clang-morello -march=morello+c64 -mabi=purecap -o integration_process-in-experiment integration_process-in-experiment.c -lssl -lcrypto -lpthread
      
      $ proccontrol -m cheric18n -s enable integration_process-in-experiment
      ```

    - **Compilation and execution without a compartment:**

      The application integration is available from Git:  
      [integration-process-out-experiment.c](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/security-single-compartment-performance/outside-tee-execution/integration_process-out-experiment.c)

      We compile and run it as follows:
      ```bash
      $ clang-morello -o integration_process-out-experiment integration_process-out-experiment.c -lssl -lcrypto -lpthread
      
      $ ./integration_process-out-experiment
      ```

2. **Launch python script:** We launched the Python that performs the memory reading.

   ```bash
   $ python3 memory_reader.py
   ```

   The [memory_reader.py](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/mem-reader-python-scripts/memory_reader.py) script cycles through the memory regions of interest reading the data between the start and end addresses of each region directly.

Figure 12 shows the steps executed by the `memory_reader.py` script:

1. The Memory Reader requests the Cheri OS for the PID of the target process by its name, using the method `getPID(processName)`.
2. Cheri OS returns the corresponding PID.
3. The `memory_reader.py` provides the PID to `getMemoryAddresses(PID)` to request a list of the memory regions associated to the process that have read and write (RW) permissions.
4. CheriBSD responds with the mapped memory regions.
5. The `memory_reader.py` starts scraping the memory directly.
6. For each RW region, it fetches the starting address by calling `seek(startAddress)`.
7. Acknowledgement is returned.
8. The `memory_reader.py` executes `read(startAddress to endAddress)` to read the content from the starting address to the end address.
9. The decoded data is returned.
10. This cycle is repeated for all RW regions.
11. The `memory_reader.py` executes `output(dataReadFromMemory)` to record the data read from the memory.

<p align="center">
  <img src="./figs/memory_scraping.png" alt="Procedure to scrap memory regions" width="65%"/>
</p>
<p align="center"><em>Figure 12: Procedure to scrap memory regions.</em></p>



## 7.1. Results

Table 11 summarises the results. The columns have the following meaning:

<div align="center">
<p><em>Table 11: Memory isolation in executions within and without compartments.</em></p>

| Test num. | Execution env.   | User privileges | Access  | Sensitive Data Visible |
|-----------|------------------|-----------------|---------|-------------------------|
| 1         | in Compartment   | Root            | Granted | Yes                     |
| 2         | in Compartment   | Ordinary user   | Denied  | No                      |
| 3         | out Compartment  | Root            | Granted | Yes                     |
| 4         | out Compartment  | Ordinary user   | Denied  | No                      |

</div>


- **Test num:** Unique identification number of the test.
- **Execution env.:** The execution environment where the application is executed, either within a compartments or no compartment.
- **User privileges:** The privileges granted to the user that executes the `memory_reader.py` script.
- **Access:** The response of cheriBSD to the `memory_reader.py` script's request to access the memory region.
- **Sensitive Data Visible:** Visibility of the data retrieved from the memory region. Can the `memory_reader.py` script extract information from the data?

The results shown in Table 10 indicate that a user with root privileges has permission to access any memory region, including memory regions allocated to compartments. However, ordinary users are unable to access memory regions allocated to processes, including processes not executed inside compartments.

These results indicate that the Morello Board implements the traditional asymmetric trust model where user applications trust privileged software. Some applications demand the symmetric trust model where privileged software and user applications distrust each other. Examples of technologies that implement mutual distrust are Intel SGX and AWS Nitro Enclaves.



### Observations runs of the experiment

We observed some unexpected behaviours and crashes of the cheriBSD that demanded reboot to recover. We have no sound explanations, we only suspect that these issues are related to the memory managements in the Morello Board.

- **Process terminated by the OS:**  
  We have observed that the application was terminated (i.e. killed) automatically by the cheriBSD OS, approximately, after 1 hour of execution. See Figure 13. This behaviour seems to be related to the CheriBSD system’s resource management. It seems that the operating system terminates processes that are consuming excessive memory or CPU, possibly in response to an infinite loop or undesirable behaviour. Another speculation is that the CHERI security model abruptly terminates processes that systematically attempt to access protected memory regions, illegally.  

  <p align="center">
    <img src="./figs/abruptkillofproc.png" alt="Abruptly termination of process by the OS" width="75%"/>
  </p>
  <p align="center"><em>Figure 13: Abruptly termination of process by the OS.</em></p>

- **Crash of cheriBSD OS:**  
  We have observed systematic crashes of the cheriBSD OS when the `memory_reader.py` script attempted to read a specific range of memory addresses. As shown in Figure 14, the OS crashed reporting a `Broken pipe` error and the disconnection of the remote SSH shell when the `memory_reader.py` attempted to read addresses in the `0x4a300000` --- `0x4bb00000` range. See Figure 15.  


  <p align="center">
    <img src="./figs/crashoutputbrokenpipe.png" alt="client_loop: send disconnect: Broken pipe" width="75%"/>
  </p>
  <p align="center"><em>Figure 14: client_loop: send disconnect: Broken pipe.</em></p>


  <p align="center">
    <img src="./figs/crashmemrange.png" alt="Crashing memory range" width="75%"/>
  </p>
  <p align="center"><em>Figure 15: Crashing memory range.</em></p>

  A possible explanation is that the crash is caused by illegal attempts to read memory addresses storing privileged software.  

  This crash raises concerns about a possible failure in memory isolation when accessed by processes, such as the `memory_reader.py` script. Another possibility is that the privileged software running in this memory range is particularly sensitive to illegal read attempts, causing cheriOS crashes. Further investigation is required to determine the exact causes.

- **Error after rebooting the cheriBSD OS:**  
  Attempt to read memory after rebooting to recover from a crash outputs `[Errno 2] No such file or directory: '/proc/PID/mem'` (see Figure 16). The error indicates that file `/proc/{pid}/mem`, which is used by `memory_reader.py`, is unavailable.

  <p align="center">
    <img src="./figs/proc_pid_mem_error.png" alt="Error after recovering from a crash: [Errno 2] No such file or directory: '/proc/3587/mem'" width="75%"/>
  </p>
  <p align="center"><em>Figure 16: Error after recovering from a crash: [Errno 2] No such file or directory: '/proc/3587/mem'.</em></p>

- **Procedure for running `memory_reader.py` after rebooting:**  
  After rebooting to recover from a crash, it is necessary to verify that the `/proc` file system is mounted correctly mounted, the `mount` command can be used.

  ```bash
  $ mount | fgrep proc
  ```

  The following command can be used to mount `/proc` if it is not mounted.  

  ```bash
  $ mount -t procfs proc /proc
  ```

  Once `proc` is mounted, the `memory_reader.py` script [memory_reader.py](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/mem-reader-python-scripts/memory_reader.py) script can be executed again.  

  We believe that this behaviour is related to the persistence of cheriBSD configurations after rebooting from crashes. It might be useful to examine how resources are locked and released by cheriBSD after crashes.




# 8. Examination of memory isolation in executions with shared libraries

To explore memory isolation further, we executed a C program that communicates a parent and a child process over a pipe after compiling them using dynamic libraries. In this experiment we have the following C codes:

- `library_a.c`: the parent process that writes a string to one end of the pipe.
- `library_b.c`: the child process that reads the string from the other end of the pipe.
- `pipe-trampoline-in-experiment.c`: the main C program that creates the parent and child process when it is executed within compartments.

The compilation process is divided into two steps: Firstly, each individual module is compiled separately to create a dynamic library. Secondly, the main executable is compiled taking the dynamic libraries as input to create the main executable. In this example, we used two modules and therefore, we produce two dynamic libraries.

1. **Compilation of the parent library for the purecap ABI:**

   To create the object file `library_a.o` from the source file `library_a.c`, execute:

   ```bash
   $ clang-morello -march=morello+c64 -mabi=purecap -fPIC -c library_a.c -o library_a.o
   ```

   The CHERI-specific settings used enable position-independent code (`-fPIC`), which is needed for creating dynamic libraries.

   To create the dynamic library `liblibrary_a.so` from the object file `library_a.o`, execute:

   ```bash
   $ clang-morello -march=morello+c64 -mabi=purecap -shared -o liblibrary_a.so library_a.o
   ```

   The source C file is available from Git:  
   [library_a.c](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/pipe-mem-secu-multicompart/purecap/library_a.c).

2. **Compilation of the child library for the purecap ABI:**

   The procedure to produce the library of the child process is similar.

   To create the object file `library_b.o` from `library_b.c`, execute:

   ```bash
   $ clang-morello -march=morello+c64 -mabi=purecap -fPIC -c library_b.c -o library_b.o
   ```

   To create the dynamic library `liblibrary_b.so` from the object file `library_b.o`, execute:

   ```bash
   $ clang-morello -march=morello+c64 -mabi=purecap -shared -o liblibrary_b.so library_b.o
   ```

   The source file is available from Git:  
   [library_b.c](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/pipe-mem-secu-multicompart/purecap/library_b.c).

3. **Compilation of the main program for the purecap ABI:**  
   The main program is compiled and linked with the dynamic libraries (`library_a.so` and `library_b.so`) created above. They are assumed to be located in the current directory specified as `-L.`.

   ```bash
   $ clang-morello -march=morello+c64 -mabi=purecap pipe-trampoline-in-experiment.c -L. -llibrary_a -llibrary_b -o pipe_trampoline
   ```

   The source C file is available from Git:  
   [pipe-trampoline-in-experiment.c](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/pipe-mem-secu-multicompart/purecap/pipe-trampoline-in-experiment.c).

4. **Execution of the main program in purecap ABI:**  
   We executed the main program within a compartment.

   - We set the `LD_LIBRARY_PATH` to enable the program to locate the shared libraries in the current directory.

     ```bash
     $ export LD_LIBRARY_PATH=.
     ```
   - To verify the PATH.

     ```bash
     $ echo $LD_LIBRARY_PATH
     ```

   - To run `pipe_trampoline` within compartments, we executed the following command:

     ```bash
     $ proccontrol -m cheric18n -s enable ./pipe_trampoline
     ```

## 8.1. Examination of memory isolation

We have performed the following steps to examine memory:

1. **Initiation of the parent and child processes:**  
   We started the `pipe_trampoline` to initiate the parent and the child process. The parent writes a string to one end of the pipe, and the child process reads it from the other end.

2. **Memory reading:**  
   We executed the `memory_reader.py` script available from [memory_reader.py](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/mem-reader-python-scripts/memory_reader.py) to attempt direct memory reads:

   ```bash
   $ python3 memory_reader.py
   ```

3. **Reading process:**  
   We executed the `memory_reader.py` script. It iterates through each RW memory region associated with the PIDs of the parent and child processes, trying to read the data from each region defined by start and end addresses. We displayed the results on the screen (see Figure 17).



## 8.2. Results

We have divided the results into three sections.

### 7.2.1. Data read from memory:

The data read from memory is available from [memory-reading-results.txt](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/pipe-mem-secu-multicompart/purecap/memory-reading-results.txt) and shows data read from memory.

The results indicate that, even when running in a multi-compartment environment, a user with root privileges is able to access data from memory. We were able to extract data, including messages and data blocks.

As a specific example, we can report that the cheriBSD crashed when we tried to access the region `0xfbfdbffff000` to `0xfbfdc0000000` which is marked with `rw---`, that is, it is a protected region.

We have stored some examples of data read in [memory-reading-results.txt](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/pipe-mem-secu-multicompart/purecap/memory-reading-results.txt).

It is sensible to think that cheriBSD blocked access to the region marked with `rw---` permission. However, the crash of cheriBSD, as a reaction, is intriguing. Further investigation is needed to fully understand the interaction between these permissions and the security policies applied to react to attempts to bypass the permissions.


### 8.2.2. Memory regions:
The memory regions are available from [memory-regions-results.txt](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/pipe-mem-secu-multicompart/purecap/memory-regions-results.txt) and show different memory regions marked with different access permissions.

Memory regions with `rw-RW` permissions allow read access without crashing the cheriBSD OS; in contrast, regions marked with `rw---` grant read access only to the owner process. Attempts to access these regions from a different process result in crashes; Figure 17 shows an example. The screenshot shows the content of the memory at crash time.

<p align="center">
  <img src="./figs/memerror_dynamiclibs.png" alt="Memory read error: attempt to read region protected by compartments" width="75%"/>
</p>
<p align="center"><em>Figure 17: Memory read error: attempt to read region protected by compartments.</em></p>


### 8.2.3. Execution results:
The execution results are available from [execution-result.txt](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/pipe-mem-secu-multicompart/purecap/execution-results.txt) and show records of parent-child communication over a pipe.

For example, line 205 (``msg received from child process TKYftt85v0l3d05SosZY1 ... iAbqS7D3VokIx'') shows the child process reading one of the strings with random characters sent by the parent process.

We managed to read this string directly from memory too. 
It is visible in the last lines of the raw version of 
the [memory-reading-results.txt](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/pipe-mem-secu-multicompart/purecap/memory-reading-results.txt) file.

_________________________________________________________________________________________________________________________________________________________________

# 9. Python scripts that can help to summarise and visualise results

If needed, these Python scripts can be used to summarise the 
raw collected metrics and present results graphically. They produce aggregated CSV files and comparative plots.

## 9.1 Python scripst for summary views  

- [Summarise CPU performance results](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/tree/main/cpu-performance/summarise-results)
- [Summarise memory performance results](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/tree/main/memory-performance/summarise-results)


## 9.2  Python script for plotting

- [Maximum number of compartments plots](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/tree/main/max_num_of_compartments_performance/plot-graph)
   
- [Memory performance plots](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/tree/main/memory-performance/plot-graph)

- [CPU performance plots](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/tree/main/cpu-performance/plot-graph)   

- [Pipe communications performance plots](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/tree/main/pipe-performance/plot-graph) 
 

_________________________________________________________________________________________________________________________________________________________________

# 10. PDF version of this report

A PDF version of this document is available for download. Please note that the PDF might be slightly behind this page in terms of updates. If it fails to open 
(Safari ver 16.6.1 produces _Error rendering embedded code_), download 
it first and then open it.

[📄 Download PDF Version](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/documents/library_based_compartments_evaluation.pdf)

_________________________________________________________________________________________________________________________________________________________________


## Acknowledgements

This work is part of the CAMB project under the responsibility of Jon ([jon.crowcroft@cl.cam.ac.uk](mailto:jon.crowcroft@cl.cam.ac.uk)) and Carlos ([carlos.molina@cl.cam.ac.uk](mailto:carlos.molina@cl.cam.ac.uk)) from [The Centre for ReDecentralisation (CRDC)](https://www.cl.cam.ac.uk/research/srg/projects/crdc/) led by Jon.

The experiments and results reported on this web page are being conducted in collaboration with the [Applied Computing Research (GCA) Group](http://gca.unijui.edu.br/member/), Unijuí, Brazil, led by Rafael Z. Frantz ([rzfrantz@unijui.edu.br](mailto:rzfrantz@unijui.edu.br)). The joint effort emerged from a long-term international collaboration between the two research groups and reflects the interest of the GCA in the [Digital Security by Design (DSbD)](https://www.dsbd.tech/) programme activities, particularly in CHERI capabilities and the Morello platform.

          
## Corresponding Authors

**Regis Rodolfo Schuch**  
*Applied Computing Research (GCA) Group, Unijui University, Brazil*  
[regis.schuch@unijui.edu.br](mailto:regis.schuch@unijui.edu.br)

**Carlos Molina-Jimenez**  
*Computer Lab, University of Cambridge*  
[carlos.molina@cl.cam.ac.uk](mailto:carlos.molina@cl.cam.ac.uk)


memsecu-multicompart
