from functions import *

class Logger:
    def __init__(self, memory, parser, cpu):
        self.memory = memory
        self.parser = parser
        self.cpu = cpu

    def log(self):
        print('IR: {}'.format(self.parser.current_instruction()))
        print('Decoded: ' + detailed_op(self.parser.analysed(self.parser.current_instruction())))
        print('PC: {}'.format(self.parser.get_pc()))
        for register, value in enumerate(self.cpu.registers):
            print('REG[{}]{}: {} ({})'.format(register, ' ' if register < 10 else '', value, hex(uint(value))))
        print('LEDs: {}'.format(self.memory.get(0x4000)))
        print('Buttons: {}'.format(self.memory.get(0x4004)))
