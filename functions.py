def neg(bits):
    return ''.join(['0' if bit == '1' else '1' for bit in bits])

def bits(ir, x, y):
    if type(ir) != str:
        return bits(leftpadded(ir), x, y)
    return ir[len(ir) - 1 - x : len(ir) - y]

def uint(bits):
    return int(bits, 2)

def sint(bits):
    if bits[0] == '1': # Si négatif, on renvoie la valeur (int(l'opposé) + 1) * -1
        return (uint(neg(bits)) + 1) * -1
    return uint(bits)

def leftpadded(value, size=32):
    if type(value) != str:
        if value < -1:
            value = bin(value+1)[3:]
            value = '1' + neg(value)
        elif value == -1:
            value = '1'
        else:
            value = bin(value)[2:]
            if len(value) < size:
                value = '0' + value
    elif len(value) < size:
        value = '0' + value
    value = value[0] * (size - len(value)) + value
    return value[len(value) - size:]

def detailed_op(ir):
    op = ir['op']
    rd = ir['rd']
    rs = ir['rs']
    rt = ir['rt']
    imm16 = sint(ir['imm16'])
    imm26 = sint(ir['imm26'])
    uimm16 = uint(ir['imm16'])
    uimm26 = uint(ir['imm26'])
    sh = uint(ir['sh'])

    if op == 'ADD':
        return 'add ${}, ${}, ${}'.format(rd, rs, rt)
    elif op == 'ADDU':
        return 'addu ${}, ${}, ${}'.format(rd, rs, rt)
    elif op == 'ADDI':
        return 'addi ${}, ${}, {}'.format(rt, rs, imm16)
    elif op == 'ADDIU':
        return 'addiu ${}, ${}, {}'.format(rt, rs, imm16)
    elif op == 'AND':
        return 'and ${}, ${}, ${}'.format(rd, rs, rt)
    elif op == 'ANDI':
        return 'andi ${}, ${}, {}'.format(rt, rs, uimm16)
    elif op == 'BEQ':
        return 'beq ${}, ${}, delta {}'.format(rs, rt, imm16)
    elif op == 'BGEZ':
        return 'bgez ${}, delta {}'.format(rs, imm16)
    elif op == 'BGEZAL':
        return 'bgezal ${}, delta {}'.format(rs, imm16)
    elif op == 'BGTZ':
        return 'bgtz ${}, delta {}'.format(rs, imm16)
    elif op == 'BLEZ':
        return 'blez ${}, delta {}'.format(rs, imm16)
    elif op == 'BLTZ':
        return 'bltz ${}, delta {}'.format(rs, imm16)
    elif op == 'BLTZAL':
        return 'bltzal ${}, delta {}'.format(rs, imm16)
    elif op == 'BNE':
        return 'bne ${}, ${}, delta {}'.format(rs, rt, imm16)
    elif op == 'BREAK':
        return 'break';
    elif op == 'DIV':
        return 'div ${}, ${}'.format(rs, rt)
    elif op == 'DIVU':
        return 'divu ${}, ${}'.format(rs, rt)
    elif op == 'ERET':
        return 'eret'
    elif op == 'J':
        return 'j delta {}'.format(imm16)
    elif op == 'JAL':
        return 'jal delta {}'.format(imm16)
    elif op == 'JALR':
        return 'jalr ${}, ${}'.format(rd, rs)
    elif op == 'JR':
        return 'jr $rs'.format(rs)
    elif op == 'LB':
        return 'lb ${}, {}(${})'.format(rt, imm16, rs)
    elif op == 'LBU':
        return 'lb ${}, {}(${})'.format(rt, uimm16, rs)
    elif op == 'LH':
        return 'lh ${}, {}(${})'.format(rt, imm16, rs)
    elif op == 'LHU':
        return 'lhu ${}, {}(${})'.format(rt, uimm16, rs)
    elif op == 'LUI':
        return 'lui ${}, {}'.format(rt, uimm16)
    elif op == 'LW':
        return 'lw ${}, {}(${})'.format(rt, imm16, rs)
    elif op == 'MFC0':
        return 'mcf0 ${}, ${}'.format(rt, rd)
    elif op == 'MFHI':
        return 'mfhi ${}, ${}'.format(rd)
    elif op == 'MFLO':
        return 'mflo ${}'.format(rd)
    elif op == 'MTC0':
        return 'mtc0 ${}, ${}'.format(rt, rd)
    elif op == 'MTHI':
        return 'mthi ${}'.format(rs)
    elif op == 'MTLO':
        return 'mtlo ${}'.format(rs)
    elif op == 'MULT':
        return 'mult ${}, ${}'.format(rs, rt)
    elif op == 'MULTU':
        return 'multu ${}, ${}'.format(rs, rt)
    elif op == 'NOR':
        return 'nor ${}, ${}, ${}'.format(rd, rs, rt)
    elif op == 'OR':
        return 'or ${}, ${}, ${}'.format(rd, rs, rt)
    elif op == 'ORI':
        return 'ori ${}, ${}, {}'.format(rt, rs, uimm16)
    elif op == 'SB':
        return 'sb ${}, {}(${})'.format(rt, imm16, rs)
    elif op == 'SH':
        return 'sh ${}, {}(${})'.format(rt, imm16, rs)
    elif op == 'SLL':
        return 'sll ${}, ${}, {}'.format(rd, rt, sh)
    elif op == 'SLLV':
        return 'sllv ${}, ${}, ${}'.format(rd, rt, rs)
    elif op == 'SLT':
        return 'slt ${}, ${}, ${}'.format(rd, rs, rt)
    elif op == 'SLTI':
        return 'slti ${}, ${}, {}'.format(rt, rs, imm16)
    elif op == 'SLTU':
        return 'sltu ${}, ${}, ${}'.format(rd, rs, rt)
    elif op == 'SLTIU':
        return 'sltiu ${}, ${}, {}'.format(rt, rs, uimm16)
    elif op == 'SRA':
        return 'sra ${}, ${}, {}'.format(rd, rt, sh)
    elif op == 'SRAV':
        return 'srav ${}, ${}, ${}'.format(rd, rt, rs)
    elif op == 'SRL':
        return 'srl ${}, ${}, {}'.format(rd, rt, sh)
    elif op == 'SRLV':
        return 'srlv ${}, ${}, ${}'.format(rd, rt, rs)
    elif op == 'SUB':
        return 'sub ${}, ${}, ${}'.format(rd, rs, rt)
    elif op == 'SUBU':
        return 'subu ${}, ${}, ${}'.format(rd, rs, rt)
    elif op == 'SW':
        return 'sw ${}, {}(${})'.format(rt, imm16, rs)
    elif op == 'SYSCALL':
        return 'syscall'
    elif op == 'XOR':
        return 'xor ${}, ${}, ${}'.format(rd, rs, rt)
    elif op == 'XORI':
        return 'xori ${}, ${}, {}'.format(rt, rs, uimm16)
    else:
        exit('Unknown op {}'.format(op))
