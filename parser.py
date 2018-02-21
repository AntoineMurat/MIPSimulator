def bits(ir, x, y):
    return ir[31 - x : 32 - y]

op_names = dict()
op_names['000000'] = 'special'
op_names['000001'] = 'regimm'
op_names['000010'] = 'J'
op_names['000011'] = 'JAL'
op_names['000100'] = 'BEQ'
op_names['000101'] = 'BNE'
op_names['000110'] = 'BLEZ'
op_names['000111'] = 'BGTZ'
op_names['001000'] = 'ADDI'
op_names['001001'] = 'ADDIU'
op_names['001010'] = 'SLTI'
op_names['001011'] = 'SLTIU'
op_names['001100'] = 'ANDI'
op_names['001101'] = 'ORI'
op_names['001110'] = 'XORI'
op_names['001111'] = 'LUI'
op_names['010000'] = 'cop0'
op_names['100000'] = 'LB'
op_names['100001'] = 'LH'
op_names['100011'] = 'LW'
op_names['100100'] = 'LBU'
op_names['100101'] = 'LHU'
op_names['101000'] = 'SB'
op_names['101001'] = 'SH'
op_names['101011'] = 'SW'

func_names = dict()
func_names['000000'] = 'SLL'
func_names['000010'] = 'SRL'
func_names['000011'] = 'SRA'
func_names['000100'] = 'SLLV'
func_names['000110'] = 'SRLV'
func_names['000111'] = 'SRAV'
func_names['001000'] = 'JA'
func_names['001001'] = 'JALR'
func_names['001100'] = 'SYSCALL'
func_names['001101'] = 'BREAK'
func_names['010000'] = 'MHFI'
func_names['010001'] = 'MTHI'
func_names['010010'] = 'MFLO'
func_names['010011'] = 'MTLO'
func_names['011000'] = 'MULT'
func_names['011001'] = 'MULTU'
func_names['011010'] = 'DIV'
func_names['011011'] = 'DIVU'
func_names['100000'] = 'ADD'
func_names['100001'] = 'ADDU'
func_names['100010'] = 'SUB'
func_names['100011'] = 'SUBU'
func_names['100100'] = 'AND'
func_names['100101'] = 'OR'
func_names['100110'] = 'XOR'
func_names['100111'] = 'NOR'
func_names['101010'] = 'SLT'
func_names['101011'] = 'SLTU'

regimm_names = dict()
regimm_names['00000'] = 'BLTZ'
regimm_names['00001'] = 'BGEZ'
regimm_names['10000'] = 'BLTZAL'
regimm_names['10001'] = 'BGEZAL'

class Parser:
    def __init__(self, memory, cpu):
        self.memory = memory
        self.cpu = cpu
        self.cpu.pc = 0

    def set_pc(self, address):
        self.cpu.pc = address

    def get_pc(self):
        return self.cpu.pc

    def increment_pc(self):
        self.cpu.pc += 4

    def current_instruction(self):
        return self.memory.get(self.cpu.pc)

    def analysed(self, ir):
        to_return = dict()
        to_return['opcode'] = bits(ir, 31, 26)
        to_return['rs'] = int(bits(ir, 25, 21), 2)
        to_return['rt'] = int(bits(ir, 20, 16), 2)
        to_return['rd'] = int(bits(ir, 15, 11), 2)
        to_return['sh'] = bits(ir, 10, 6)
        to_return['func'] = bits(ir, 5, 0)
        to_return['imm16'] = bits(ir, 15, 0)
        to_return['imm26'] = bits(ir, 25, 0)
        to_return['op'] = op_names[to_return['opcode']]
        if to_return['op'] == 'special':
            to_return['op'] = func_names[to_return['func']]
        elif to_return['op'] == 'regimm':
            to_return['op'] = regimm_names[bits(ir, 20, 16)]
        return to_return

    def instructions(self):
        while True:
            new_ir = self.current_instruction()
            self.increment_pc()
            yield self.analysed(new_ir)
