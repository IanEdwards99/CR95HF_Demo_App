CFLAGS=-g -fPIC -I.
CC=g++
prefix=/usr
#LDFLAGS=-lCR95HF -lusb-1.0
LDFLAGS=-lusb-1.0

all: libCR95HF.so TestApp

TestApp: TestApp.cpp
	$(CC) TestApp.cpp -o TestApp $(LDFLAGS) -lCR95HF

libCR95HF.so: HIDManager.o libcr95hf.o
	$(CC) -shared -o libCR95HF.so libcr95hf.o HIDManager.o $(LDFLAGS)

libcr95hf.o: libcr95hf.cpp libcr95hf.h
	$(CC) -c libcr95hf.cpp $(CFLAGS)

HIDManager.o: HIDManager.cpp HIDManager.h
	$(CC) -c HIDManager.cpp $(CFLAGS)

install: libCR95HF.so
	install -m 644 libCR95HF.so $(prefix)/lib/libCR95HF.so
.PHONY: all clean install

clean:
	rm -f libCR95HF.so libcr95hf.o HIDManager.o TestApp
