/*Lex program to recognize displayed words,numbers.*/

%{
#include<stdio.h>
%}

%%
if |
else |
printf {printf ("%s is a keyword.", yytext);}
[0-9]+ {printf ("%s is a number/digit.", yytext);}
[a-zA-Z_][a-zA-Z0-9]+ {printf ("%s is a identifier.", yytext);}
 
.|\n {ECHO;}
%%

int main()
{
printf("Enter the String: ");
yylex();
}

int yywrap()
{
return 1;
}
