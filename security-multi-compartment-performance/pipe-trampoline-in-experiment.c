//pipe-trampoline-in-experiment.c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <time.h>
#include <assert.h>
#include <string.h>
#include "library_a.h"
#include "library_b.h"

// Definindo STRLEN e NUM_OF_MSG no arquivo principal
#define STRLEN     1024
#define NUM_OF_MSG 100

int main() {
    int pipechan[2], child;

    FILE *log_file = fopen("pipe-in-experiment-result.csv", "w");
    if (log_file == NULL) {
        printf("error: opening CSV file.\n");
        exit(1);
    }

    fprintf(log_file, "Test,Message Size (Bytes),Write Time (ms),Read Time (ms),Total Time (ms)\n");
    fclose(log_file);

    if (pipe(pipechan)) {
        printf("error: opening stream sockets pair\n");
        exit(10);
    }

    if ((child = fork()) == -1) {
        printf("error: fork child process failed\n");
        exit(-1);
    }

    if (child > 0) { // Parent process
        parent_process(pipechan);
    } else { // Child process
        child_process(pipechan);
    }

    return 0;
}
