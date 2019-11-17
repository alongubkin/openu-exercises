#include <stdio.h>

extern FILE *yyin;

int yylex();
int yyparse();

int main(int argc, char **argv) {
	if (argc != 2) {
		fprintf(stderr, "Usage: %s <input-file>\n", argv[0]);
		return 1;
	}

	if (!(yyin = fopen(argv[1], "r"))) {
		fprintf(stderr, "Could not open file '%s'\n", argv[1]);
		return 1;
	}

	yyparse();
	return 0;
}