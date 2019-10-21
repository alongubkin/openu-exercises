import sys
import re
import os
import ply.lex as lex
from tabulate import tabulate

SIGNATURE = "Made by Alon Gubkin"

reserved = {
  'break': 'BREAK',
  'case': 'CASE',
  'default': 'DEFAULT',
  'else': 'ELSE',
  'float': 'FLOAT',
  'if': 'IF',
  'input': 'INPUT',
  'int': 'INT',
  'output': 'OUTPUT',
  'static_cast': 'STATIC_CAST',
  'switch': 'SWITCH',
  'while': 'WHILE',
}

tokens = list(reserved.values()) + [
  # Operators
  'RELOP',        # == | != | > | < | >= | <=
  'ADDOP',        # + | -
  'MULOP',        # * | /
  'OR',           # ||
  'AND',          # &&
  'NOT',          # !

  # Other
  'ID',
  'NUM',
]

literals = ['(', ')', '{', '}', ',', ':', ';', '=']

t_RELOP = r'[\=\!\>\<]\=|\<|\>'
t_ADDOP = r'\+|\-'
t_MULOP = r'\*|\/'
t_OR = r'\|\|'
t_AND = r'\&\&'
t_NOT = r'\!'

def t_STATIC_CAST(t):
  # This rule is needed because t_ID doesn't support underscore (_) so it won't catch it
  # Note that it must be a function and not a string so it'll take precedence over t_ID
  r'static_cast'
  return t

def t_ID(t):
  r'[a-zA-Z][a-zA-Z0-9]{0,8}'

  # Check for reserved words, as recommended in:
  # http://www.dabeaz.com/ply/ply.html#ply_nn6
  t.type = reserved.get(t.value, 'ID')
  return t

def t_NUM(t):
  r'[0-9]+\.[0-9]*|[0-9]+'
  t.value = float(t.value) if '.' in t.value else int(t.value)
  return t

# Ignore spaces, tabs and newlines
t_ignore = ' \t'

# Ignore comments
t_ignore_COMMENT = r'(?s)\/\*.*\*\/'

# Error handling rule
def t_error(t):
  print("Illegal character '{}' on line {}".format(t.value[0], t.lineno), file=sys.stderr)
  t.lexer.skip(1)

 # Track line numbers
def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

def lexer(code):
  lexer = lex.lex()
  lexer.input(code)
  return lexer
    
def main():
  print(SIGNATURE, file=sys.stderr)

  try:
    _, code_path = sys.argv
  except ValueError:
    print('USAGE: cla.py <code-path>')
    return

  # Read the code file
  with open(code_path, 'r') as code_file:
    code = code_file.read()

  tokens = tabulate([[tok.type, tok.value] for tok in lexer(code)], 
    headers=['TOKEN', 'VALUE'])

  # Write the tokens file
  with open(os.path.splitext(code_path)[0] + '.tok', 'w') as tokens_file:
    tokens_file.write(SIGNATURE + '\n')
    tokens_file.write(tokens)

if __name__ == '__main__':
  main()