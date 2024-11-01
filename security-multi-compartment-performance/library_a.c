#define _POSIX_C_SOURCE 199309L // Definição para expor CLOCK_MONOTONIC

#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <time.h>
#include <string.h>
#include "library_a.h"

#define STRLEN     1024
#define NUM_OF_MSG 100

void parent_process(int pipechan[]) {
    printf("I'm the PARENT process!\n");
    close(pipechan[1]);
    char buf1[STRLEN];
    struct timespec start_read, end_read;

    FILE *log_file = fopen("pipe-in-experiment-result.csv", "a");
    if (log_file == NULL) {
        printf("error: opening CSV file.\n");
        exit(1);
    }

    for (int i = 0; i < NUM_OF_MSG; i++) {
        if (clock_gettime(CLOCK_MONOTONIC, &start_read) == -1) {
            perror("clock_gettime failed");
            exit(-1);
        }

        if (read(pipechan[0], buf1, STRLEN) < 0) {
            printf("error: reading from pipe failed!!!\n");
            exit(-1);
        }

        if (clock_gettime(CLOCK_MONOTONIC, &end_read) == -1) {
            perror("clock_gettime failed");
            exit(-1);
        }

        double read_time = ((end_read.tv_sec - start_read.tv_sec) * 1000.0) +
                           ((end_read.tv_nsec - start_read.tv_nsec) / 1e6);

        double write_time;
        if (read(pipechan[0], &write_time, sizeof(double)) < 0) {
            printf("error: reading write time from pipe failed!!!\n");
            exit(-1);
        }

        double total_time = write_time + read_time;
        fprintf(log_file, "%d,%d,%.3f,%.3f,%.3f\n", i + 1, STRLEN, write_time, read_time, total_time);

        printf("i= %d\n!!!!!!!!msg received from child process %s : \n", i, buf1);
    }

    fclose(log_file);

    printf("Press Enter to terminate the PARENT process...\n");
    getchar();
}
