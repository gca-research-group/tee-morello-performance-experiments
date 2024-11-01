// clang-morello -march=morello+c64 -mabi=purecap -fPIC -c trampoline.c -o trampoline.o
// clang-morello -march=morello+c64 -mabi=purecap -shared -o libtrampoline.so trampoline.o

#include <stdio.h>
#include <unistd.h>
#include <string.h>

void trampoline_process(int read_fd, int write_fd) {
    char buffer[256];
    ssize_t bytes_read;
    while (1) {
        bytes_read = read(read_fd, buffer, sizeof(buffer));
        if (bytes_read > 0) {
            printf("[Trampoline] Forwarded message: %s\n", buffer);
            if (write(write_fd, buffer, bytes_read) == -1) {
                perror("Failed to write in trampoline_process");
                break;
            }
        } else {
            perror("Error reading in trampoline_process");
            break;
        }
    }
}