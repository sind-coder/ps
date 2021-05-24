import SymbolTable
import ParserCompiller

symbol_table, root = SymbolTable.main()
three_addr_code = {'global': []}
counter = 0
if_while_counter = 0
t_temps = {}

class T_temp():
    def __init__(self, count):
        self.count = count
    def __repr__(self):
        return 't' + str(self.count)


def three_code_generation(root, name):
    global counter, if_while_counter, counter
    if(type(root) != ParserCompiller.Three):
        if root in {'break', 'continue'}:
            three_addr_code[name].append(root)
        else:
            return
    elif (root.name == 'decdeclaration'):
        for i in root.children[0].children:
            three_addr_code[name].append('declaration~ ' + i)
    elif(root.name == 'equals'):
        if (type(root.children[0]) == str and type(root.children[1]) == str):
            if (not SymbolTable.check_scope(root.children[0], name)):
                return
            three_addr_code[name].append(\
                'assigment~ ' + root.children[1] + ' ' + root.children[0])
        else:
            tree_addr_code_for_assigment(root, name)
            if (not SymbolTable.check_scope(root.children[0], name)):
                return
            three_addr_code[name].append( \
                'assigment~ ' + str(T_temp(counter - 1)) + ' ' + root.children[0])
            t_temps[str(T_temp(counter - 1))] = []
            t_temps[str(T_temp(counter - 1))].append(root.children[0])
            counter = 0
    elif (root.name == 'if'):
        logical_expression(root.children[0], name)
        label = 'if_label_' + str(if_while_counter)
        if_while_counter = if_while_counter + 1
        three_addr_code[label] = []
        three_addr_code[name].append('jump '  + str(T_temp(counter - 1)) + ' goto ' + label)
        three_code_generation(root.children[1], label)
        three_addr_code[label].append('goto end')
    elif(root.name == 'while'):
        logical_expression(root.children[0], name)
        label = 'if_label_' + str(if_while_counter)
        if_while_counter = if_while_counter + 1
        three_addr_code[label] = []
        if counter == 0:
            counter = counter + 1
        three_addr_code[name].append('jump ' + str(T_temp(counter - 1)) + ' goto ' + label)
        three_code_generation(root.children[1], label)
        three_addr_code[label].append('goto start')
    elif(root.name == 'return'):
        tree_addr_code_for_assigment(root.children[0], name)
        three_addr_code[name].append('return ' + str(T_temp(counter - 1)))
    elif (root.name == 'write'):
        three_addr_code[name].append('write ' + root.children[0])
    else:
        for i in range(len(root.children)):
            three_code_generation(root.children[i], name)

def logical_expression(root, name):
    global counter
    if(type(root) != ParserCompiller.Three):
        if (not SymbolTable.check_scope(root, name)):
            return
        return root
    elif (root.name == '&' or root.name == '|'):
        operand = root.name
        arg1 = logical_expression(root.children[0], name)
        arg2 = logical_expression(root.children[1], name)
        if arg1 == None and arg2 == None:
            arg1 = str(T_temp(counter - 2))
            t_temps[str(T_temp(counter - 2))].append(str(T_temp(counter - 1)))
            t_temps[str(T_temp(counter - 2))].append(str(T_temp(counter - 2)))
        if arg1 == None:
            arg1 = str(T_temp(counter - 1))
            t_temps[str(T_temp(counter - 1))].append(arg2)
        if arg2 == None:
            arg2 = str(T_temp(counter - 1))
            t_temps[str(T_temp(counter - 1))].append(arg1)
        temp = str(T_temp(counter))
        if not(temp in t_temps):
            t_temps[temp]=[]
            t_temps[str(T_temp(counter))].append(arg1)
        counter = counter + 1
    elif (root.name == '!'):
        operand = root.name
        logical_expression(root.children[0], name)
        arg = str(T_temp(counter - 1))
        temp = str(T_temp(counter))
        counter = counter + 1
        three_addr_code[name].append(str(operand) + ' ' + str(arg) + ' ' + str(temp))
    elif (root.name == '>' or root.name == '<' or root.name == '=='):
        operand = root.name
        arg1 = tree_addr_code_for_assigment(root.children[0], name)
        arg2 = tree_addr_code_for_assigment(root.children[1], name)
        temp = str(T_temp(counter))
        t_temps[temp] = []
        t_temps[temp].append(arg1)
        counter = counter + 1
        three_addr_code[name].append(str(operand) + ' ' + str(arg1) + ' ' + str(arg2) + ' ' + str(temp))
    else:
        for i in range(len(root.children)):
            logical_expression(root.children[i], name)

def tree_addr_code_for_assigment(root, name):
    global counter
    if type(root) != ParserCompiller.Three:
        if (not SymbolTable.check_scope(root, name)):
            return
        return root
    elif (root.name == '*' or root.name == '/' or root.name == '+' or root.name == '-'):
        operand = root.name
        arg1 = tree_addr_code_for_assigment(root.children[0], name)
        arg2 = tree_addr_code_for_assigment(root.children[1], name)
        if arg1 == None and arg2 == None:
            arg1 = str(T_temp(counter - 2))
            t_temps[str(T_temp(counter - 2))].append(str(T_temp(counter - 1)))
            t_temps[str(T_temp(counter - 2))].append(str(T_temp(counter - 2)))
        if arg1 == None:
            arg1 = str(T_temp(counter - 1))
            t_temps[str(T_temp(counter - 1))].append(arg2)
        if arg2 == None:
            arg2 = str(T_temp(counter - 1))
            t_temps[str(T_temp(counter - 1))].append(arg1)
        temp = str(T_temp(counter))
        counter = counter + 1
        three_addr_code[name].append(str(operand) + ' ' + str(arg1) + ' ' + str(arg2) + ' ' + str(temp))
    elif (root.name in SymbolTable.functions):
        string = 'call ' + root.name + ' '
        for arg in root.children[0].children:
            string = string + arg + ' '
        temp = 't' + str(counter)
        counter = counter + 1
        string = string + temp
        three_addr_code[name].append(string)
    else:
        for i in range(len(root.children)):
            tree_addr_code_for_assigment(root.children[i], name)

def traverse_three(root):
    if (len(root.children) != 1):
        three_code_generation(root.children[1].children[0], 'global')
        three_code_generation(root.children[1].children[1], 'global')
        for function in root.children[0].children:
            three_addr_code[function.name] = []
            three_code_generation(function, function.name)
    else:
        three_code_generation(root.children[0].children[0], 'global')
        three_code_generation(root.children[0].children[1], 'global')
    three_addr_code['global'].append("goto end_")

def main():
    global root, three_addr_code, symbol_table
    print('Generate Three Address Code ............')
    traverse_three(root)
    for key in three_addr_code:
        print(key + ' : ')
        for i in three_addr_code[key]:
            print('\t' + str(i))
    return three_addr_code, t_temps, symbol_table
if __name__ == '__main__':
    main()