// File: calculator.s
// Description: A simple calculator that adds two user-provided numbers
// Author: Ion Ionascu
// Copyright (c) 2025 Ion Ionascu
// License: MIT with Attribution (see LICENSE file)
// Target: Apple M4 Max (ARM64) - macOS Terminal
// Build: clang -o calculator calculator.s

.section __TEXT,__text,regular,pure_instructions
.globl _main
.p2align 2

.section __DATA,__data
prompt1: .asciz "Enter first number: "
prompt1_len = . - prompt1 - 1
prompt2: .asciz "Enter second number: "
prompt2_len = . - prompt2 - 1
buffer1: .space 64
buffer2: .space 64
error_msg: .asciz "Error: Invalid input\n"
error_len = . - error_msg - 1

.section __TEXT,__text,regular,pure_instructions

_main:
    stp x29, x30, [sp, #-32]!
    mov x29, sp
    stp x19, x20, [sp, #16]

    
    mov x0, #1
    adrp x1, prompt1@PAGE
    add x1, x1, prompt1@PAGEOFF
    mov x2, #prompt1_len
    bl write_call

    
    mov x0, #0
    adrp x1, buffer1@PAGE
    add x1, x1, buffer1@PAGEOFF
    mov x2, #127
    bl read_call
    
    mov x22, x0
    cmp x0, #0
    b.le error_exit

    
    adrp x1, buffer1@PAGE
    add x1, x1, buffer1@PAGEOFF
    bl parse_number
    cmp x2, #0
    b.ne error_exit
    mov x19, x0
    mov x23, x1

    
find_delimiter:
    ldrb w2, [x1], #1
    cmp w2, #'\n'
    b.eq check_second_number
    cmp w2, #' '
    b.eq check_second_number
    cmp w2, #'\t'
    b.eq check_second_number
    cmp w2, #0
    b.eq need_second_read
    sub x22, x22, #1
    cmp x22, #0
    b.gt find_delimiter
    b need_second_read

check_second_number:
    
skip_delim_ws:
    ldrb w2, [x1]
    cmp w2, #' '
    b.eq skip_delim_char
    cmp w2, #'\t'
    b.eq skip_delim_char
    b check_has_data
skip_delim_char:
    add x1, x1, #1
    b skip_delim_ws

check_has_data:
    
    ldrb w2, [x1]
    cmp w2, #0
    b.eq need_second_read
    cmp w2, #'\n'
    b.eq need_second_read
    
    b parse_second_from_buffer

need_second_read:
    
    mov x0, #1
    adrp x1, prompt2@PAGE
    add x1, x1, prompt2@PAGEOFF
    mov x2, #prompt2_len
    bl write_call
    
    
    mov x0, #0
    adrp x1, buffer2@PAGE
    add x1, x1, buffer2@PAGEOFF
    mov x2, #63
    bl read_call
    
    cmp x0, #0
    b.le error_exit

    
    adrp x1, buffer2@PAGE
    add x1, x1, buffer2@PAGEOFF
    bl parse_number
    cmp x2, #0
    b.ne error_exit
    mov x20, x0
    b done_input

parse_second_from_buffer:
    
    mov x23, x1
    mov x0, #1
    adrp x1, prompt2@PAGE
    add x1, x1, prompt2@PAGEOFF
    mov x2, #prompt2_len
    bl write_call
    
    
    mov x1, x23  // Restore buffer position
    bl parse_number
    cmp x2, #0
    b.ne error_exit
    mov x20, x0

done_input:
    
    
    add x21, x19, x20

    
    mov x0, x19
    bl print_number
    
    mov x0, #1
    adrp x1, plus_msg@PAGE
    add x1, x1, plus_msg@PAGEOFF
    mov x2, #3
    bl write_call
    
    mov x0, x20
    bl print_number
    
    mov x0, #1
    adrp x1, equals_msg@PAGE
    add x1, x1, equals_msg@PAGEOFF
    mov x2, #3
    bl write_call
    
    mov x0, x21
    bl print_number
    
    mov x0, #1
    adrp x1, newline_msg@PAGE
    add x1, x1, newline_msg@PAGEOFF
    mov x2, #1
    bl write_call

    mov x0, #0
    b exit_program

error_exit:
    mov x0, #2
    adrp x1, error_msg@PAGE
    add x1, x1, error_msg@PAGEOFF
    mov x2, #error_len
    bl write_call
    mov x0, #1

exit_program:
    ldp x19, x20, [sp, #16]
    ldp x29, x30, [sp], #32
    mov x16, #1
    orr x16, x16, #0x2000000
    svc #0

parse_number:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    
    mov x0, #0   // result
    mov x3, #10  // base
    mov x4, #0   // sign (0=positive, 1=negative)
    mov x5, #0   // digit count
    
    // Skip leading whitespace (space, tab)
skip_whitespace:
    ldrb w2, [x1]
    cmp w2, #' '
    b.eq skip_ws_char
    cmp w2, #'\t'
    b.eq skip_ws_char
    b check_sign
skip_ws_char:
    add x1, x1, #1
    b skip_whitespace
    
check_sign:
    // Check for negative
    ldrb w2, [x1]
    cmp w2, #'-'
    b.ne parse_digits
    mov x4, #1
    add x1, x1, #1
    
parse_digits:
    ldrb w2, [x1]
    cmp w2, #'0'
    b.lt check_end
    cmp w2, #'9'
    b.gt check_end
    
    sub w2, w2, #'0'
    add x5, x5, #1
    mul x0, x0, x3
    add x0, x0, x2
    add x1, x1, #1
    b parse_digits

check_end:
    cmp x5, #0
    b.eq parse_error
    
    cmp x4, #1
    b.ne parse_ok
    neg x0, x0

parse_ok:
    
    mov x2, #0
    ldp x29, x30, [sp], #16
    ret

parse_error:
    
    mov x2, #1
    ldp x29, x30, [sp], #16
    ret

print_number:
    stp x29, x30, [sp, #-32]!
    mov x29, sp
    
    mov x4, #0
    cmp x0, #0
    b.ge convert_positive
    mov x4, #1
    neg x0, x0
    
convert_positive:
    add x1, sp, #16
    add x2, sp, #31
    mov w3, #0
    strb w3, [x2]
    
    mov x3, #10
convert_loop:
    udiv x5, x0, x3
    msub x6, x5, x3, x0
    add w6, w6, #'0'
    sub x2, x2, #1
    strb w6, [x2]
    mov x0, x5
    cbnz x0, convert_loop
    
    cmp x4, #1
    b.ne print_digits
    sub x2, x2, #1
    mov w6, #'-'
    strb w6, [x2]
    
print_digits:
    mov x0, #1
    mov x1, x2
    add x3, sp, #31
    sub x2, x3, x2
    bl write_call
    
    ldp x29, x30, [sp], #32
    ret

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

.section __DATA,__data
plus_msg: .asciz " + "
equals_msg: .asciz " = "
newline_msg: .asciz "\n"