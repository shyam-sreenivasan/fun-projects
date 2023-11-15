# Concurrency and Threading

motivation

unit of concurrency
- threads
- they are similar to processes but have their own private registers, program counters and stack
- they share the address space with the process
- similar to processes , context switching takes places for threads as well.
- threads are tracking in the Thread Control Block
(context switching is essentially time sharing of cpu)


why use threads at all ?
- parallelism. when you have more cores, you can utilise them effectively.
- to avoid blocking program process due to slow IO

similar to processes where overlapping for processes take place where a process waiting for IO is suspended
and other process that want to utilise the cpu can run (context switching / scheduling)

overlapping of threads occur within a process itself.

This above thing is multiprogramming and multithreading.

> thread creation code
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

If you run this is a few times and see, you will realise you can never predict which will run first.
Computers already hard to understand without concurrency. With threads it only gets much worse.

How ??

> shared data !!



```c
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>


#define ITERATIONS 1e6
int x = 0;

void *incrementer(void* arg) {
	char *thread_name = (char*) arg;
	int y = 0;

	for(int i=0; i<ITERATIONS; i++) {
		x++;
		y++;
	}
	printf("%s, x= %d, y= %d\n", thread_name, x, y);
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
y++ looks like a simple instruction but it has 3 steps.
1. Read value from memory to the threads' private registers.
2. Increment the value 
3. Store the value in the corresponding memory

Now imagine a timer interrupt goes off after the first intruction.
The thread state along with whatever is there in its stack and registers are saved.

Now thread 2 starts running and updates the values. Then a timer interrupt goes again and thread 1
comes back alive and starts executing from where it left off. Now its registers contain the old values
and it increments that and overwrites the memory.

Now this is a nightmare because, not only we are getting the wrong value, but each time the value is unpredictable. 

Why should you care ??

Well well, think about mysql db where 2 or more threads, trying to update a specific row and such timer 
interrupts go off. Data corruption!!!
But we say mysql is ACID compliant. How does that happen ??

So what do we need here ?

- atomicity, we want the 3 actions to happen together, not in pieces.
- let's call this a transaction.
- also when a transaction occurs, we want it to be the only one modifying the shared data

atomicity is one kind of issue.
But there is another one. Sometimes processes or threads are put to sleep when waiting for some kind of I/O. when the I/O happens, how to wake this processes from sleep to process the data.

There are 2 keys ideas here. One is lock and the other is condition variables, as a form of signaling between threads or processes.

lets look at the different techniques people tried.
- single powerful instruction may be ??

- disabling and interrupt for the transaction.

```c
disable_interrupt()
// transaction goes here
enable_interrupt()
```

a brief idea about locks and condition variables.

Why not use a simple flag.
 - performs poorly wasting cpu cycles
 - it leads to lot of unforseen bugs. 
