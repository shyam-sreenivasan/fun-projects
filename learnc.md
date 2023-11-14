
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

### Parse and print the command line arguments
```c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char const *argv[])
{
	if(argc < 2) {
		printf("Please pass atleast 1 argument");
		exit(0);
	}

	int counter = 0;
	for(int counter=0; counter < argc; counter++) {
		printf("%s\n", argv[counter]);
	}
}
```

### mimic the word count (wc) linux utility given an input paragraph
```c
#include <stdio.h>
#include <stdlib.h>

#define IN 0
#define OUT 1

int main(int argc, char const *argv[])
{
	int nc = 0, nw = 0;
	int state = OUT;
	char c;
	printf("Enter a paragraph\n");
	while ((c = getchar()) != EOF) {
		nc++;
		if(c == ' ' || c == '\t' || c == '\n') {
			state = OUT;
		} else if (state == OUT) {
			state = IN;
			nw++;
		}
	}
	printf("\nTotal words is %d\n", nw);
}
```

### Count the digits, white-spaces and other characters in paragraph.
```c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char const *argv[])
{
	int ndigit[10], nwhite, nother, nc;
	nwhite = nother = nc = 0;
	for(int i=0; i<10; i++) {
		ndigit[i] = 0;
	}

	int c;
	while ((c = getchar()) != EOF) {
		nc++;
		if(c >= '0' && c <= '9') {
			ndigit[c - '0'] += 1;
		} else if(c == ' ' || c == '\n' || c =='\t') {
			nwhite++;
		} else {
			nother++;
		} 
	}

	printf("\nTotal characters %d\n", nc);
	printf("\nTotal numbers\n");
	for(int i=0; i<10; i++) {
		printf("%d ", ndigit[i]);
	}
	printf("\n");
	printf("White spaces count %d\n", nwhite);
	printf("Other characters %d\n", nother);
}
```

### Read input into a array of char arrays and print line by line.
```c
#include <stdio.h>
#include <stdlib.h>
#define MAX_CHAR_PER_LINE 100
#define MAXLINES 10

int mygetline(char line[], int max_char_per_line);
void copy(char from[], char to[]);
void clearline(char line[], int len);


int main(int argc, char const *argv[])
{
	char line[MAX_CHAR_PER_LINE];
	char lines[MAXLINES][MAX_CHAR_PER_LINE];
	int len, nline;
	len = nline = 0;
	while (( len = mygetline(line, MAX_CHAR_PER_LINE)) > 0) {
		copy(line, lines[nline]);
		clearline(line, len);
		nline++;
	}

	for(int i=0; i<nline; i++) {
		printf("\nLine %d: %s",i , lines[i]);
	}
	printf("\n");
	return 0;
}

int mygetline(char line[], int max_char_per_line) {
	char c;
	int i = 0;
	while ((i < max_char_per_line - 1) && ((c = getchar()) != '\n') && c != EOF) {
		line[i] = c;
		i++;
	}

	if(c == '\n') {
		line[i] = '\0';
	}
	return i;
}

void copy(char from[], char to[]) {
	for(int i =0; from[i] != '\0'; i++) {
		to[i] = from[i];
	}
}

void clearline(char line[], int len) {
	for (int i=0; i<len; i++) {
		line[i] = '\0';
	}
}
```