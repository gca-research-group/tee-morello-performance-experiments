/*
 * Programmer   : Regis Rodolfo Schuch
 * Date         : 10 June 2024
 *              : Applied Computing Research Group, Unijui University, Brazil
 *              : regis.schuch@unijui.edu.br
 *              :
 * Title        : cpu-in-experiment.c 
 *              :
 * Description  : The cpu-in-experiments.c programme carries out a series of CPU performance tests, measuring the time taken to perform
 *              : complex mathematical operations, integer arithmetic operations, floating point arithmetic operations and array 
 *              : manipulations. The results are recorded in a CSV file.
 *              : 
 *              : Code breakdown:
 *              : 1) Constants and Definitions
 *              :  a) NUM_TESTS is the number of tests to be performed for each type of operation.
 *              :  b) WORKLOAD_SIZE is the number of workload iterations in each test to stress the CPU.
 *              : 2) Test functions:
 *              :  a) perform_math_test function:
 *              :   - Performs complex mathematical operations (sin, cos, tan, sqrt, log).
 *              :   - It measures the time taken to perform these operations WORKLOAD_SIZE times and records the results in a CSV file.
 *              :  b) Perform_int_test function:
 *              :   - Performs integer arithmetic operations (*, /, -, %).
 *              :   - It measures the time taken to perform these operations WORKLOAD_SIZE times and records the results in the CSV file.
 *              :  c) Perform_float_test function:
 *              :   - Performs floating point arithmetic operations (*, /, -).
 *              :   - It measures the time taken to perform these operations WORKLOAD_SIZE times and records the results in the CSV file.
 *              :  d) Perform_array_test function:
 *              :   - Manipulates an array of integers, performing initialisation, multiplication and division operations.
 *              :   - It allocates memory for an array of size WORKLOAD_SIZE.
 *              :   - Measures the time taken to perform these operations and records the results in a CSV file.
 *              :   - Releases the allocated memory. 
 *              :
 * Compile      :
 * Capabilities : clang-morello -march=morello+c64 -mabi=purecap -o cpu-in-experiment cpu-in-experiment.c -lm
 *              :
 * run          : proccontrol -m cheric18n -s enable ./cpu-in-experiment	 
 * 
 * 
*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

#define NUM_TESTS 30
#define WORKLOAD_SIZE 100000000 

void perform_math_test(int num_of_trials, FILE *log_file, long *total_time) {
    /* for (int trial_num = 1; trial_num <= NUM_TESTS; trial_num++) { */
    for (int trial_num = 1; trial_num <= num_of_trials; trial_num++) {
        clock_t start, end;
        long cpu_time;

        start = clock();
        for (int i = 0; i < WORKLOAD_SIZE; i++) {
            volatile double result = sin(i) * cos(i) * tan(i) * sqrt(i) * log(i + 1);
        }
        end = clock();
        cpu_time = ((long)(end - start)) * 1000 / CLOCKS_PER_SEC;

        fprintf(log_file, "%d,math,%ld\n", trial_num, cpu_time);
        *total_time += cpu_time;
    }
}

void perform_int_test(int num_of_trials, FILE *log_file, long *total_time) {
    for (int trial_num = 1; trial_num <= num_of_trials; trial_num++) {
        clock_t start, end;
        long cpu_time;

        start = clock();
        for (int i = 0; i < WORKLOAD_SIZE; i++) {
            volatile int result = i * i / (i + 1);
            result -= i * i % (i + 1);
            result *= (i + 1);
            result /= (i + 2);
        }
        end = clock();
        cpu_time = ((long)(end - start)) * 1000 / CLOCKS_PER_SEC;

        fprintf(log_file, "%d,int,%ld\n", trial_num, cpu_time);
        *total_time += cpu_time;
    }
}

void perform_float_test(int num_of_trials, FILE *log_file, long *total_time) {
    /* for (int test_num = 1; test_num <= NUM_TESTS; test_num++) { */
    for (int trial_num = 1; trial_num <= num_of_trials; trial_num++) {
        clock_t start, end;
        long cpu_time;

        start = clock();
        for (int i = 0; i < WORKLOAD_SIZE; i++) {
            volatile float result = (float)i / (i + 1) * (float)i;
            result -= (float)i / (i + 2) * (float)i;
            result *= (float)i / (i + 3);
            result /= (float)i / (i + 4);
        }
        end = clock();
        cpu_time = ((long)(end - start)) * 1000 / CLOCKS_PER_SEC;

        fprintf(log_file, "%d,float,%ld\n", trial_num, cpu_time);
        *total_time += cpu_time;
    }
}

void perform_array_test(int num_of_trials, FILE *log_file, long *total_time) {
    for (int trial_num = 1; trial_num <= num_of_trials; trial_num++) {
        clock_t start, end;
        long cpu_time;
        int *array = (int *)malloc(WORKLOAD_SIZE * sizeof(int));
        if (array == NULL) {
            fprintf(log_file, "%d,array,Allocation failed\n", trial_num);
            return;
        }

        start = clock();
        for (int i = 0; i < WORKLOAD_SIZE; i++) {
            array[i] = i;
        }
        for (int i = 0; i < WORKLOAD_SIZE; i++) {
            array[i] = array[i] * 2;
        }
        for (int i = 0; i < WORKLOAD_SIZE; i++) {
            array[i] = array[i] / 2;
        }
        end = clock();
        cpu_time = ((long)(end - start)) * 1000 / CLOCKS_PER_SEC;

        free(array);

        fprintf(log_file, "%d,array,%ld\n", trial_num, cpu_time);
        *total_time += cpu_time;
    }
}

int main() {

    
    time_t t;   // not a primitive datatype
    time(&t);


    int num_of_trials= 0;    /* number of repetitions of each operation */
    int my_num_of_trials= 0; /* number of repetitions of each operation */
                             /* selected at run time */

    printf("\nThis program has been launched at (date and time): %s", ctime(&t));

    FILE *log_file = fopen("cpu-in-experiment-results.csv", "w");
    if (log_file == NULL) {
        printf("Failed to open log file\n");
        return 1;
    }

   
    /* 
    * Activate these two lines to determine the number
    * of trials at run time.
     printf("\nType the number of trials e.g., 50 : ");
     scanf("%d", &my_num_of_trials);
    */

    my_num_of_trials= 100; /* Im hard-fixing this number to tun on background */
    printf("Each operation will be executed %d times \n", my_num_of_trials);


    // Write CSV header
    fprintf(log_file, "TrialNum,Operation,CPU Time (ms)\n");

    long total_time = 0;

    num_of_trials= my_num_of_trials;
    perform_math_test(num_of_trials, log_file, &total_time);

    num_of_trials= my_num_of_trials;
    perform_int_test(num_of_trials, log_file, &total_time);

    num_of_trials= my_num_of_trials;
    perform_float_test(num_of_trials, log_file, &total_time);


    num_of_trials= my_num_of_trials;
    perform_array_test(num_of_trials, log_file, &total_time);

    fclose(log_file);

    printf("Total execution time: %ld milliseconds\n", total_time);

    return 0;
}
