ifeq ($(OS),Windows_NT)
SHELL = cmd
endif

CC= g++

CFLAGS= -Wl,--enable-auto-import

LIBS = -lchilkat-9.5.0 -lcrypt32 -lws2_32 -ldnsapi

SOURCEDIR = src

SOURCES = $(wildcard $(SOURCEDIR)/*.cc)

BUILDDIR = bin

ifeq ($(OS),Windows_NT)
	EXECUTABLE = main.exe
else
	EXECUTABLE = main
endif

OBJECTS = $(patsubst $(SOURCEDIR)/%.cc,$(BUILDDIR)/%.o,$(SOURCES))

all: dir $(BUILDDIR)/$(EXECUTABLE)

ifeq ($(OS),Windows_NT)
dir:
else
dir:
		mkdir -p $(BUILDDIR)
endif

$(BUILDDIR)/$(EXECUTABLE): $(OBJECTS)
	$(CC) -o $@ $^ $(LIBS)

$(OBJECTS): $(BUILDDIR)/%.o : $(SOURCEDIR)/%.cc
	$(CC) -o $@ -c $< $(CFLAGS)

ifeq ($(OS),Windows_NT)

.PHONY: cls

clean:
		RMDIR /S $(BUILDDIR)/*o $(BUILDDIR)/$(EXECUTABLE)
else

.PHONY: clean

clean:
		rm -f $(BUILDDIR)/*o $(BUILDDIR)/$(EXECUTABLE)
endif