# Calculator Application

Note: This repository accompanies the Medium article ["The Return of Assembly — When LLMs No Longer Need High-Level Languages"](https://medium.com/@ionionascu/the-return-of-assembly-when-llms-no-longer-need-high-level-languages-79bc43c0822c)

**An experimental project by Ion Ionascu**

A complete calculator application written in ARM64 assembly language for macOS, specifically targeting the Apple M4 Max processor. This project demonstrates low-level systems programming concepts while providing a functional command-line calculator that prompts users to enter two numbers on separate lines and displays their sum.

> **Note**: This is an experimental educational project created to explore ARM64 assembly programming on modern Apple Silicon hardware. Use at your own discretion.

## Target Platform

- **Hardware**: MacBook Pro 16-inch (November 2024)
- **Processor**: Apple M4 Max (ARM64 architecture)
- **Operating System**: macOS
- **Execution Environment**: Terminal applications

## Features

### Core Functionality

- **Interactive Command-Line Interface**: Sequential input prompts for two numbers
- **Addition Operation**: Performs 64-bit signed integer addition
- **Input Validation**: Handles invalid input gracefully with error messages
- **Sequential Input**: Accepts two numbers on separate lines (ENTER-separated)
- **Negative Number Support**: Properly handles negative numbers and mixed signs
- **Error Handling**: Comprehensive error handling with appropriate exit codes
- **Clear, Formatted Output**: Clean "a + b = c" output format

### Technical Implementation

- **ARM64 Assembly**: Written in ARMv8.4-A assembly language with AAPCS64 calling convention
- **macOS System Calls**: Direct BSD-style system calls (read, write, exit) without C library dependencies
- **Memory Management**: Proper stack frame management and register preservation
- **String Processing**: Custom number parsing and formatting routines
- **Buffer Management**: Safe input buffer handling with proper clearing

## Project Structure

```plaintext
mac-assembly/
├── src/
│   └── calculator.s              # Main assembly source code
├── requirements/
│   └── functional-requirements.md # Detailed requirements specification
├── tests/
│   ├── test_calculator.py        # Comprehensive Python test suite (pytest)
│   ├── simple_test.py            # Simple Python test runner (no dependencies)
│   └── quick_test.sh             # Quick shell script for manual testing
├── build/                        # Build output directory (created during build)
│   └── calculator                # Compiled executable
├── .github/
│   └── copilot-instructions.md   # GitHub Copilot development guidelines
├── Makefile                      # Build automation
└── README.md                     # This file
```

## Building the Application

### Prerequisites

- macOS with Apple Silicon (M1/M2/M3/M4)
- Xcode Command Line Tools (for `clang`)
- Make utility

### Build Commands

```bash
# Build the application
make all

# Build with debug symbols
make debug

# Build with optimizations
make release

# Clean build artifacts
make clean
```

### Manual Build

If you prefer to build manually without Make:

```bash
# Create build directory
mkdir -p build

# Compile the assembly code
clang -arch arm64 -o build/calculator src/calculator.s
```

## Running the Application

### Basic Usage

```bash
# After building
./build/calculator
```

### Example Session

```text
Enter first number: 5
Enter second number: 3
5 + 3 = 8
```

### Examples

```bash
# Run directly after building
make run

# Or run the executable
./build/calculator
```

Example inputs and outputs:

```text
# Positive numbers
Enter first number: 15
Enter second number: 25
15 + 25 = 40

# Negative numbers
Enter first number: -10
Enter second number: 7
-10 + 7 = -3

# Both negative
Enter first number: -5
Enter second number: -8
-5 + -8 = -13

# With zero
Enter first number: 0
Enter second number: 42
0 + 42 = 42
```

## Testing

The application includes a comprehensive multi-level test suite to ensure correctness and reliability.

### Test Implementation

1. **Shell Script Tests** (`quick_test.sh`): Quick manual verification with colored output
2. **Python Test Suite** (`simple_test.py`): Comprehensive automated testing without external dependencies
3. **Pytest Framework** (`test_calculator.py`): Advanced testing with fixtures and detailed assertions

### Quick Testing

For quick manual testing with immediate feedback:

```bash
cd tests
./quick_test.sh
```

This runs 6 test cases covering basic operations, edge cases, and error handling.

### Automated Testing

For comprehensive automated testing:

```bash
# Simple test runner (no dependencies required)
cd tests
python3 simple_test.py

# Or using pytest (requires installation)
pip3 install pytest
cd tests
pytest test_calculator.py -v

# Or use the Makefile
make test
```

### Test Coverage

The test suite includes:

- **Basic Operations**: Positive numbers, negative numbers, zero values
- **Large Numbers**: Testing with large integers within 64-bit limits
- **Input Validation**: Invalid inputs, empty inputs, malformed data
- **User Interface**: Verification of both input prompts and output formatting
- **Performance**: Execution time validation (< 1 second)
- **Edge Cases**: Boundary conditions, single digits, whitespace handling
- **Error Handling**: Invalid input detection, error message validation

### Test Results

All tests pass successfully:

- ✅ `quick_test.sh`: 6/6 tests passing
- ✅ `simple_test.py`: 7/7 tests passing
- ✅ `test_calculator.py`: Full pytest suite passing

## Error Handling

The application handles various error conditions:

- **Invalid Input** (Exit Code 1): Non-numeric input, empty input
- **System Errors** (Exit Code 2): System call failures
- **Overflow Errors** (Exit Code 3): Integer overflow detection
- **Success** (Exit Code 0): Normal completion

## Technical Details

### Technical Architecture

#### Assembly Language Features

- **Instruction Set**: ARM64 (AArch64) ARMv8.4-A or later
- **Calling Convention**: AAPCS64 (ARM Architecture Procedure Call Standard)
- **System Interface**: Direct macOS system call interface without C library dependencies
- **Register Usage**: Follows ARM64 register conventions for arguments and preservation
  - x0-x7: Argument/result registers
  - x19-x28: Callee-saved registers (used for storing parsed numbers)
  - x29: Frame pointer
  - x30: Link register
- **Memory Management**: Proper stack frame setup/teardown with register preservation

#### Key Algorithms

1. **Number Parsing**: Custom integer parser handling signs and validation
   - Reads input character by character
   - Handles negative sign prefix
   - Converts ASCII digits to integer values
   - Validates numeric input

2. **String Conversion**: Integer-to-string conversion for output formatting
   - Divides by 10 repeatedly to extract digits
   - Handles negative numbers with sign prefix
   - Builds ASCII string in reverse order

3. **Input Processing**: Sequential two-line input handling
   - Reads all available input into buffer
   - Parses first number up to newline
   - Displays second prompt
   - Parses second number from remaining buffer
   - Works with both interactive and piped input

4. **Error Detection**: Input validation and boundary checking
   - Validates numeric characters
   - Detects empty or invalid input
   - Returns appropriate error codes

#### System Calls Used

- **read** (0x2000003): Reading user input from stdin (file descriptor 0)
- **write** (0x2000004): Writing output to stdout (fd 1) and stderr (fd 2)
- **exit** (0x2000001): Program termination with status code

#### Memory Layout

- **Text Section** (`.section __TEXT,__text,regular,pure_instructions`): Program instructions
- **Data Section** (`.section __DATA,__data`): String literals and constants
  - `prompt1`: "Enter first number: "
  - `prompt2`: "Enter second number: "
  - `error_msg`: "Error: Invalid input\n"
  - `plus_msg`, `equals_msg`, `newline_msg`: Output formatting strings
- **Buffers**: Input buffers for reading user data (127 bytes total)

## Development

### Code Quality

- **Comments**: Comprehensive inline documentation explaining functionality
- **Structure**: Clean function organization with proper separation of concerns
- **Standards**: Adherence to ARM64 assembly best practices and AAPCS64 conventions
- **Maintainability**: Clear naming conventions and modular design
- **Error Handling**: Comprehensive error detection and reporting at every level

### Debugging

To build with debug symbols:

```bash
make debug
```

Then debug with LLDB:

```bash
lldb build/calculator-debug
```

Common debugging commands:

```lldb
(lldb) breakpoint set --name _main
(lldb) run
(lldb) register read
(lldb) memory read --size 1 --format x --count 64 $x1
(lldb) step
(lldb) continue
```

### Performance

The application is designed to:

- Complete execution within 1 second under normal conditions
- Handle input responsively with immediate feedback
- Use efficient ARM64 instruction sequences
- Minimize memory allocation (uses stack for temporary storage)
- Optimize for Apple M4 Max's ARM64 architecture

### Build System

The Makefile provides multiple targets for different use cases:

- **`make all`**: Standard build (default)
- **`make debug`**: Build with debug symbols for LLDB debugging
- **`make release`**: Optimized build with -O2 flag
- **`make clean`**: Remove all build artifacts
- **`make run`**: Build and execute the calculator
- **`make test`**: Build and run the test suite

## Requirements

See `requirements/functional-requirements.md` for detailed functional and non-functional requirements.

### Key Requirements Summary

- **FR-001**: Sequential input collection with two separate prompts
- **FR-002**: Mathematical addition of two signed 64-bit integers
- **FR-003**: Formatted output display ("a + b = c")
- **FR-004**: Clear English prompts for user experience
- **NFR-001**: Performance under 1 second
- **NFR-002**: Graceful error handling for invalid input

## Educational Value

### Learning Outcomes

This project demonstrates key concepts in:

- **Low-level Programming**: Direct hardware interface programming without abstractions
- **System Programming**: Operating system interface and system call mechanisms
- **Assembly Language**: ARM64 instruction set and programming patterns
- **Memory Management**: Stack operations, register handling, and buffer management
- **Input/Output**: Character-by-character processing and string manipulation
- **Testing**: Multi-level testing strategy with different frameworks

### Technical Skills Demonstrated

- ARM64 assembly language programming on Apple Silicon
- macOS BSD-style system call interface
- Memory management and stack frame operations
- Input/output processing at the system level
- Error handling and validation in assembly
- Build system creation and automation with Make
- Comprehensive testing strategy implementation
- Technical documentation and code commenting

## Future Enhancements

### Potential Improvements

- Support for additional arithmetic operations (subtraction, multiplication, division)
- Floating-point number support using NEON/SIMD registers
- Expression parsing for complex calculations (e.g., "5 + 3 * 2")
- Command-line argument support for non-interactive mode
- Support for different number bases (binary, octal, hexadecimal)
- History and memory functions (store/recall)

### Advanced Features

- Mathematical function library (sqrt, power, trigonometric functions)
- Scientific calculator mode with advanced operations
- Scripting interface for batch calculations
- GUI frontend using macOS native frameworks
- Performance profiling and optimization

## Author

**Ion Ionascu**

This is an experimental educational project exploring ARM64 assembly programming on Apple Silicon.

## License

This project is licensed under the terms described in the [LICENSE](LICENSE) file.

**Summary**: You are free to use, modify, and distribute this code as long as:

- You attribute the original authorship to Ion Ionascu
- You include a reference to the original source

**Disclaimer**: This software is provided "as is" without any warranties. The author is not responsible for any issues, damages, or problems that may arise from using this code.

See the [LICENSE](LICENSE) file for complete terms.

## Contributing

When contributing to this project:

1. Ensure all tests pass (`make test`)
2. Follow the established code style and commenting conventions
3. Update tests for new functionality
4. Update documentation as needed
5. Follow ARM64 best practices and AAPCS64 calling conventions
6. Test on actual Apple Silicon hardware

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Ensure Xcode Command Line Tools are installed: `xcode-select --install`
   - Verify you're on Apple Silicon Mac
   - Check that clang supports ARM64

2. **Runtime Errors**
   - Verify the executable has proper permissions
   - Check that the terminal supports the expected input/output

3. **Test Failures**
   - Ensure pytest is installed: `pip3 install pytest`
   - Verify the calculator executable exists in `build/calculator`
   - Check that Python 3 is available

### Getting Help

1. Review the functional requirements document in `requirements/`
2. Check the test suite for expected behavior examples
3. Use the debug build for troubleshooting (`make debug`)
4. Run the quick test script to verify basic functionality (`./tests/quick_test.sh`)
5. Review `.github/copilot-instructions.md` for development guidelines

## Conclusion

This calculator application successfully demonstrates a complete system programming solution using ARM64 assembly language on macOS. The implementation showcases proper low-level programming practices, comprehensive testing strategies, and professional software development methodologies. The resulting application is functional, robust, and well-documented, serving both as a practical tool and an educational resource for assembly language programming on modern Apple Silicon hardware.

---

**Created by Ion Ionascu** | [License](LICENSE) | Educational Experiment | 2025
