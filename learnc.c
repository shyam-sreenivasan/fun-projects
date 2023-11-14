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