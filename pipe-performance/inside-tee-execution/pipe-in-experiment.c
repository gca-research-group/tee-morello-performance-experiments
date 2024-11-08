/*
 * Programmer : Carlos Molina Jimenez
 * Institution: Computer Lab, University of Cambridge
 * 9 Sep 2024
 *
 * pipe.c 
 * communicates a parent and a child process through a pipe.
 * The parent: 
 * 1) creates a pipe 
 * 2) forks a child process
 * 3) The child sends N schar strings of 1024 bytes
 * 4) N is meant to be large such as N= 1 000 000 to
 *    send 1GB = 1x10 exp 9 of chars
 * N can is defined and can be changed through NUM_OF_MSG
 * #define NUM_OF_MSG 100
 * 
 *
 * I) Compile and run without library compartmentalisation:
 * cm770@morello-camb-2: $ clang-morello -o pipe pipe.c
 *
 * cm770@morello-camb-2: $ ./pipe
 * I'm the PARENT process!
 * I'm the CHILD process!
 * i= 0
 * !!!!!!!!msg recv from child proc EL24imDZwzUdbYQgcRI8so
 * ...
 *
 *
 * II) Compile and run with library compartmentalisation:
 *
 * cm770@morello-camb-2: $ clang-morello -march=morello+c64 -mabi=purecap -g -o pipe pipe.c -L. -lm
 * clang-14: warning: Using c64 in the arch string is deprecated. The CPU mode should be inferred from the ABI. [-Wdeprecated]
 *
 * cm770@morello-camb-2: $ proccontrol  -m cheric18n -s enable pipe
 * I'm the PARENT process!
 * I'm the CHILD process!
 * i= 0
 * !!!!!!!!msg recv from child proc EL24imDZwzUdbY 
 * ...
 */

#include        <stdlib.h>
#include	<unistd.h>
#include        <stdio.h>
#include        <time.h>
#include        <assert.h>
#include        <string.h>

#define STRLEN     1024 
#define NUM_OF_MSG 100

/*
 source
 https://stackoverflow.com/questions/15767691/whats-the-c-library-function-to-generate-random-string
 */
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

int main()
{
    int pipechan[2], child;

    FILE *log_file = fopen("pipe-in-experiment-result.csv", "w");
    if (log_file == NULL) {
        printf("error: opening CSV file.\n");
        exit(1);
    }

    fprintf(log_file, "Test,Message Size (Bytes),Write Time (ms),Read Time (ms),Total Time (ms)\n");
    fclose(log_file); 

    if (pipe(pipechan)) {
        printf("error: opening stream sockets pair");
        exit(10);
    }

    if ((child = fork()) == -1) {
        printf("error: fork child1 failed"); 
        exit(-1);
    }

    if (child > 0) /* parent proc */
    {
        printf("I'm the PARENT process!\n"); 
        close(pipechan[1]);  
        char buf1[STRLEN];
        struct timespec start_read, end_read;

        log_file = fopen("pipe-in-experiment-result.csv", "a");
        if (log_file == NULL) {
            printf("error: opening CSV file.\n");
            exit(1);
        }

        for (int i = 0; i < NUM_OF_MSG; i++) 
        {
            clock_gettime(CLOCK_MONOTONIC, &start_read);
            
            if (read(pipechan[0], buf1, STRLEN) < 0) 
            {
                printf("error: reading from pipe failed!!!");
                exit(-1);
            }

            clock_gettime(CLOCK_MONOTONIC, &end_read);

            // Calculate read time
            double read_time = ((end_read.tv_sec - start_read.tv_sec) * 1000.0) +
                               ((end_read.tv_nsec - start_read.tv_nsec) / 1e6);

            double write_time;
            if (read(pipechan[0], &write_time, sizeof(double)) < 0) {
                printf("error: reading write time from pipe failed!!!");
                exit(-1);
            }

            // Calculate total time
            double total_time = write_time + read_time;

            // Log data to CSV
            fprintf(log_file, "%d,%d,%.3f,%.3f,%.3f\n", i + 1, STRLEN, write_time, read_time, total_time);

            // Print message to terminal, as in original code
            printf("i= %d", i);
            printf("\n\n\n!!!!!!!!msg recv from child proc %s : \n", buf1);
            printf("\n\n\n");
        }

        fclose(log_file);  

    } else /* child proc */
    {
        printf("I'm the CHILD process!\n"); 
        close(pipechan[0]);
        struct timespec start_write, end_write;

        for (int k = 0; k < NUM_OF_MSG; k++) 
        { 
            char *str = (char *) malloc(STRLEN);

            str[STRLEN-1] = '\1';
            rand_str(str, STRLEN-1);
            
            clock_gettime(CLOCK_MONOTONIC, &start_write);

            if (write(pipechan[1], str, STRLEN) < 0) 
            {
                printf("error: writing to pipe failed!!!");
                exit(-1);
            }

            clock_gettime(CLOCK_MONOTONIC, &end_write);

            // Calculate write time
            double write_time = ((end_write.tv_sec - start_write.tv_sec) * 1000.0) +
                                ((end_write.tv_nsec - start_write.tv_nsec) / 1e6);

            // Send write time to parent process
            if (write(pipechan[1], &write_time, sizeof(double)) < 0) {
                printf("error: writing write time to pipe failed!!!");
                exit(-1);
            }

            free(str);
        }
    }
}
