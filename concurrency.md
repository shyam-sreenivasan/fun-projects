# Ideals of Parallelism

## A simple counter program in c.

```c
#include <stdio.h>

int main(int argc, char const *argv[])
{
	int counter = 0;
	counter += 1;
	printf("%d\n", counter);
}

```

## This is a concurrency talk. So let's see how to create a thread in C

```c
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

void *hello(void* arg) {
	printf("Hello from %s\n", (char*) arg);
}

int main(int argc, char const *argv[])
{
	pthread_t p1, p2;
	printf("Main: begin\n");

	pthread_create(&p1, NULL, hello, "A");
	pthread_create(&p2, NULL, hello, "B");

	pthread_join(p1, NULL);
	pthread_join(p2, NULL);
	
	printf("Main: end\n");
}
```

## Let's complicate it a little more.
### Lets create 2 threads that increment a globally shared counter
```c
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>


#define ITERATIONS 10
int x = 0;

void *incrementer(void* arg) {
	char *thread_name = (char*) arg;

	for(int i=0; i<ITERATIONS; i++) {
		x++;
	}
	printf("%s, x= %d\n", thread_name, x);
}


int main(int argc, char const *argv[])
{
	pthread_t p1, p2;

	printf("Main: begin\n");
	pthread_create(&p1, NULL, incrementer, "ThreadA");
	pthread_create(&p2, NULL, incrementer, "ThreadB");

	pthread_join(p1, NULL);
	pthread_join(p2, NULL);
	
	printf("Final value of x: %d\n", x);
	printf("Main: end\n");
}
```

## OOP's why did that happen.

## May be we should use a flag ??
```c
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define ITERATIONS 1e6
int x = 0;
int flag = 0;

void *incrementer(void *arg) {
    char *thread_name = (char *)arg;

    for (int i = 0; i < ITERATIONS; i++) {
        while (flag != 0); // Spin until the flag becomes 0
        flag = 1;
        x++;
        flag = 0;
    }

    printf("%s, x= %d\n", thread_name, x);
}

int main(int argc, char const *argv[]) {
    pthread_t p1, p2;

    printf("Main: begin\n");
    pthread_create(&p1, NULL, incrementer, "ThreadA");
    pthread_create(&p2, NULL, incrementer, "ThreadB");

    pthread_join(p1, NULL);
    pthread_join(p2, NULL);

    printf("Final value of x: %d\n", x);
    printf("Main: end\n");

    return 0;
}

```

### Let's dig a little deeper into the assembly code for the counter
>run `objdump -d learn` after compiling the code using `gcc learnc.c -o learn`

- C code
```
counter += 1;
```
- Assembly instructions that correspond to this
```
addl $0x1, -0x4(%rbp): Increment the local variable by 1.

mov -0x4(%rbp), %eax: Move the value of the local variable to the %eax register.

mov %eax, %esi: Move the value in %eax to the source index register %esi.
```
#### Ofcourse I asked chatGPT to explain this assembly!!!

## So what's going on ??
- untimely timer interrupt going off in the middle
- what you really want is the 3 instructions need to happen "Atomically"
- Any group of actions that need to be performed atomically is called a "Transaction"

## What can we do ??
- may be add a single powerful instruction to the hardware that is becomes atomic
	- how about more complex data structures like BTree

- may each process can temporarily disable interrupts
	- Now thats a really dangerous thing to give interrupt control to a process.
	```c
	disable_interrupt()
	// transaction goes here
	enable_interrupt()
	```
	- any malicious code can take control of the cpu and starve other processes.


## We need some hardware + os help to do this right !!
### Enter Test-And-Set instruction and Mutexes. (aka locks)
```c
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define ITERATIONS 1e6
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
```
