// clang-morello -march=morello+c64 -mabi=purecap -fPIC -c caller.c -o caller.o
// clang-morello -march=morello+c64 -mabi=purecap -shared -o libcaller.so caller.o

#include <stdio.h>
#include <unistd.h>
#include <string.h>

void caller_process(int write_fd) {
    char message[256];
    for (int i = 1; i <= 10; i++) {
        snprintf(message, sizeof(message), "Hello from Caller %d", i);
        if (write(write_fd, message, strlen(message) + 1) == -1) {
            perror("Failed to write in caller_process");
        } else {
            printf("[Caller] Sent message: %s\n", message);
        }
        sleep(1);  // Delay to observe message flow
    }
    if (write(write_fd, message, strlen(message) + 1) == -1) {
        perror("Failed to write in caller_process");
    } else {
        printf("[Caller] Sent message: %s\n", message);
    }
}
