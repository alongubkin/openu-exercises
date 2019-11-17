OBJS	= main.o parser.o lexer.o
OUT	= tree
CC	 = gcc
FLAGS	 = -g -c -Wall
LFLAGS	 =

all: $(OBJS) 
	$(CC) -g $(OBJS) -o $(OUT) $(LFLAGS)

lexer.c: tokens.l
	flex -o $@ $<

parser.c: grammar.y
	bison --defines=tokens.h -v -o $@ $<

main.o: main.c
	$(CC) $(FLAGS) main.c

parser.o: parser.c
	$(CC) $(FLAGS) parser.c

lexer.o: lexer.c
	$(CC) $(FLAGS) lexer.c

clean:
	rm -f *.o *.output $(OUT) lexer.c parser.c tokens.h