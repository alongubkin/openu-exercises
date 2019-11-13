#include <stdbool.h>
#include <stdio.h>
#include <string.h>

char* lookahead = NULL;

bool S();
bool A();
bool B();

// S1 -> aBAa
bool S1() {
  if ('a' != *lookahead++) { return false; }
  if (!B()) { return false; }
  if (!A()) { return false; }
  if ('a' != *lookahead++) { return false; }
  return true;
}

// S2 -> Ac
bool S2() {
  if (!A()) { return false; }
  if ('c' != *lookahead++) { return false; }
  return true;
}

// S -> S1 | S2
bool S() {
  switch (*lookahead) {
    case 'a': return S1();
    case 'b': case 'c': return S2();
  }

  return false;
}

// A1 -> bB
bool A1() {
  if ('b' != *lookahead++) { return false; }
  if (!B()) { return false; }
  return true;
}

// A2 -> epsilon
bool A2() {
  return true;
}

// A -> A1 | A2 
bool A() {
  switch (*lookahead) {
    case 'a': case 'c': return A2();
    case 'b': return A1();
  }

  return false;
}

// B1 -> abS
bool B1() {
  if ('a' != *lookahead++) { return false; }
  if ('b' != *lookahead++) { return false; }
  if (!S()) { return false; }
  return true;
}

// B2 -> bbSB
bool B2() {
  if ('b' != *lookahead++) { return false; }
  if ('b' != *lookahead++) { return false; }
  if (!S()) { return false; }
  if (!B()) { return false; }
  return true;
}

// B3 -> caB
bool B3() {
  if ('c' != *lookahead++) { return false; }
  if ('a' != *lookahead++) { return false; }
  if (!B()) { return false; }
  return true;
}

// B -> B1 | B2 | B3 
bool B() {
  switch (*lookahead) {
    case 'a': return B1();
    case 'b': return B2();
    case 'c': return B3();
  }

  return false;
}

int main(int argc, char* argv[]) {
  if (2 != argc) {
    printf("USAGE: ./parser <input-string>\n");
    printf("EXAMPLE: ./parser aabca\n");
    return 1;
  }

  char* input = argv[1];
  lookahead = input;

  if (S() && lookahead == (input + strlen(input))) {
    printf("Parse successful.\n");
  } else {
    printf("Parse failure.\n");
  }

  return 0;
}