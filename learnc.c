#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

int x = 0;

void hello() {
	printf("Hello is a function pointer");
}

void hello_wrapper(void (*f)()) {
	f();
}

int main(int argc, char const *argv[])
{
	hello_wrapper(hello);
}  