// clang-morello -march=morello+c64 -mabi=purecap -fPIC -c caller.c -o caller.o
// clang-morello -march=morello+c64 -mabi=purecap -shared -o libcaller.so caller.o

#include <stdio.h>
#include <unistd.h>
#include <string.h>

void caller_process(int write_fd) {
    char message[256];
    snprintf(message, sizeof(message), "Hello from Caller");
    if (write(write_fd, message, strlen(message) + 1) == -1) {
        perror("Failed to write in caller_process");
    } else {
        printf("[Caller] Sent message: %s\n", message);
    }
}

