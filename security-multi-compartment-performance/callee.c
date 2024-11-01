// clang-morello -march=morello+c64 -mabi=purecap -fPIC -c callee.c -o callee.o
// clang-morello -march=morello+c64 -mabi=purecap -shared -o libcallee.so callee.o

#include <stdio.h>
#include <unistd.h>

void callee_process(int read_fd) {
    char buffer[256];
    ssize_t bytes_read;
    while (1) {
        bytes_read = read(read_fd, buffer, sizeof(buffer));
        if (bytes_read > 0) {
            printf("[Callee] Received message: %s\n", buffer);
        } else {
            perror("Error reading from pipe in Callee");
            break;
        }
    }
}
