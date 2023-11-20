#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define ITERATIONS 1e7
int x = 0;
pthread_mutex_t mutex;  // Declare a mutex

void *incrementer(void* arg) {
    char *thread_name = (char*) arg;

    for (int i = 0; i < ITERATIONS; i++) {
        // Lock the mutex before accessing the shared variable
        pthread_mutex_lock(&mutex);
        x++;
        // Unlock the mutex after updating the shared variable
        pthread_mutex_unlock(&mutex);
    }

    printf("%s, x= %d\n", thread_name, x);
}

int main(int argc, char const *argv[]) {
    pthread_t p1, p2;

    // Initialize the mutex
    pthread_mutex_init(&mutex, NULL);

    printf("Main: begin\n");
    pthread_create(&p1, NULL, incrementer, "ThreadA");
    pthread_create(&p2, NULL, incrementer, "ThreadB");

    pthread_join(p1, NULL);
    pthread_join(p2, NULL);

    // Destroy the mutex
    pthread_mutex_destroy(&mutex);

    printf("Final value of x: %d\n", x);
    printf("Main: end\n");
}