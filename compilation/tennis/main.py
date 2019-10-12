import sys
import ply.lex as lex
from tabulate import tabulate

tokens = (
  'TITLE',
  'TAG',
  'STRING',
  'KEYWORD',
  'YEAR',
  'RANGE',
  'NUMBER',
  'COMMA',
)

def t_TITLE(t):
  r'\*\*.*\*\*'
  t.attribute = t.value.replace('**', '').strip()
  return t

def t_TAG(t):
  r'\<[a-zA-Z\s]+\>'
  t.attribute = t.value.replace('<', '').replace('>', '')
  return t

def t_STRING(t):
  r'\".*\"'
  t.attribute = t.value[1:-1]
  return t

def t_YEAR(t):
  r'\d{4}'
  t.attribute = int(t.value)
  return t

def t_NUMBER(t):
  r'\#\d+'
  t.attribute = int(t.value[1:])
  return t

t_KEYWORD = '[a-zA-z]+'
t_RANGE = r'\-'
t_COMMA = r'\,'

# Ignore spaces
t_ignore = ' \t\n'

# Error handling rule
def t_error(t):
  print("Illegal character '{}' on line {}".format(t.value[0], t.lineno))
  t.lexer.skip(1)

def main():

  if len(sys.argv) == 1:  # No arguments
    input_data = input()
  else:
    try:
      _, input_file_path = sys.argv
    except ValueError:
      print('USAGE: main.py <input-file-path>')
      return

    with open(input_file_path, 'r') as input_file:
      input_data = input_file.read()

  lexer = lex.lex()
  lexer.input(input_data)

  table = []

  while True:
    tok = lexer.token()
    
    if not tok: 
      # No more input
      break      
    
    table.append([tok.type, tok.value, tok.attribute if hasattr(tok, 'attribute') else ''])

  print(tabulate(table, headers=['TOKEN', 'LEXEME', 'ATTRIBUTE']))

if __name__ == '__main__':
  main()