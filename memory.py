from functions import *

def no_comment(lines):
    for line in lines:
        line = line.replace('\n', '')
        if len(line) >= 8 and line[0] != '#':
            yield line[:8]

class Memory:
    def __init__(self, last_address=0xCAFFF):
        self.content = ['00000000'] * (last_address + 3) # 4 bytes à la dernière adresse
        self.updated_VRAM = None

    def pop_updated_VRAM(self):
        buffered = self.updated_VRAM
        self.updated_VRAM = None
        return buffered

    def load(self, filename):
        with open(filename, 'r') as memory_file:
            for line, value in enumerate(no_comment(memory_file)):
                self.content[line] = value

    def load_hex(self, filename):
        with open(filename, 'r') as memory_file:
            for line, value in enumerate(no_comment(memory_file)):
                self.content[line * 4] = leftpadded(int(value[0:2], 16), 8)
                self.content[line * 4 + 1] = leftpadded(int(value[2:4], 16), 8)
                self.content[line * 4 + 2] = leftpadded(int(value[4:6], 16), 8)
                self.content[line * 4 + 3] = leftpadded(int(value[6:8], 16), 8)

    def get(self, address):
        if address % 4 != 0 :
            exit('Address not aligned {}'.format(hex(address)))

        return self.content[address] \
            + self.content[address + 1] \
            + self.content[address + 2] \
            + self.content[address + 3]

    def set(self, address, value):
        value = leftpadded(value)
        self.content[address] = value[0:8]
        self.content[address + 1] = value[8:16]
        self.content[address + 2] = value[16:24]
        self.content[address + 3] = value[24:32]
        # Optimisation for VRAM
        if address > 0x80000:
            self.updated_VRAM = address
