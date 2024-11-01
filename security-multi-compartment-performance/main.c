// clang-morello -march=morello+c64 -mabi=purecap main.c -L. -lcaller -lcallee -ltrampoline -o main_program

// export LD_LIBRARY_PATH=.
// proccontrol -m cheric18n -s enable ./main_program

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include "caller.h"
#include "callee.h"
#include "trampoline.h"

int main() {
    int pipe_a_to_tramp[2], pipe_tramp_to_b[2];

    if (pipe(pipe_a_to_tramp) == -1 || pipe(pipe_tramp_to_b) == -1) {
        perror("Failed to create pipes");
        exit(EXIT_FAILURE);
    }

    pid_t trampoline_pid = fork();
    if (trampoline_pid == -1) {
        perror("Failed to fork trampoline");
        exit(EXIT_FAILURE);
    }

    if (trampoline_pid == 0) {  // Trampoline process
        close(pipe_a_to_tramp[1]);  // Close write end of Caller->Trampoline pipe
        close(pipe_tramp_to_b[0]);  // Close read end of Trampoline->Callee pipe
        trampoline_process(pipe_a_to_tramp[0], pipe_tramp_to_b[1]);
        close(pipe_a_to_tramp[0]);
        close(pipe_tramp_to_b[1]);
        printf("[Trampoline] Process completed\n");
        exit(EXIT_SUCCESS);
    }

    pid_t callee_pid = fork();
    if (callee_pid == -1) {
        perror("Failed to fork callee");
        exit(EXIT_FAILURE);
    }

    if (callee_pid == 0) {  // Callee process
        close(pipe_a_to_tramp[0]);
        close(pipe_a_to_tramp[1]);
        close(pipe_tramp_to_b[1]);  // Close write end of Trampoline->Callee pipe
        callee_process(pipe_tramp_to_b[0]);
        close(pipe_tramp_to_b[0]);
        printf("[Callee] Process completed\n");
        exit(EXIT_SUCCESS);
    }

    // Caller process
    close(pipe_a_to_tramp[0]);  // Close read end of Caller->Trampoline pipe
    close(pipe_tramp_to_b[0]);
    close(pipe_tramp_to_b[1]);
    
    // Send the message once
    caller_process(pipe_a_to_tramp[1]);
    
    // Wait for user action to exit
    printf("Press Enter to exit the program...\n");
    getchar();

    close(pipe_a_to_tramp[1]);
    printf("[Caller] Process completed\n");

    // Wait for children to finish
    waitpid(trampoline_pid, NULL, 0);
    waitpid(callee_pid, NULL, 0);

    return 0;
}
