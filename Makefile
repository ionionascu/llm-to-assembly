# Makefile for Calculator Application
# Target: Apple M4 Max (ARM64) - macOS

# Compiler and flags
CC = clang
CFLAGS = -arch arm64
DEBUG_FLAGS = -g
OPTIMIZE_FLAGS = -O2

# Directories
SRC_DIR = src
BUILD_DIR = build
TEST_DIR = tests

# Source files
ASM_SRC = $(SRC_DIR)/calculator.s
TARGET = $(BUILD_DIR)/calculator

# Default target
all: $(TARGET)

# Create build directory if it doesn't exist
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

# Build the calculator
$(TARGET): $(ASM_SRC) | $(BUILD_DIR)
	$(CC) $(CFLAGS) -o $@ $<

# Build with debug symbols
debug: $(ASM_SRC) | $(BUILD_DIR)
	$(CC) $(CFLAGS) $(DEBUG_FLAGS) -o $(BUILD_DIR)/calculator-debug $<

# Build with optimization
release: $(ASM_SRC) | $(BUILD_DIR)
	$(CC) $(CFLAGS) $(OPTIMIZE_FLAGS) -o $(TARGET) $<

# Clean build artifacts
clean:
	rm -rf $(BUILD_DIR)

# Run the application
run: $(TARGET)
	./$(TARGET)

# Run tests
test: $(TARGET)
	cd $(TEST_DIR) && python3 test_calculator.py

# Install dependencies for testing (requires pip)
test-deps:
	pip3 install pytest

# Help target
help:
	@echo "Available targets:"
	@echo "  all       - Build the calculator (default)"
	@echo "  debug     - Build with debug symbols"
	@echo "  release   - Build with optimizations"
	@echo "  clean     - Remove build artifacts"
	@echo "  run       - Build and run the calculator"
	@echo "  test      - Run the test suite"
	@echo "  test-deps - Install testing dependencies"
	@echo "  help      - Show this help message"

.PHONY: all debug release clean run test test-deps help