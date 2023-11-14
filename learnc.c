#include <stdio.h>

int main(int argc, char const *argv[])
{
	printf("Enter a few lines\n");
	char c;
	long int count = 0;
	while ((c = getchar()) != EOF) {
		if (c == '\n') {
			count++;
		}
	}
	printf("Total lines in the input is %ld\n", count);
}