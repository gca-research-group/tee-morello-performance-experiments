#define _POSIX_C_SOURCE 199309L // Definição para expor CLOCK_MONOTONIC

#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <time.h>
#include <string.h>
#include "library_b.h"

#define STRLEN     1024
#define NUM_OF_MSG 100

void rand_str(char *dest, size_t length) {
    char charset[] = "0123456789"
                     "abcdefghijklmnopqrstuvwxyz"
                     "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    while (length-- > 0) {
        size_t index = (double) rand() / RAND_MAX * (sizeof charset - 1);
        *dest++ = charset[index];
    }
    *dest = '\0';
}

void child_process(int pipechan[]) {
    printf("I'm the CHILD process!\n");
    close(pipechan[0]);
    struct timespec start_write, end_write;

    for (int k = 0; k < NUM_OF_MSG; k++) {
        char *str = (char *) malloc(STRLEN);
        str[STRLEN-1] = '\1';
        rand_str(str, STRLEN-1);

        if (clock_gettime(CLOCK_MONOTONIC, &start_write) == -1) {
            perror("clock_gettime failed");
            exit(-1);
        }

        if (write(pipechan[1], str, STRLEN) < 0) {
            printf("error: writing to pipe failed!!!\n");
            exit(-1);
        }

        if (clock_gettime(CLOCK_MONOTONIC, &end_write) == -1) {
            perror("clock_gettime failed");
            exit(-1);
        }

        double write_time = ((end_write.tv_sec - start_write.tv_sec) * 1000.0) +
                            ((end_write.tv_nsec - start_write.tv_nsec) / 1e6);

        if (write(pipechan[1], &write_time, sizeof(double)) < 0) {
            printf("error: writing write time to pipe failed!!!\n");
            exit(-1);
        }

        free(str);
    }

    printf("Press Enter to terminate the CHILD process...\n");
    getchar();
}
