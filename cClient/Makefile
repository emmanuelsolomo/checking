CC=gcc
CFLAGS=-I.
LIBS=-lcurl
OBJ = nslog.c



%.o: %.c
	$(CC) -c -o $@ $< $(CFLAGS) $(LIBS)

nsloger: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(LIBS)
