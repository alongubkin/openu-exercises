import sys
import ply.lex as lex

ROMAN_DIGITS = {
  '0': '0',  # No roman digit for zero :(
  '1': 'I',
  '2': 'II',
  '3': 'III',
  '4': 'IV',
  '5': 'V',
  '6': 'VI',
  '7': 'VII',
  '8': 'VIII',
  '9': 'IX',
}

tokens = (
  'NEWLINE',
  'DIGIT',
  'TEXT',
)

t_NEWLINE = r'\n'
t_DIGIT = r'\d'
t_TEXT = r'[^\d\s][^\s]+|\d+[^\s]+|[^\d\s]'

# Ignore spaces
t_ignore = ' '

# Error handling rule
def t_error(t):
  print("Illegal character '{}'".format(t.value[0]))
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

  print('1.\t', end='')
  lineno = 2

  while True:
    tok = lexer.token()
    
    if not tok: 
      # No more input
      break      
    
    if tok.type == 'TEXT':
      print(tok.value, end=' ')
    elif tok.type == 'DIGIT':
      print(ROMAN_DIGITS[tok.value], end=' ')
    elif tok.type == 'NEWLINE':
      if lineno % 2 != 0:
        print('\n{}.\t'.format(lineno), end='')
      else:
        print('\n\t', end='')

      lineno += 1

if __name__ == '__main__':
  main()