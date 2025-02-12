# Compiler
CXX = g++

# Compiler Flags
CXXFLAGS = -Wall -Wextra -O0 -std=c++17

# Target executable
TARGET = main

# Source files
SRCS = main.cpp

# Object files
OBJS = $(SRCS:.cpp=.o)

# Default target (compile)
all: $(TARGET)

# Compile the executable
$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJS)

# Compile C++ files into object files
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Clean build files
clean:
	rm -f $(TARGET) $(OBJS)

# Run the program
run: all
	./$(TARGET)
