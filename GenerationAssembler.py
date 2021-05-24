import sys
import ThreeAddresseCodeGeneration
from SymbolTable import is_float
data = '.data' + '\n\t' + 'true: .byte 1' + '\n\t' + 'false: .byte 0\n'
text = '.text' + '\n'
is_if = False
if_count = 0
skip_count = 0
count = 0
f_bc = False
str_count = 0
three_addr_code, t_temp, symbol_table = ThreeAddresseCodeGeneration.main()

def add_temps(t_temp, symbol_table):
    global data, text

    for i in range(len(t_temp)):
        if t_temp['t' + str(i)][0].isdigit():
            t_temp['t' + str(i)] = []
            t_temp['t' + str(i)] = 'int'
            symbol_table['t' + str(i)] = []
            symbol_table['t' + str(i)] = 'int'
        elif is_float(t_temp['t' + str(i)][0]):
            t_temp['t' + str(i)] = []
            t_temp['t' + str(i)] = 'float'
            symbol_table['t' + str(i)] = []
            symbol_table['t' + str(i)] = 'float'
        elif t_temp['t' + str(i)][0] in symbol_table \
            and symbol_table[t_temp['t' + str(i)][0]][1] == 'int':
            t_temp['t' + str(i)] = []
            t_temp['t' + str(i)] = 'int'
            symbol_table['t' + str(i)] = []
            symbol_table['t' + str(i)] = 'int'
        elif t_temp['t'+str(i)][0] in symbol_table and symbol_table[t_temp['t'+str(i)][0]][1]=='float':
            t_temp['t'+str(i)]=[]
            t_temp['t' + str(i)] = 'float'
            symbol_table['t' + str(i)] = []
            symbol_table['t' + str(i)] = 'float'
        else:
            t_temp['t' + str(i)] = []
            t_temp['t' + str(i)] = 'int'
            symbol_table['t' + str(i)] = []
            symbol_table['t' + str(i)] = 'int'
        for symbol in (symbol_table):
            if symbol == ('t0'):
                break
            t_temp[symbol] = []
            t_temp[symbol].append(symbol)

def generate_MIPS_assembler(t_temp,three_addr_code, symbol_table):
    global data, text
    for label in three_addr_code:
        if label == 'global':
            text = text + 'main:' + '\n'
        else:
            text = text + label + ':' + '\n'
        for instruction in three_addr_code[label]:
            instruct = instruction.split(' ')
            operand = instruct[0]
            if (operand == 'assigment~'):
                generate_assigment_code(instruct[1], instruct[2], symbol_table, t_temp)
            elif (operand == '*'):
                generate_mult_code(instruct[1], instruct[2], symbol_table, t_temp, instruct)
            elif (operand == '/'):
                generate_div_code(instruct[1], instruct[2], symbol_table, t_temp, instruct)
            elif (operand == '+'):
                generate_add_code(instruct[1], instruct[2], symbol_table, t_temp, instruct)
            elif (operand == '-'):
                generate_sub_code(instruct[1], instruct[2], symbol_table, t_temp, instruct)
            elif (operand == '<' or operand == '>' or operand == '=='):
                generate_logical_code(operand,instruct[1], instruct[2],symbol_table, instruct)
            elif (operand == '&' or operand[0] == '|'):
                generate_and_or_code(operand, instruct[1], instruct[2], instruct)
            elif(operand == '!'):
                generate_not_code(instruct[1], instruct[2])
            elif(operand == 'jump'):
                generate_if_code(instruct[1], instruct[2], instruct)
            elif(operand == 'goto'):
                generate_goto_code(instruct[1])
            elif(operand == 'break'):
                generate_break()
            elif (operand == 'continue'):
                generate_continue()
            elif (operand == 'write'):
                genereate_print_code(instruct[1], symbol_table)
            elif(operand == 'return'):
                generate_return(instruct[1])
            elif (operand == 'call'):
                generate_call_function(instruct[1], instruct, symbol_table)


def generate_mult_code(arg1, arg2, symbol_table, t_temp, instruct):
    global text, data
    if not (is_float(arg1) or is_float(arg2)):
        if (arg1.isnumeric() or symbol_table[arg1][1] == 'int' or t_temp[arg1][0] == 'i') and (
                arg2.isnumeric() or symbol_table[arg2][1] == 'int' or t_temp[arg2][0] == 'i'):
            if arg1.isnumeric():
                text = text +'\tli $t0, ' + arg1 + '\n'
                arg1_ = '$t0'
                if arg2.isnumeric():
                    text = text +'\tli $t1, ' + arg2 + '\n'
                    arg2_ = '$t1'
                    text = text +'\tmult ' + arg1_ + ', ' + arg2_ + '\n'
                elif (arg2 in symbol_table and symbol_table[arg2][1] == 'int'):
                    arg2_ = '$' + symbol_table[arg2][0]
                    text = text +'\tmult ' + arg1_ + ', ' + arg2_ + '\n'
                elif (t_temp[arg2][0] == 'i'):
                    arg2_ = '$' + arg2
                    text = text +'\tmult ' + arg1_ + ', ' + arg2_ + '\n'
            elif ((arg1 in symbol_table and symbol_table[arg1][1] == 'int') or (
                    t_temp[arg1][0] == 'i' and arg1 in t_temp)):
                if (arg1 in symbol_table and symbol_table[arg1][1] == 'int'):
                    arg1_ = '$' + symbol_table[arg1][0]
                else:
                    arg1_ = '$' + arg1
                if arg2.isnumeric():
                    text = text +'\tli $t1, ' + arg2 + '\n'
                    arg2_ = '$t1'
                    text = text +'\tmult ' + arg1_ + ', ' + arg2_ + '\n'
                elif (arg2 in symbol_table and symbol_table[arg2][1] == 'int'):

                    arg2_ = '$' + symbol_table[arg2][0]
                    text = text +'\tmult ' + arg1_ + ', ' + arg2_ + '\n'
                elif (t_temp[arg2][0] == 'i' and arg2 in t_temp):
                    arg2_ = '$' + arg2
                    print(1)
                    text = text +'\tmult ' + arg1_ + ', ' + arg2_ + '\n'
                text = text +'\tmflo $' + instruct[3] + '\n'
        elif ((arg1 in symbol_table and symbol_table[arg1][1] == 'float') or (
                t_temp[arg1][0] == 'f' and arg1 in t_temp)):
            if (arg1 in symbol_table and symbol_table[arg1][1] == 'float'):
                arg1_ = '$' + symbol_table[arg1][0]
            else:
                ar = arg1[1:]
                arg1_ = '$f' + str(ar)
            if is_float(arg2):
                text = text +'\tli.s $f1, ' + arg2 + '\n'
                arg2_ = '$f1'
                text = text +'\tmul.s $f' + instruct[3][1:] + ', ' + arg1_ + ', ' + arg2_ + '\n'
            elif (arg2 in symbol_table and symbol_table[arg2][1] == 'float'):
                arg2_ = '$' + symbol_table[arg2][0]
                ar = instruct[3][1:]

                text = text +'\tmul.s $f' + str(ar) + ', ' + arg1_ + ', ' + arg2_ + '\n'
            elif (t_temp[arg2][0] == 'f' and arg2 in t_temp):
                ar = arg2[1:]
                arg2_ = '$f' + str(ar)
                text = text +'\tmul.s $f' + instruct[3][1:] + ', ' + arg1_ + ', ' + arg2_ + '\n'
            else:
                print('error неверный тип')
                return
    elif is_float(arg1):
        text = text +'\tli.s $f0, ' + arg1 + '\n'
        arg1_ = '$f0'
        if is_float(arg2):
            text = text +'\tli.s $f1, ' + arg2 + '\n'
            arg2_ = '$f1'
            text = text +'\tmul.s $f' + instruct[3][1:] + ', ' + arg1_ + ', ' + arg2_ + '\n'
        elif (arg2 in symbol_table and symbol_table[arg2][1] == 'float'):
            arg2_ = '$' + symbol_table[arg2][0]
            text = text +'\tmul.s $f' + instruct[3][1:] + ', ' + arg1_ + ', ' + arg2_ + '\n'
        elif (t_temp[arg2][0] == 'f' and arg2 in t_temp):
            ar = arg2[1:]
            arg2_ = '$f' + str(ar)
            text = text +'\tmul.s $f' + instruct[3][1:] + ', ' + arg1_ + ', ' + arg2_ + '\n'
        else:
            print('Ошибка! Введены неверные типы')
            return

def generate_assigment_code(arg1, arg2, symbol_table, t_temp):
    global text, data
    if arg1.isnumeric() and (symbol_table[arg2][1] == 'int' or t_temp[arg2][0] == 'i'):
        if (arg2 in t_temp.keys() and t_temp[arg2][0] != arg2):
            text = text + '\tli $' + arg2 + ', ' + arg1 + '\n'
        else:
            text = text + '\tli $' + symbol_table[arg2][0] + ', ' + arg1 + '\n'
    elif (is_float(arg1) and (symbol_table[arg2][1] == 'float' or t_temp[arg2][0] == 'f')):
        data = data + '\tdrob' + arg1 + ': .float ' + arg1 + '\n'
        if (arg2 in t_temp.keys() and t_temp[arg2][0] != arg2):
            text = text + '\tla $' + arg2 + ', drob' + arg1 + '\n'
        else:
            text = text + '\tli.s $' + symbol_table[arg2][0] + ', ' + arg1 + '\n'
    elif arg1.startswith('\"') and arg1.endswith('\"') and (symbol_table[arg2][1] == 'str'):
        data = data + '\t' + arg2 + ': .asciiz ' + arg1 + '\n'

    elif (arg1 in symbol_table.keys()):
        if (arg1 in t_temp.keys() and t_temp[arg1][0] != arg1):
            if (arg2 in t_temp.keys() and t_temp[arg2][0] != arg2):
                if t_temp[arg1][0] == 'f':

                    text = text + '\tmov.s $f' + arg2[1:] + ', $f' + arg1[1:] + '\n'
                else:
                    text = text + '\tmove $' + arg2 + ', $f' + arg1 + '\n'
            elif arg2 in symbol_table.keys():
                if t_temp[arg1][0] == 'f':

                    text = text + '\tmov.s $' + symbol_table[arg2][0] + ', $f' + arg1[1:] + '\n'
                else:
                    text = text + '\tmove $' + symbol_table[arg2][0] + ', $' + arg1 + '\n'
        elif (arg1 in symbol_table.keys()):
            if (arg2 in symbol_table.keys()):
                if symbol_table[arg2][1] == 'float':
                    text = text + '\tmov.s $' + symbol_table[arg2][0] + ', $' + symbol_table[arg1][0] + '\n'
                else:
                    text = text + '\tmove $' + symbol_table[arg2][0] + ', $' + symbol_table[arg1][0] + '\n'
    else:
        if (arg2 in symbol_table.keys()):
            text = text + '\tmove $' + arg2 + ', $' + arg1 + '\n'
        elif (arg2 in symbol_table.keys()):
            text = text + '\tmove $' + symbol_table[arg2][0] + ', $' + arg1 + '\n'
        else:
            text = text + '\tmove $' + arg2 + ', $' + arg1 + '\n'


def generate_div_code(arg1, arg2, symbol_table, t_temp, instruct):
    global text
    if not (is_float(arg1) or is_float(arg2)):
        if (arg1.isnumeric() or symbol_table[arg1][1] == 'int' or t_temp[arg1][0] == 'i') and (
                arg2.isnumeric() or symbol_table[arg2][1] == 'int' or t_temp[arg1][0] == 'i'):
            if arg1.isnumeric():
                text = text + '\tli $t0, ' + arg1 + '\n'
                arg1_ = '$t0'
                if arg2.isnumeric():
                    text = text + '\tli $t1, ' + arg2 + '\n'
                    arg2 = '$t1'
                    text = text + '\tdiv ' + arg1 + ', ' + arg2 + '\n'
                elif (arg2 in symbol_table and symbol_table[arg2][1] == 'int'):
                    arg2 = '$' + symbol_table[arg2][0]
                    text = text + '\tdiv ' + arg1 + ', ' + arg2 + '\n'
                elif (t_temp[arg2][0] == 'i'):
                    arg2 = '$' + arg2
                    text = text + '\tdiv ' + arg1 + ', ' + arg2 + '\n'
            elif ((arg1 in symbol_table and symbol_table[arg1][1] == 'int') or (
                    t_temp[arg1][0] == 'i' and arg1 in t_temp)):
                if (arg1 in symbol_table and symbol_table[arg1][1] == 'int'):
                    arg1 = '$' + symbol_table[arg1][0]
                else:
                    arg1 = '$' + arg1
                if arg2.isnumeric():
                    text = text + '\tli $t1, ' + arg2 + '\n'
                    text = text + '\tdiv ' + arg1 + ', ' + '$t1' + '\n'
                elif (arg2 in symbol_table and symbol_table[arg2][1] == 'int'):
                    arg2 = '$' + symbol_table[arg2][0]
                    text = text + '\tdiv ' + arg1 + ', ' + arg2 + '\n'
                elif (t_temp[arg2][0] == 'i' and arg2 in t_temp):
                    arg2 = '$' + arg2
                    text = text + '\tdiv ' + arg1 + ', ' + arg2 + '\n'
            text = text + '\tmflo $' + instruct[3] + '\n'
        elif ((arg1 in symbol_table and symbol_table[arg1][1] == 'float') or (
                t_temp[arg1][0] == 'f' and arg1 in t_temp)):
            if (arg1 in symbol_table and symbol_table[arg1][1] == 'float'):
                arg1_ = '$' + symbol_table[arg1][0]
            else:
                arg1_ = '$f' + str(arg1[1:])
            if is_float(arg2):
                text = text + '\tli.s $f1, ' + arg2 + '\n'
                arg2_ = '$f1'
                text = text + '\tdiv.s $f' + instruct[3][1:] + ', ' + arg1_ + ', ' + arg2_ + '\n'
            elif (arg2 in symbol_table and symbol_table[arg2][1] == 'float'):
                arg2_ = '$' + symbol_table[arg2][0]
                text = text + '\tdiv.s $f' + instruct[3][1:] + ', ' + arg1_ + ', ' + arg2_ + '\n'
            elif (t_temp[arg2][0] == 'f' and arg2 in t_temp):
                arg2_ = '$f' + arg2[1:]
                text = text + '\tdiv.s $f' + instruct[3][1:] + ', ' + arg1_ + ', ' + arg2_ + '\n'

        else:
            print('Error! Неверный тип!')
            return

def generate_add_code(arg1, arg2, symbol_table, t_temp, instruct):
    global text
    if not (is_float(arg1) or is_float(arg2)):
        if (arg1.isnumeric() or symbol_table[arg1][1] == 'int' or t_temp[arg1][0] == 'i') and (
                arg2.isnumeric() or symbol_table[arg2][1] == 'int' or t_temp[arg2][0] == 'i'):
            if arg1.isnumeric():
                text = text +'\tli $t0, ' + arg1 + '\n'
                arg1_ = '$t0'
                if arg2.isnumeric():
                    text = text +'\tli $t1, ' + arg2 + '\n'
                    arg2_ = '$t1'
                    text = text +'\taddu $' + instruct[3] + ', ' + arg1_ + ', ' + arg2_ + '\n'
                elif (arg2 in symbol_table and symbol_table[arg2][1] == 'int'):
                    arg2_ = '$' + symbol_table[arg2][0]
                    text = text +'\taddu $' + instruct[3] + ', ' + arg1_ + ', ' + arg2_ + '\n'
                elif (t_temp[arg2][0] == 'i'):
                    arg2_ = '$' + arg2
                    text = text +'\taddu $' + instruct[3] + ', ' + arg1_ + ', ' + arg2_ + '\n'
            elif ((arg1 in symbol_table and symbol_table[arg1][1] == 'int') or (
                    t_temp[arg1][0] == 'i' and arg1 in t_temp)):
                if (arg1 in symbol_table and symbol_table[arg1][1] == 'int'):
                    arg1_ = '$' + symbol_table[arg1][0]
                else:
                    arg1_ = '$' + arg1
                if arg2.isnumeric():
                    text = text +'\tli $t1, ' + arg2 + '\n'
                    arg2_ = '$t1'
                    text = text +'\taddu $' + instruct[3] + ', ' + arg1_ + ', ' + arg2_ + '\n'
                elif (arg2 in symbol_table and symbol_table[arg2][1] == 'int'):
                    arg2_ = '$' + symbol_table[arg2][0]
                    text = text +'\taddu $' + instruct[3] + ', ' + arg1_ + ', ' + arg2_ + '\n'
                elif (t_temp[arg2][0] == 'i' and arg2 in t_temp):
                    arg2_ = '$' + arg2
                    text = text +'\taddu $' + instruct[3] + ', ' + arg1_ + ', ' + arg2_ + '\n'
        elif ((arg1 in symbol_table and symbol_table[arg1][1] == 'float') or (
                t_temp[arg1][0] == 'f' and arg1 in t_temp)):
            if (arg1 in symbol_table and symbol_table[arg1][1] == 'float'):
                arg1_ = '$' + symbol_table[arg1][0]
            else:
                arg1_ = '$f' + arg1[1:]
            if is_float(arg2):
                text = text +'\tli.s $f1, ' + arg2 + '\n'
                arg2_ = '$f1'
                text = text +'\tadd.s $f' + instruct[3][1:] + ', ' + arg1_ + ', ' + arg2_ + '\n'
            elif (arg2 in symbol_table and symbol_table[arg2][1] == 'float'):
                arg2_ = '$' + symbol_table[arg2][0]
                text = text +'\tadd.s $f' + instruct[3][1:] + ', ' + arg1_ + ', ' + arg2_ + '\n'
            elif (t_temp[arg2][0] == 'f' and arg2 in t_temp):
                arg2_ = '$f' + arg2[1:]
                text = text +'\tadd.s $f' + instruct[3][1:] + ', ' + arg1_ + ', ' + arg2_ + '\n'
        else:
            print('error неверный тип')
            return
    elif is_float(arg1):

        text = text +'\tli.s $f0, ' + arg1 + '\n'
        arg1_ = '$f0'
        if is_float(arg2):
            text = text +'\tli.s $f1, ' + arg2 + '\n'
            arg2 = '$f1'
            text = text +'\tadd.s $f' + instruct[3][1:] + ', ' + arg1_ + ', ' + arg2 + '\n'
        elif ((arg2 in symbol_table and symbol_table[arg2][1] == 'float') or (
                t_temp[arg1][0] == 'f' and arg1 in t_temp)):
            if (arg2 in symbol_table and symbol_table[arg2][1] == 'float'):
                arg2 = '$' + symbol_table[arg2][0]
            elif (t_temp[arg1][0] == 'f' and arg1 in t_temp):
                arg2 = '$' + arg2
            text = text +'\tadd.s $f' + instruct[3][1:] + ', ' + arg1_ + ', ' + arg2 + '\n'
        else:
            print('error неверный тип')
            return
    else:
        print('error неверный тип')
        return

def generate_sub_code(arg1, arg2, symbol_table, t_temp, instruct):
    global text
    if not (is_float(arg1) or is_float(arg2)):
        if (arg1.isnumeric() or symbol_table[arg1][1] == 'int' or t_temp[arg1][0] == 'i') and (
                arg2.isnumeric() or symbol_table[arg2][1] == 'int' or t_temp[arg1][0] == 'i'):
            if arg1.isnumeric():
                text = text  +'\tli $t0, ' + arg1 + '\n'
                arg1_ = '$t0'
                if arg2.isnumeric():
                    text = text  +'\tli $t1, ' + arg2 + '\n'
                    arg2 = '$t1'
                    text = text  +'\tsubu $' + instruct[3] + ', ' + arg1_ + ', ' + arg2 + '\n'
                elif (arg2 in symbol_table and symbol_table[arg2][1] == 'int'):
                    arg2 = '$' + symbol_table[arg2][0]
                    text = text  +'\tsubu $' + instruct[3] + ', ' + arg1_ + ', ' + arg2 + '\n'
                elif (t_temp[arg2][0] == 'i'):
                    arg2 = '$' + arg2
                    text = text  +'\tsubu $' + instruct[3] + ', ' + arg1_ + ', ' + arg2 + '\n'
            elif ((arg1 in symbol_table and symbol_table[arg1][1] == 'int') or (
                    t_temp[arg1][0] == 'i' and arg1 in t_temp)):
                if (arg1 in symbol_table and symbol_table[arg1][1] == 'int'):
                    arg1_ = '$' + symbol_table[arg1][0]
                else:
                    arg1_ = '$' + arg1
                if arg2.isnumeric():
                    text = text  +'\tli $t1, ' + arg2 + '\n'
                    arg2 = '$t1'
                    text = text  +'\tsubu $' + instruct[3] + ', ' + arg1_ + ', ' + arg2 + '\n'
                elif (arg2 in symbol_table and symbol_table[arg2][1] == 'int'):
                    arg2 = '$' + symbol_table[arg2][0]
                    text = text  +'\tsubu $' + instruct[3] + ', ' + arg1_ + ', ' + arg2 + '\n'
                elif (t_temp[arg2][0] == 'i' and arg2 in t_temp):
                    arg2 = '$' + arg2
                    text = text  +'\tsubu $' + instruct[3] + ', ' + arg1_ + ', ' + arg2 + '\n'
        elif ((arg1 in symbol_table and symbol_table[arg1][1] == 'float') or (
                t_temp[arg1][0] == 'f' and arg1 in t_temp)):
            if (arg1 in symbol_table and symbol_table[arg1][1] == 'float'):
                arg1_ = '$' + symbol_table[arg1][0]
            else:
                arg1_ = '$f' + arg1[1:]
            if is_float(arg2):
                text = text  +'\tli.s $f1, ' + arg2 + '\n'
                arg2 = '$f1'
                text = text  +'\tsub.s $f' + instruct[3][1:] + ', ' + arg1_ + ', ' + arg2 + '\n'
            elif (arg2 in symbol_table and symbol_table[arg2][1] == 'float'):
                arg2 = '$' + symbol_table[arg2][0]
                text = text  +'\tsub.s $f' + instruct[3][1:] + ', ' + arg1_ + ', ' + arg2 + '\n'
            elif (t_temp[arg2][0] == 'f' and arg2 in t_temp):
                arg2 = '$f' + arg2[1:]
                text = text  +'\tsub.s $f' + instruct[3][1:] + ', ' + arg1_ + ', ' + arg2 + '\n'
        else:
            print('error неверный тип')
            return
    elif is_float(arg1):
        text = text  +'\tli.s $f0, ' + arg1 + '\n'
        arg1_ = '$f0'
        if is_float(arg2):
            text = text  +'\tli.s $f1, ' + arg2 + '\n'
            arg2 = '$f1'
            text = text  +'\tsub.s $f' + instruct[3][1:] + ', ' + arg1_ + ', ' + arg2 + '\n'
        elif ((arg2 in symbol_table and symbol_table[arg2][1] == 'float') or (
                t_temp[arg2][0] == 'f' and arg2 in t_temp)):
            if (arg1 in symbol_table and symbol_table[arg1][1] == 'float'):
                arg2 = '$' + symbol_table[arg2][0]
            else:
                arg2 = '$f' + arg2[1:]
            text = text  +'\tsub.s $' + instruct[3][1:] + ', ' + arg1_ + ', ' + arg2 + '\n'
        else:
            print('error неверный тип')
            return
    else:
        print('error неверный тип')
        return

def generate_and_or_code(operand, arg1, arg2, instruct):
    global text
    text = text + '\t' + operand + ' $' + instruct[3] + ', $' + arg1 + ', $' + arg2 + '\n'

def generate_not_code(arg1, arg2):
    global index, text
    index = arg2[1:]
    index = int(index) + 1
    temp = 't' + str(index)
    text = text + '\tla $' + temp + ' false\n'
    text = text + '\tnor $' + arg2 + ', $' + arg1 + ', $' + temp + '\n'
def generate_logical_code(operand,arg1, arg2,symbol_table, instruct):
    global is_if, if_count, skip_count, text
    if is_if == False:
        L = 'L' + str(if_count)
        if_count = if_count + 1
        is_if = True
        text =text + L + ':\n'
    if operand == '<':
        text =text +'\tla $' + instruct[3] + ', false\n'
        text =text + '\tbge $' + symbol_table[arg1][0] + ', $' + symbol_table[arg2][0] + ', jump_' + str(skip_count) + '\n'
        text =text +'\tla $' + instruct[3] + ', true\n'
        text =text +'jump_' + str(skip_count) + ':\n'
        skip_count = skip_count + 1
    elif operand == '>':
        text =text +'\tla $' + instruct[3] + ', false\n'
        text =text + '\tble $' + symbol_table[arg1][0] + ', $' + symbol_table[arg2][0] + ', jump_' + str(skip_count) + '\n'
        text =text +'\tla $' + instruct[3] + ', true\n'
        text =text +'jump_' + str(skip_count) + ':\n'
        skip_count = skip_count + 1
    elif operand == '==':
        text =text +'\tla $' + instruct[3] + ', false\n'
        text =text + '\tbne $' + symbol_table[arg1][0] + ', $' + symbol_table[arg2][0] + ', jump_' + str(skip_count) + '\n'
        text =text +'\tla $' + instruct[3] + ', true\n'
        text =text +'jump_' + str(skip_count) + ':\n'
        skip_count = skip_count + 1

def generate_if_code(arg1, arg2, instruct):
    global text, if_count, is_if
    is_if = False
    index = arg1[1:]
    index = int(index) + 1
    temp = 't' + str(index)
    text = text + '\tla $' + temp + ', true\n'
    text = text + '\tbeq $' + temp + ', $' + arg1 + ', ' + instruct[3] + '\n'
    text = text + 'L' + str(if_count) + ':\n'
    if_count = if_count + 1
def generate_return(arg1):
    global text
    text = text + '\tmove $t9, $' + arg1 + '\n'
    text = text + '\tjr $ra\n'
def generate_goto_code(arg1):
    global if_count, text, f_bc
    if (arg1 == 'end'):
        if f_bc == False:
            text = text + '\tj L' + str(if_count - 1) + '\n'
    elif (arg1 == 'start'):
        text = text +'\tj L' + str(if_count - 2) + '\n'
    else:
        text = text +'\tj ' + arg1 + '\n'
def generate_break():
    global f_bc, if_count, text
    text = text + '\tj L' + str(if_count - 3) + '\n'
    f_bc = True

def generate_continue():
    global text, f_bc
    text = text + '\tj L' + str(if_count - 4) + '\n'
    f_bc = True

def generate_call_function(arg1,instruct, symbol_table):
    global text
    function_args = instruct[2:len(instruct) - 1]
    for i in range(len(function_args)):
        text = text + '\tmove $a' + str(i) + ', $' + symbol_table[function_args[i]][0] + '\n'
    text = text + '\tjal ' + arg1 + '\n'
    text = text + '\tmove $' + instruct[len(instruct)-1] + ', $t9\n'

def genereate_print_code(arg1, symbol_table):
    global data, text, str_count
    if (arg1.startswith('\"') and arg1.endswith('\"')):
        data = data + '\tstr' + str(str_count) + ': .asciiz ' + arg1 + '\n'
        str_count = str_count + 1
        text = text + '\tli $v0, 4\n'
        text = text + '\tla $a0, ' + 'str' + str(str_count - 1) + '\n'
        text = text + '\tsyscall\n'
    elif (arg1 in symbol_table and symbol_table[arg1][1] == 'str'):
        text = text + '\tli $v0, 4\n'
        text = text + '\tla $a0, ' + arg1 + '\n'
        text = text + '\tsyscall\n'
    elif (arg1.isnumeric()):
        text = text + '\tli $v0, 1\n'
        text = text + '\tla $a0, ' + arg1 + '\n'
        text = text + '\tsyscall\n'
        if data.find('strinr_w') == -1:
            data = data + '\tstrinr_w' + r': .asciiz "\n"' + '\n'
        text = text + '\tli $v0, 4\n'
        text = text + '\tla $a0, ' + 'strinr_w' + '\n'
        text = text + '\tsyscall\n'
    elif (is_float(arg1)):
        data = data + '\tdrob' + arg1 + ': .float ' + arg1 + '\n'
        text = text + '\tli $v0, 2\n'
        text = text + '\tlvc1 $f14, drob' + arg1 + '\n'
        text = text + '\tsyscall\n'
    elif (arg1 in symbol_table and symbol_table[arg1][1] == 'int'):
        text = text + '\tli $v0, 1\n'
        text = text + '\tla $a0, ' + '($' + symbol_table[arg1][0] + ')\n'
        text = text + '\tsyscall\n'
        if data.find('strinr_w') == -1:
            data = data + '\tstrinr_w' + r': .asciiz "\n"' + " " + '\n'
        text = text + '\tli $v0, 4\n'
        text = text + '\tla $a0, ' + 'strinr_w' + '\n'
        text = text + '\tsyscall\n'
    elif (arg1 in symbol_table and symbol_table[arg1][1] == 'float'):
        text = text + '\tli $v0, 2\n'
        text = text + '\tmov.s $f12, $' + symbol_table[arg1][0] + '\n'
        text = text + '\tsyscall\n'

def main():
    global text, data, t_temp, symbol_table, three_addr_code
    if len(sys.argv) >= 3:
        code_file = sys.argv[1]
        out_file = sys.argv[2]
        add_temps(t_temp,symbol_table)
        generate_MIPS_assembler(t_temp, three_addr_code, symbol_table)
        print('Generation complete........')
        out = open(out_file, 'w')
        text = text + 'end_:\n'
        out.write(text + data)
        out.close()

if __name__ == '__main__':
    main()