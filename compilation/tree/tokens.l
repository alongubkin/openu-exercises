%option noyywrap

%{
  #include "tokens.h"
%}

IGNORE [ \n\t]

%%

"sum"     { return SUM; }
"zero"    { return ZERO; }
"height"  { return HEIGHT; }
"double"  { return DOUBLE; }
"("       { return PAREN_START; }
")"       { return PAREN_END; }
[0-9]+    { yylval.intval = atoi(yytext); return NUMBER; }
[[:space:]]+      ;
%%
