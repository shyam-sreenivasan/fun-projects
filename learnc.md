
# C programs

### Hello world
```c
#include <stdio.h>

int main(int argc, char const *argv[])
{
	printf("Hello,  world\n");
	return 0;
}
```

### Celsius to Fahrenheit
```c
#include <stdio.h>
#define LOWER 0
#define UPPER 300
#define STEP 20

int main(int argc, char const *argv[])
{
	float fahr = LOWER;
	while(fahr <= UPPER) {
		float cel = ( 5 * (fahr - 32) ) / 9;
		printf("%3f\t%6.1f\n", fahr, cel);
		fahr += STEP;
	}	
}
```

### getchar() and putchar() - read and write a character to/from standard IO
```c
int main(int argc, char const *argv[])
{
	
	char c;
	while (c != '$') {
		c = getchar();
		printf("Entered char is:");
		putchar(c);
	}
	return 0;
}
```

### Count characters in input
 - for EOF value, use Ctrl + D at the end of the input string.
```c
#include <stdio.h>

int main(int argc, char const *argv[])
{
	printf("Enter a string\n");
	int n = 0;
	while(getchar() != EOF) {
		n++;
	}
	printf("\nTotal characters: %d\n", n);
	return 0;
}
```

### count the number of lines in the given standard input
- Remember to always initialise variables in c. Otherwise it can lead to junk results.
```c
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
```