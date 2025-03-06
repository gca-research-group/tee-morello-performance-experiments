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

To run the experiments reported in this document, we use four Morello Boards connected as shown in **Figure 1**.

- Three local Morello Boards are physically located in the William Gates building of the Computer Laboratory.
- A remote Morello Board is physically located in Toronto, within the premises of [TODAQ](https://engineering.todaq.net/), a non-funding partner of the [CAMB project](https://www.cl.cam.ac.uk/research/srg/projects/camb/).

We connect to the remote Morello Board through SSH from a laptop connected to the network of the [Applied Computing Research Group (GCA)](http://gca.unijui.edu.br/) at Unijuí, Brazil.

The figure below shows the main configuration parameters of the Morello Board under evaluation. **Table 1** lists additional parameters and the CheriBSD commands that can be used to double-check the configuration parameters.

![Morello boards used in the evaluation](memory-pipe-performance/figs/experimentsetup_morelloboard.pdf)
*Figure 1: Morello boards used in the evaluation.*

## Morello Board Configuration

**Table 1** lists the configuration parameters of the Morello Board used in the experiments, along with CheriBSD commands to verify them.

| **Component**           | **Specification**                                     | **Command**                                        |
|------------------------|-----------------------------------------------------|---------------------------------------------------|
| **Operating System**   | CheriBSD 24.5 (FreeBSD 15.0-CURRENT)                 | `uname -a`                                        |
| **Kernel Version**     | FreeBSD 15.0-CURRENT, releng/24.05                   | `uname -v`                                        |
| **Board**             | Morello System Development Platform                   | `kenv | grep smbios.system.product`              |
| **RAM**               | 17 GB detected (16 GB DDR4, 2933 MT/s, ECC)           | `dmidecode --type memory`                        |
| **Storage**           | SSD                                                  | `camcontrol identify ada0`                       |
| **Architecture**      | aarch64c (with CHERI support)                         | `sysctl hw.machine_arch`                         |
| **Processor Model**   | Research Morello SoC r0p0                            | `sysctl hw.model`                                |
| **Number of CPUs**    | 4                                                    | `sysctl hw.ncpu`                                 |
| **Compiler**         | clang (with Morello support)                          | `clang-morello --version`                        |
| **Tool**              | proccontrol (for CHERI compartments)                  | `proccontrol -m cheric18n -s enable ./binary`    |
| **Python**           | Python 3 (required for Experiments 1, 5, and 6)        | `python3 --version`                              |
| **Scripts Used**     | cheri-cap-experiment.py, cpu-in-experiment.c, memory-in-experiment.c, pipe-in-experiment.c, pipe-trampoline-in-experiment.c, library_a.c, library_b.c, memory_reader.py, integration_process.c | Not applicable |
| **Access**            | Remote via SSH                                       | `ssh -i private_key user@server`                |

---

## Compilation and Execution

The inclusion of library-based compartments is determined at compilation and execution time. It is documented in:

- **CHERI Software Compartmentalization** [Robert Watson, 2019](https://www.cl.cam.ac.uk/research/security/ctsrd/cheri/cheri-compartmentalization.html).
- **Library-based Compartmentalisation** [Cheri team, 2022](https://github.com/CTSRD-CHERI/cheripedia/wiki/Library-based-Compartmentalisation).
- **User-level software compartmentalization (experimental)** [Cheri team, 2024](https://ctsrd-cheri.github.io/cheribsd-getting-started/features/c18n.html).
- **Compartmentalization, c18n — Library-based software compartmentalization** [Dapeng Gao, 2024](https://man.cheribsd.org/cgi-bin/man.cgi/c18n).
- **Library-based Compartmentalisation on CHERI** [Dapeng Gao and Robert Watson, Plarch2023](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/documents/LibraryBasedCompartmentalisationOnCHERI_Dapeng2023.pdf).
- **Dapeng's Video Presentation** (Plarch2023) provides a summary of the architecture. [Watch here](https://www.youtube.com/watch?v=0Zk0NzfiQJA).

---

## Userspace Execution Environments

As explained in the [User Level Process Environments](https://ctsrd-cheri.github.io/cheribsd-getting-started/features/processes.html), in CheriBSD 24.05, a user can compile a program to run in three different execution environments:

- **Hybrid process**: Use default compilation.
- **CheriABI processes**: Use `-mabi=purecap`.
- **Benchmark ABI processes**: Use `-mabi=purecap-benchmark`.

A useful example of the compilation of `helloworld.c` can be found [here](https://ctsrd-cheri.github.io/cheribsd-getting-started/helloworld/index.html).

To verify the ABI targeted by the compiler, the following command can be used:

```bash
root# file binary
```

Programs to be run in **library-based compartments** can be compiled with either `-mabi=purecap` or `-mabi=purecap-benchmark`. However, for performance evaluation, the latter is recommended. See [man compartmentalization](https://man.cheribsd.org/cgi-bin/man.cgi/c18n) for details.

---

## Compilation and Execution Without Library-Based Compartments

To compile and execute a program **without** using library-based compartments, use:

```bash
$ clang-morello -o hello hello.c

$ ./helloworld
```

---

## Compilation and Execution With Library-Based Compartments

### **Compilation for Purecap ABI**

To enable **library-based compartments** during compilation, use:

```bash
$ clang-morello -march=morello+c64 -mabi=purecap -o helloworld helloworld.c
```

#### **Explanation of Compilation Parameters**
- `-march=morello+c64`: Defines the 64-bit Morello architecture.
- `-mabi=purecap`: Targets the **Application Binary Interface (ABI)**, implementing all memory references and pointers as **capabilities**.

To execute the compiled program **within a library-based compartment**, use:

```bash
$ proccontrol -m cheric18n -s enable helloworld
```

The **proccontrol** command enables execution within a **library-based compartment**.

---

### **Compilation for Purecap-Benchmark ABI**

The compilation and execution process for **purecap-benchmark ABI** is similar to **purecap ABI**, with the exception of using:

```bash
$ clang-morello -march=morello+c64 -mabi=purecap-benchmark -o helloworld helloworld.c

$ proccontrol -m cheric18n -s enable helloworld
```






# 2. Memory performance in the execution of allocate, release, read and write Operations

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


## 2.1 Compilation and execution without compartments
  

  ```bash

   $ clang-morello -o memory-out-experiment memory-out-experiment.c -lm

   $ ./memory-out-experiment

  ```

We stored the metrics collected in the 
[memory-out-experiment-results.csv](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/memory-performance/outside-tee-execution/memory-out-experiment-results.csv) file.
We calculate the average time that it takes to allocate, write, read and free for  each block size of 100 MB, 200 MB, 300 MB, etc.). The 
results are summarised in Table 2.


<div align="center">
<p><em>Table 2: Metrics of runs outside a compartment, including mean and standard deviation.</em></p>


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





## 2.2 Compilation and execution withing compartments created to run in purecap ABI

  ```bash
  $ clang-morello -march=morello+c64 -mabi=purecap -o memory-in-experiment-purecap memory-in-experiment-purecap.c -lm
  
  $ proccontrol -m cheric18n -s enable memory-in-experiment-purecap
  ```

The metrics collected are stored in two separate csv files: [memory-in-experiment-purecap-results.csv](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/memory-performance/inside-tee-execution-purecap/memory-in-experiment-purecap-results.csv) for the run inside a compartment. 
We calculate the average time that it takes to allocate, write, 
read and free for  each block size of 100 MB, 200 MB, 300 MB, 
etc.). The results are summarised in Tables 3.


  
<div align="center">
<p><em>Table 3: Metrics of runs inside compartment created for the
purecap ABI, including mean and standard deviation.</em></p>


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




## 2.3 Compilation and execution withing compartments created to run in purecap-benchmark ABI
 
 
  ```bash
  $ clang-morello -march=morello+c64 -mabi=benchmark -o memory-in-experiment-purecap-benchmark memory-in-experiment-purecap-benchmark.c -lm
  
  $ proccontrol -m cheric18n -s enable memory-in-experiment-purecap-benchmark
  ```

The metrics collected are stored in two separate CSV files: [memory-in-experiment-purecap-benchmark-results.csv](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/memory-performance/inside-tee-execution-purecap-benchmark/memory-in-experiment-purecap-benchmark-results.csv) for the run inside a compartment. 
We calculate the average time that it takes to allocate, write, 
read and free for  each block size of 100 MB, 200 MB, 300 MB, 
etc.). The results are summarised in Table 4.

  
<div align="center">
<p><em>Table 4: Metrics of runs inside a compartment compiled for the
bechmark ABI, including mean and standard deviation.</em></p>

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




## 2.4. Comparion of results

Plots of the results from Tables 2, 3 and 4 are shown in Figure 2.  

<p align="center">
  <img src="./figs/perfor_mem_oper_compare.png" alt="Time to execute allocate, write, read and release memory operations" width="100%"/>
</p>
<p align="center"><em>Figure 2: Comparison of time to execute allocate, write, read 
   and release memory operations: no copartment, compartment for purecap and benchmark ABI.</em></p>


- **Allocation time:** The results in the tables reveal that it takes significantly longer to allocate memory blocks inside compartments. For example, allocating 100 MB takes approximately 2 ms without a compartment, whereas it takes 93 ms in the purecap ABI compartment and 81 ms in the purecap-benchmark ABI compartment. Allocation times without a compartment range from 2 to 5 ms for block sizes between 100 MB and 1000 MB, whereas inside compartments, they range from 93 to 288 ms for the purecap ABI and 81 to 283 ms for the purecap-benchmark ABI.

- **Write time:** The tables show a linear increase in write time as the block size increases. Execution inside a compartment consistently takes longer. For example, writing a 100 MB block takes 282,584 ms without a compartment, compared to 283,239 ms in the purecap ABI compartment and 40,369 ms in the purecap-benchmark ABI compartment. The difference becomes more evident as block sizes grow, particularly in the purecap ABI.

- **Read time:** The time to execute read operations increases linearly in all scenarios. However, execution within compartments shows consistently longer read times. For example, reading 100 MB takes 282,581 ms without a compartment, compared to 283,133 ms in the purecap ABI compartment and 80,737 ms in the purecap-benchmark ABI compartment.

- **Free time:** The metrics in the tables highlight contrasting performances for freeing memory. Without a compartment, free times range from 6 to 18 ms. In the purecap ABI compartment, free times range from 89 to 444 ms, and in the purecap-benchmark ABI compartment, they range from 86 to 443 ms. The results demonstrate that freeing memory inside compartments introduces significant delays.

A boxplot is shown in Figure 3.

<p align="center">
  <img src="./figs/boxplot_perfor_mem_oper_compare.png" alt="Dispersion of the time to execute allocate, write, read, and free operations" width="100%"/>
</p>
<p align="center"><em>Figure 3: Comparison of dispersion of the time to execute 
   allocate, write, read, and free operations: no copartment, compartment for purecap and benchmark ABI.</em></p>






# 3. Communication performance over pipes

This experiment was conducted to evaluate how the use of compartments affects the performance of communication over Unix pipes. To collect metrics, we have implemented a C program that communicates a parent with a child process over a pipe and collects metrics about writing to and reading from a pipe that interconnected them. As shown in Figure 4, the parent process writes a message to the pipe and the child process reads it.

<p align="center">
  <img src="./figs/parent-child-pipe.png" alt="Parent-child communication over a pipe"/>
</p>
<p align="center"><em>Figure 4: Parent--child communication over a pipe.</em></p>

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


Algorithm 3 describes the execution of the operations and the settings of timers to collect the metrics.


<pre style="border: 1px solid #ddd; padding: 10px; background-color: #f9f9f9; font-family: monospace;">
Algorithm 2: Pipe Communication Performance

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

In Algorithm 2, the `start_test` function (line 1) initiates a sequence of operations that measure the performance of pipe communication between the parent and child processes. The parameters `STRLEN` and `NUM_OF_MSG` (lines 3 and 4) establish the message size and the number of messages to be sent, respectively. For each iteration, from 1 to `NUM_OF_MSG` (line 5), the parent starts the write timer (line 7), writes a message of size `STRLEN` to the pipe (line 8), stops the write timer (line 9), and then sends the recorded `write_time` back through the pipe (line 10). The child process, in turn, reads the message and the `write_time` from the pipe (lines 12 and 13). To collect the metrics, the child process starts the read timer before reading (line 14) and stops it upon completing the reading (line 15). The test number, along with the write and read times, is logged in the log file (line 16). The procedure is repeated for each iteration until all messages are written to and read from the pipe (line 17).



## 3.1. Results

Table 5, Table 6 and Table 7 contain the results of each iteration, including message size, write time, read time, and total time taken for the operations.


The metrics collected from the run of the experiment 
inside a compartment for the purecap ABI are stored
in the [pipe-in-experiment-purecap-results.csv](https://github.com/CAMB-DSbD/tee-morello-performance-experiments/blob/main/pipe-performance/inside-tee-execution-purecap/pipe-in-experiment-purecap-results.csv) file.


<div align="center">
<p><em>Table 5: Time to execute write and read from a pipe inside a compartment for
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
<p><em>Table 6: Time to execute write and read from a pipe inside a compartment for
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
<p><em>Table 7: Time to execute write and read from a pipe without a compartment.</em></p>

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

A graphical view of the results is shown in Figure 5.

<p align="center">
  <img src="./figs/pipe_comm_perfor.png" alt="Times to write and read a 1024 byte string from a pipe executed in compartments and without compartments" width="100%"/>
</p>
<p align="center"><em>Figure 5: Times to write and read a 1024 byte string from a pipe executed in compartments and without compartments.</em></p>

The figure reveals that compartments affect performance. The write operation executed inside compartments consistently shows a higher latency that ranges from 0.016 ms to 0.003 ms. In contrast, the write time outside compartments is notably shorter, closer to 0.001 ms. This discrepancy highlights the additional computational cost introduced by the compartment.

The effect of the compartment on the performance of the read operation is less severe yet, it is visible. The first test shows a read time of 0.161 ms, compared to 0.059 ms in the execution without compartments. As the tests progress, the execution within the compartment consistently exhibits longer read times. This demonstrates that compartmentalisation introduces delays in inter-process communication.

The results suggest the compartments provide significant benefits in terms of security; yet they incur performance costs; the cost might not be negligible in applications that rely on rapid inter--process communication.

