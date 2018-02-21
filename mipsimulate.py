#!/usr/bin/env python3
import sys
from memory import Memory
from parser import Parser
from cpu import CPU
from MIPSio import IO
from logger import Logger

def main():
    if len(sys.argv) < 2:
        return print('Usage: ./main memory_file [-x (hex)] [-w (wait)] -s [(screen) [-v (verbose)]')

    memory = Memory()
    if '-x' in sys.argv:
        memory.load_hex(sys.argv[1])
    else:
        memory.load(sys.argv[1])
    cpu = CPU(memory)
    parser = Parser(memory, cpu)
    io = IO(memory)
    logger = Logger(memory, parser, cpu)
    if '-v' in sys.argv:
        logger.log()
    for instruction in parser.instructions():
        if '-w' in sys.argv:
            input('next -> press enter')
        cpu.do(instruction)
        io.display(screen='-s' in sys.argv)
        if '-v' in sys.argv:
            logger.log()

main()
