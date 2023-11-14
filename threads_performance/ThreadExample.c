#include <stdio.h>
#include <pthread.h>
#include <sys/time.h>
#include <stdlib.h>

int TOTAL_THREADS;
int MAX_ITERATIONS;
void* count(void* arg) {
    int tid = *((int*)arg);
    int counter = 0;

    for (int i = 0; i < MAX_ITERATIONS; i++) {
        counter++;
    }

    // printf("Thread %d done. Counter= %d\n", tid, counter);

    pthread_exit(NULL);
}

int main(int argc, char* argv[]) {
    int total_threads = atoi(argv[1]);
    int max_iterations = atoi(argv[2]);
    
    TOTAL_THREADS = total_threads;
    MAX_ITERATIONS = max_iterations;
    pthread_t threads[TOTAL_THREADS];
    int thread_ids[TOTAL_THREADS];

    // Record start time
    struct timeval start, end;
    gettimeofday(&start, NULL);

    // Create threads
    for (int i = 0; i < TOTAL_THREADS; i++) {
        thread_ids[i] = i;
        if (pthread_create(&threads[i], NULL, count, (void*)&thread_ids[i]) != 0) {
            perror("Error creating thread");
            return 1;
        }
    }

    // Wait for threads to complete
    for (int i = 0; i < TOTAL_THREADS; i++) {
        if (pthread_join(threads[i], NULL) != 0) {
            perror("Error joining thread");
            return 1;
        }
    }

    // Record end time
    gettimeofday(&end, NULL);

    // Calculate elapsed time in milliseconds
    long elapsed_time = (end.tv_sec - start.tv_sec) * 1000 + (end.tv_usec - start.tv_usec) / 1000;

    printf("%ld\n", elapsed_time);

    return 0;
}
