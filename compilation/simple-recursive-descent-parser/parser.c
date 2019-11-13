#include <stdbool.h>
#include <stdio.h>
#include <string.h>

char* currentToken = NULL;

bool S();
bool A();
bool B();

// S1 -> aBAa
bool S1() {
  char* originalToken = currentToken;
  if ('a' != *currentToken++) { currentToken = originalToken; return false; }
  if (!B()) { currentToken = originalToken; return false; }
  if (!A()) { currentToken = originalToken; return false; }
  if ('a' != *currentToken++) { currentToken = originalToken; return false; }
  return true;
}

// S2 -> Ac
bool S2() {
  char* originalToken = currentToken;
  if (!A()) { currentToken = originalToken; return false; }
  if ('c' != *currentToken++) { currentToken = originalToken; return false; }
  return true;
}

// S -> S1 | S2
bool S() {
  char* originalToken = currentToken;
  if (S1()) { return true; } currentToken = originalToken;
  if (S2()) { return true; } currentToken = originalToken;
  return false;
}

// A1 -> bB
bool A1() {
  char* originalToken = currentToken;
  if ('b' != *currentToken++) { currentToken = originalToken; return false; }
  if (!B()) { currentToken = originalToken; return false; }
  return true;
}

// A2 -> epsilon
bool A2() {
  return true;
}

// A -> A1 | A2 
bool A() {
  char* originalToken = currentToken;
  if (A1()) { return true; } currentToken = originalToken;
  if (A2()) { return true; } currentToken = originalToken;
  return false;
}

// B1 -> abS
bool B1() {
  char* originalToken = currentToken;
  if ('a' != *currentToken++) { currentToken = originalToken; return false; }
  if ('b' != *currentToken++) { currentToken = originalToken; return false; }
  if (!S()) { currentToken = originalToken; return false; }
  return true;
}

// B2 -> bbSB
bool B2() {
  char* originalToken = currentToken;
  if ('b' != *currentToken++) { currentToken = originalToken; return false; }
  if ('b' != *currentToken++) { currentToken = originalToken; return false; }
  if (!S()) { currentToken = originalToken; return false; }
  if (!B()) { currentToken = originalToken; return false; }
  return true;
}

// B2 -> caB
bool B3() {
  char* originalToken = currentToken;
  if ('c' != *currentToken++) { currentToken = originalToken; return false; }
  if ('a' != *currentToken++) { currentToken = originalToken; return false; }
  if (!B()) { currentToken = originalToken; return false; }
  return true;
}

// B -> B1 | B2 | B3 
bool B() {
  char* originalToken = currentToken;
  if (B1()) { return true; } currentToken = originalToken;
  if (B2()) { return true; } currentToken = originalToken;
  if (B3()) { return true; } currentToken = originalToken;
  return false;
}

int main(int argc, char* argv[]) {
  if (2 != argc) {
    printf("USAGE: ./parser <input-string>\n");
    printf("EXAMPLE: ./parser aabca\n");
    return 1;
  }

  char* input = argv[1];
  currentToken = input;

  if (S() && currentToken == (input + strlen(input))) {
    printf("Parse successful.\n");
  } else {
    printf("Parse failure.\n");
  }

  return 0;
}