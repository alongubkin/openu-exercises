OBJS	= parser.o
SOURCE	= parser.c
HEADER	= 
OUT	= parser
CC	 = gcc
FLAGS	 = -g -c -Wall
LFLAGS	 = 

all: $(OBJS)
	$(CC) -g $(OBJS) -o $(OUT) $(LFLAGS)

parser.o: parser.c
	$(CC) $(FLAGS) parser.c 


clean:
	rm -f $(OBJS) $(OUT)