%{
	#include <stdio.h>
	#define MAX(x, y) (((x) > (y)) ? (x) : (y))

	extern int yylineno;

	int yylex();

	void yyerror(const char *msg) {
		printf("[line=%d] %s\n", yylineno + 1, msg);
	}
%}

%union {
	struct {
		int value;
		int height;
		int sum;
	} tree;
	int intval;
}

%token <intval> NUMBER
%token SUM
%token ZERO
%token HEIGHT
%token DOUBLE
%token PAREN_START
%token PAREN_END
%token ERROR
%token END_OF_FILE

%type <tree> program tree treelist

%%
program: tree { 
	printf("Tree value: %d\n", $1.value); 
};

tree: PAREN_START SUM treelist PAREN_END { 
	$$.value = $3.sum;
	$$.height = $3.height + 1; 
};

tree: PAREN_START ZERO treelist PAREN_END { 
	$$.value = 0; 
	$$.height = $3.height + 1;
};

tree: PAREN_START HEIGHT treelist PAREN_END { 
	$$.value = $3.height; 
	$$.height = $3.height + 1; 
};

tree: PAREN_START DOUBLE tree PAREN_END {
	$$.value = 2 * $3.value;
	$$.height = $3.height + 1;
}

tree: NUMBER {
	$$.value = $1;
	$$.height = 1;
}

treelist: treelist tree {
	$$.sum = $1.sum + $2.value;
	$$.height = MAX($1.height, $2.height);
}

treelist: tree {
	$$.sum = $1.value;
	$$.height = $1.height;
}
%%