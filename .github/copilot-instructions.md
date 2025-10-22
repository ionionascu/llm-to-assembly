# GitHub Copilot Instructions for macOS Assembly Development

## Target Platform

- **Hardware**: MacBook Pro 16-inch (November 2024)
- **Processor**: Apple M4 Max (ARM64 architecture)
- **Operating System**: macOS
- **Execution Environment**: Terminal applications

## Assembly Language Specifications

### Architecture and ISA

- **Target Architecture**: ARM64 (AArch64)
- **Instruction Set**: ARMv8.4-A or later
- **Calling Convention**: AAPCS64 (ARM Architecture Procedure Call Standard)
- **Endianness**: Little-endian
- **Register Set**:
  - 31 general-purpose 64-bit registers (x0-x30)
  - 32 SIMD/floating-point registers (v0-v31)
  - Stack pointer (sp), program counter (pc)

### Assembly Syntax

- **Assembler**: Use GNU Assembler (gas) syntax compatible with Apple's assembler
- **File Extension**: `.s` for assembly source files
- **Directives**: Use Apple-specific directives when needed
- **Comments**: Use `//` for single-line comments, `/* */` for multi-line

### Code Structure Guidelines

#### File Header Template

```assembly
// File: [filename].s
// Description: [Brief description of the program]
// Target: Apple M4 Max (ARM64) - macOS Terminal
// Build: clang -o [output] [filename].s

.section __TEXT,__text,regular,pure_instructions
.globl _main
.p2align 2
```

#### Entry Point

- **Main function**: Always use `_main` as the entry point
- **Exit convention**: Use system call `exit(0)` or return 0 from main
- **System calls**: Use macOS system call numbers and conventions

#### Memory Sections

- **Text section**: `.section __TEXT,__text,regular,pure_instructions`
- **Data section**: `.section __DATA,__data`
- **BSS section**: `.section __DATA,__bss`

### System Interaction

#### System Calls

- Use macOS BSD-style system call interface
- System call numbers are base number ORed with 0x2000000
- System call numbers for common operations:
  - `exit`: 0x2000001 (base: 1)
  - `read`: 0x2000003 (base: 3)
  - `write`: 0x2000004 (base: 4)
  - `open`: 0x2000005 (base: 5)
  - `close`: 0x2000006 (base: 6)

Example system call wrapper:

```assembly
write_call:
    mov x16, #4
    orr x16, x16, #0x2000000
    svc #0
    ret

read_call:
    mov x16, #3
    orr x16, x16, #0x2000000
    svc #0
    ret
```

#### Terminal I/O

- **stdout**: File descriptor 1
- **stdin**: File descriptor 0
- **stderr**: File descriptor 2
- Use `write` system call for output to terminal
- Use `read` system call for input from terminal
- **Important**: Terminal input is line-buffered; `read()` may return multiple lines at once
- For sequential prompts, read all input first, then parse line-by-line
- Display prompts using `write` to stdout before reading input

Example sequential input pattern:

```assembly
// Show first prompt
mov x0, #1
adr x1, prompt1
mov x2, prompt1_len
bl write_call

// Read all input (may contain multiple lines)
mov x0, #0
adr x1, buffer
mov x2, #127
bl read_call

// Parse first line
adr x1, buffer
bl parse_number
mov x19, x0

// Find and skip to second line
// ... (find newline logic)

// Show second prompt
mov x0, #1
adr x1, prompt2
mov x2, prompt2_len
bl write_call

// Parse second line from buffer
bl parse_number
mov x20, x0
```

#### String Operations

- Null-terminated strings (C-style) for constants
- Use appropriate ARM64 string manipulation instructions
- Consider NEON instructions for optimized string operations
- For number parsing: process character-by-character using `ldrb`
- For number printing: convert integer to ASCII digits using division by 10

Example number parsing:

```assembly
parse_number:
    mov x0, #0          // result
    mov x3, #10         // base
    mov x4, #0          // sign flag

    // Check for negative sign
    ldrb w2, [x1]
    cmp w2, #'-'
    b.ne parse_digits
    mov x4, #1
    add x1, x1, #1

parse_digits:
    ldrb w2, [x1]
    cmp w2, #'0'
    b.lt done_parsing
    cmp w2, #'9'
    b.gt done_parsing

    sub w2, w2, #'0'    // Convert ASCII to digit
    mul x0, x0, x3      // result *= 10
    add x0, x0, x2      // result += digit
    add x1, x1, #1
    b parse_digits

done_parsing:
    cmp x4, #1
    b.ne positive
    neg x0, x0          // Apply negative sign
positive:
    ret
```

### Build and Execution

#### Compilation

```bash
# Basic compilation
clang -o program program.s

# With debugging symbols
clang -g -o program program.s

# Optimization levels
clang -O2 -o program program.s
```

#### Linking

- Link against system libraries when needed
- Use `-lc` for C library functions if required
- Static linking: `-static` (when applicable)

#### Execution

```bash
# Run the program
./program

# Run with arguments
./program arg1 arg2

# Debug with lldb
lldb ./program
```

### Code Patterns and Best Practices

#### Function Prologue/Epilogue

```assembly
// Function prologue
stp x29, x30, [sp, #-16]!
mov x29, sp

// Function epilogue
ldp x29, x30, [sp], #16
ret
```

#### Register Usage

- **x0-x7**: Argument/result registers
- **x8**: Indirect result location register
- **x9-x15**: Temporary registers
- **x16-x17**: Intra-procedure-call temporary registers
- **x18**: Platform register (reserved)
- **x19-x28**: Callee-saved registers
- **x29**: Frame pointer
- **x30**: Link register

#### Common Operations

- Use appropriate load/store instructions (`ldr`, `str`, `ldp`, `stp`)
- Utilize ARM64 addressing modes effectively
- Use conditional execution and branches efficiently
- Leverage NEON instructions for SIMD operations when beneficial

### Debugging and Development

#### Debugging Information

- Include `.file` and `.line` directives for debugging
- Use meaningful labels and comments
- Structure code with clear function boundaries

#### Error Handling

- Check return values from system calls
- Implement proper error reporting to stderr
- Use appropriate exit codes (0 for success, non-zero for errors)

### Performance Considerations

#### Optimization Guidelines

- Utilize ARM64-specific optimizations
- Consider instruction scheduling and pipeline effects
- Use appropriate data alignment (`.p2align` directive)
- Leverage the M4 Max's performance characteristics

#### Memory Access

- Optimize for cache locality
- Use efficient addressing modes
- Consider prefetching for large data operations

### Input Handling Best Practices

When implementing terminal input in assembly:

- **Sequential Input**: For multiple inputs, read all available input at once into a buffer
- **Line Parsing**: Parse input line-by-line by finding newline delimiters (`\n`)
- **Buffer Management**: Use separate buffers or parse from a single buffer with position tracking
- **Terminal Buffering**: Be aware that terminal input is line-buffered; `read()` may return multiple lines
- **Interactive vs Piped**: Design input handling to work with both interactive terminal use and piped input

Example pattern for two-number input:

```assembly
// Read all input at once (up to buffer size)
mov x0, #0              // stdin
adr x1, buffer          // buffer address
mov x2, #127            // buffer size
bl read_call

// Parse first number (up to newline)
adr x1, buffer
bl parse_number
mov x19, x0             // Store result

// Find newline delimiter
find_newline:
    ldrb w2, [x1], #1
    cmp w2, #'\n'
    b.eq found_newline
    b find_newline

found_newline:
// x1 now points to second line
// Parse second number
bl parse_number
mov x20, x0             // Store result
```

### Example Programs

When generating assembly code, create complete, runnable programs that:

1. Include proper headers and section declarations
2. Implement the `_main` function correctly
3. Use appropriate system calls for terminal interaction
4. Include proper error handling with meaningful error messages
5. Follow ARM64 calling conventions (AAPCS64)
6. Can be compiled and run with the specified build commands
7. Handle both interactive terminal use and piped/scripted input
8. Use proper input parsing strategies for line-based input

### Testing and Validation

#### Test Framework

- Create test cases that can be run from the terminal
- Include input/output validation
- Test edge cases and error conditions
- Verify proper memory management

#### Performance Testing

- Consider timing measurements for performance-critical code
- Use appropriate benchmarking techniques
- Profile using Instruments or other macOS profiling tools

## Additional Notes

- Always prioritize correctness over performance initially
- Write self-documenting code with clear comments
- Consider portability within the ARM64 macOS ecosystem
- Stay updated with the latest ARM64 instruction set extensions
- Use Apple's development tools and documentation as reference
