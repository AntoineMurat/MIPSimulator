# MIPSimulator

A basic MIPS emulator written in Python

# Dependencies

Written and tested with Python 3.5 on GNU/Linux.

Requires pygame (pip3 install pygame).

# What's in?

This project aims to implement the instructions [described here (Ensimag CPU conception class, 2nd semester)](docs/Ensimag_CEP_cdc_resume.pdf) and more precisely [here](docs/Ensimag_CEP_cdc.pdf).

Currently implemented instruction set:

- op: J, JAL, BEQ, BNE, BLEZ, BGTZ, ADDI, ADDIU, SLTI, SLTIU, ANDI, ORI, XORI, LUI, cop0, LB, LH, LW, LBU, LHU, SB, SH, SW

- special: SLL, SRL, SRA, SLLV, SRLV, SRAV, JA, JALR, SYSCALL, BREAK, MHFI, MTHI, MFLO, MTLO, MULT, MULTU, DIV, DIVU, ADD, ADDU, SUB, SUBU, AND, OR, XOR, NOR, SLT, SLTU

- regimm: BLTZ, BGEZ, BLTZAL, BGEZAL

You can load any memory dump in the emulator memory and then run the simulation (PC will start at 0).

The simulator displays the content of the VRAM (0x80000-0xCAFFF) on a virtual monitor (320 x 240, 16 bits, 5R 6G 5B).

It also displays the content of 0x4000 as 32 LEDs (green is 'on', red is 'off') and you can interact with the content of 0x4004 by pushing the buttons at the bottom of the window (green is 'on', red is 'off'). The content of those addresses is not refreshed until the next CPU instruction!

# What's not in?

Right now the memory loader doesn't let you specify where to write the dumps, lines are loaded sequentially one after the other (starting at 0x0).

Also, this project doesn't include an ASM to MIPS machine code translator.

You can use [this nice (but incomplete) tool instead](http://www.kurtm.net/mipsasm/) (don't forget to remove the limitations under the "Advanced Options" tab).

# How to use it?
**Your memory dumps must be written in ASCII/UTF8** either:

- in binary, one byte a line.
- in hexadecimal, 4 bytes a line (no prefix).

Any line with less than 8 characters will be ignored and line with more than 8 will be truncated. A line starting with a *#* will also be ignored.

Then, run your program with `./mipsimulate PATH/TO/YOUR/PROGRAM -v -w -s -x`

**Arguments:**

- *-v*: Display the current registers state and the instruction to come after each instruction.
- *-w*: You will be asked to press 'Enter' after each instruction.
- *-s*: Enable the virtual screen.
- *-x*: Load machine code written in hex.
