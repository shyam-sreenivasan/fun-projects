#include <stdio.h>
int test = 25;
int main(int argc, char const *argv[])
{
	extern int test;
	printf("Test value before %d\n",test);
	test = 10;
	printf("Test value after %d\n",test);	

}