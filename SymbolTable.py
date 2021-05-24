import sys

import ParserCompiller

root = ParserCompiller.main()
symbol_table = []
functions = []
def traverse_tree(root):
    global symbol_table
    if (type(root) != ParserCompiller.Three):
        return
    elif (root.name == 'function'):
        for j in root.children:
            if (len(j.children) == 2):
                print(j.name)
                traverse_tree_fun(j, j.name)
                functions.append(j.name)
            elif (len(j.children) == 3):
                functions.append(j.name)
                for l in j.children:
                    traverse_tree_fun(l, j.name)
    elif (root.name == 'declaration'):
        for i in root.children[0].children:
            symbol_table.append((i, root.children[1].children[0], 'global'))
        return
    else:
        for i in range(len(root.children)):
            traverse_tree(root.children[i])

def is_float(variable):
    try:
        float(variable)
        if (variable.isdigit()):
            return False
        return True
    except ValueError:
        return False

def traverse_tree_fun(root, function):
    global symbol_table
    if (type(root) != ParserCompiller.Three):
        return
    elif (root.name == 'declaration'):
        for i in root.children[0].children:
            symbol_table.append((i, root.children[1].children[0], function))
    else:
        for child in root.children:
            traverse_tree_fun(child, function)

def create_new_temps(symbol_table):
    s_temps = {}
    a_temps = {}
    count_temps = 0
    for i in range(len(symbol_table)):
        s_temps[symbol_table[i][0]] = []
        s_temps[symbol_table[i][0]]\
            .extend(['s' + str(count_temps), symbol_table[i][1], symbol_table[i][2]])
        count_temps = count_temps + 1
    count_temps = 0
    a_count = 0
    for s_temp in s_temps:
        if s_temps[s_temp][2] != 'global':
            a_temps[s_temp[0]] = []
            a_temps[s_temp[0]]\
                .extend(['a' + str(a_count), s_temps[s_temp][1], s_temps[s_temp][2]])
            a_count = a_count + 1
        else:
            a_temps[s_temp[0]] = []
            if s_temps[s_temp][1] == 'float':
                a_temps[s_temp[0]].\
                    extend(['f1' + str(count_temps), s_temps[s_temp][1], s_temps[s_temp][2]])
            else:
                a_temps[s_temp[0]]\
                    .extend(['s' + str(count_temps), s_temps[s_temp][1], s_temps[s_temp][2]])
            count_temps = count_temps + 1
    return a_temps

def check_scope(root, name):
    global symbol_table
    if name.find('if') != -1 or (root.isnumeric()) or (is_float(root)):
        return True
    elif root in symbol_table.keys():
        if(symbol_table[root][2] != name):
            print('Error : variable "%s" is not found in this scope!!!' %(root))
            return False
        else:
            return True
    else:
        print("Error : variable %s is incorrect!!!" %(root))
        return False

def print_symbol_table(symbol_table):
    for i in symbol_table:
        print(str(i) + ':\t' + "|".join(symbol_table[i]))

def main():
    global symbol_table, root
    traverse_tree(root)
    print('Symbol table is generated.................')
    symbol_table = create_new_temps(symbol_table)
    print_symbol_table(symbol_table)
    return symbol_table, root

