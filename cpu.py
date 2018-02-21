from functions import *

class CPU:
    def __init__(self, memory):
        self.memory = memory
        # Special registers
        self.pc = 0
        self.lo = 0
        self.hi = 0
        self.epc = 0x0
        self.sr = 1
        self.bar = 0x0
        self.cr = 0
        # General usage registers
        self.registers = ['00000000' * 4] * 32

    def do(self, ir):

        def reg(register, value=None, signed=False):
            if value is None:
                if signed:
                    return sint(self.registers[ir[register]])
                return uint(self.registers[ir[register]])
            if register == 0:
                exit('Can\'t write to register $0 (const 0)')
            self.registers[ir[register]] = leftpadded(value)

        def rt(value=None, signed=False):
            return reg('rt', value, signed)

        def rs(value=None, signed=False):
            return reg('rs', value, signed)

        def rd(value=None, signed=False):
            return reg('rd', value, signed)

        def mem(address, value=None):
            if value is None:
                return self.memory.get(address)
            self.memory.set(address, leftpadded(value))

        # Raccourcis
        op = ir['op']
        imm16 = ir['imm16']
        imm26 = ir['imm26']

        if op == 'ADD':
            rd(rs() + rt())
        elif op == 'ADDU':
            rd(rs(signed=True) + rt(signed=True))
        elif op == 'ADDI':
            rt(uint(imm16) + rs())
        elif op == 'ADDIU':
            rt(sint(imm16) + rs(signed=True))
        elif op == 'AND':
            rd(rt() & rs())
        elif op == 'ANDI':
            rt(uint(imm16) & rs())
        elif op == 'BEQ':
            if rs() == rt():
                self.pc += sint(imm16) << 2
        elif op == 'BGEZ':
            if rs(signed=True) >= 0:
                self.pc += sint(imm16) << 2
        elif op == 'BGEZAL':
            reg(31, self.pc)
            if rs(signed=True) >= 0:
                self.pc += sint(imm16) << 2
        elif op == 'BGTZ':
            if rs(signed=True) > 0:
                self.pc += sint(imm16) << 2
        elif op == 'BLEZ':
            if rs(signed=True) <= 0:
                self.pc += sint(imm16) << 2
        elif op == 'BLTZ':
            if rs(signed=True) < 0:
                self.pc += sint(imm16) << 2
        elif op == 'BLTZAL':
            reg(31, self.pc)
            if rs(signed=True) < 0:
                self.pc += sint(imm16) << 2
        elif op == 'BNE':
            if rs() != rt():
                self.pc += sint(imm16) << 2
        elif op == 'BREAK':
            self.pc = 0x00000080
        elif op == 'DIV':
            self.lo = rs(signed=True) // rt(signed=True)
            self.hi = rs(signed=True) % rt(signed=True)
        elif op == 'DIVU':
            self.lo = rs() // rt()
            self.hi = rs() % rt()
        elif op == 'ERET':
            self.pc = self.epc
            self.sr = bits(self.sr, 31, 1) + '0'
        elif op == 'J':
            self.pc = uint(bits(self.pc, 31, 28) + imm16 + '00')
        elif op == 'JAL':
            reg(31, self.pc)
            self.pc = uint(bits(self.pc, 31, 28) + imm16 + '00')
        elif op == 'JALR':
            rd(self.pc)
            self.pc = rs()
        elif op == 'JR':
            self.pc = rs()
        elif op == 'LB':
            rt(sint(bits(sint(mem(imm16)) + rs(signed=True), 24, 7)))
        elif op == 'LBU':
            rt(uint(bits(sint(mem(imm16)) + rs(), 24, 7)))
        elif op == 'LH':
            rt(sint(mem(imm16) + rs(signed=True)))
        elif op == 'LHU':
            rt(uint(mem(imm16) + rs()))
        elif op == 'LUI':
            rt(uint(imm16) << 16)
        elif op == 'LW':
            rt(mem(uint(imm16) + rs(signed=True)))
        elif op == 'MFC0':
            if ir['rd'] == 8:
                rt(self.bar)
            elif ir['rd'] == 12:
                rt(self.sr)
            elif ir['rd'] == 13:
                rt(self.cr)
            elif ir['rd'] == 14:
                rt(self.epc)
            else:
                exit('Unknown special register {}'.format(ir['rd']))
        elif op == 'MFHI':
            rd(self.hi)
        elif op == 'MFLO':
            rd(self.lo)
        elif op == 'MTC0':
            if ir['rd'] == 8:
                self.bar = rt()
            elif ir['rd'] == 12:
                self.sr = rt()
            elif ir['rd'] == 13:
                self.cr = rt()
            elif ir['rd'] == 14:
                self.epc = rt()
            else:
                exit('Unknown special register {}'.format(ir['rd']))
        elif op == 'MTHI':
            self.hi = rs()
        elif op == 'MTLO':
            self.lo = rs()
        elif op == 'MULT':
            self.lo = bits(leftpadded(rs(signed=True) * rt(signed=True), 64), 31, 0)
            self.hi = bits(leftpadded(rs(signed=True) * rt(signed=True), 64), 63, 32)
        elif op == 'MULTU':
            self.lo = bits(leftpadded(rs() * rt(), 64), 31, 0)
            self.hi = bits(leftpadded(rs() * rt(), 64), 63, 32)
        elif op == 'NOR':
            rd(neg(rs() | rt()))
        elif op == 'OR':
            rd(rs() | rt())
        elif op == 'ORI':
            rt(uint(imm16) | rs())
        elif op == 'SB':
            mem(sint(imm16) + rs(signed=True), bits(rt(), 7, 0))
        elif op == 'SH':
            mem(sint(imm16) + rs(signed=True), bits(rt(), 15, 0))
        elif op == 'SLL':
            rd(bits(rt(), 31 - uint(ir['sh']), 0) + '0' * uint(ir['sh']))
        elif op == 'SLLV':
            rd(bits(rt(), 31 - uint(bits(rs(), 4, 0)), 0) + '0' * uint(bits(rs(), 4, 0)))
        elif op == 'SLT':
            rd(1 if rs(signed=True) < rt(signed=True) else 0)
        elif op == 'SLTI':
            rd(1 if rs(signed=True) < sint(imm16) else 0)
        elif op == 'SLTU':
            rd(1 if rs() < rt() else 0)
        elif op == 'SLTIU':
            rd(1 if rs() < uint(imm16) else 0)
        elif op == 'SRA':
            rd(bits(rt(), 31, 31) * uint(ir['sh']) + bits(rt(), 31, uint(ir['sh'])))
        elif op == 'SRAV':
            rd(bits(rt(), 31, 31) * uint(bits(rs(), 4, 0)) + bits(rt(), 31, uint(bits(rs(), 4, 0))))
        elif op == 'SRL':
            rd('0' * uint(ir['sh']) + bits(rt(), 31, uint(ir['sh'])))
        elif op == 'SRLV':
            rd('0' * unit(bits(rs(), 4, 0)) + bits(rt(), 31, unit(bits(rs(), 4, 0))))
        elif op == 'SUB':
            rd(rs(signed=True) - rt(signed=True))
        elif op == 'SUBU':
            rd(rs() - rt())
        elif op == 'SW':
            mem(sint(imm16) + rs(signed=True), rt())
        elif op == 'SYSCALL':
            self.pc = 0x00000080
        elif op == 'XOR':
            rd(rs() ^ rt())
        elif op == 'XORI':
            rd(uint(imm16) ^ rs())
        else:
            exit('Unknown op {}'.format(op))
