reserved = {
    'break' : 'BREAK',
    'continue' : 'CONTINUE',
    'float' : 'FLOAT',
    'if' : 'IF',
    'int' : 'INT',
    'return' : 'RETURN',
    'function' : 'FUNCTION',
    'while' : 'WHILE',
    'write' : 'PRINT',
    'str' : 'STRING'
}


tokens = list(reserved.values()) + [

    #OPERATORS
    'EQ_OP',
    #LITERALS
    'IDENTIFIER','STRING_LITERAL','INT_N', 'FLOAT_N'
]

literals = [';','{','}',',',':','=','(',')',
            '&','!','-','+','*','/','%','<','>','|']

t_EQ_OP = r'=='
t_INT_N = r'\d+'
t_FLOAT_N = r'\d+\.\d+'

t_ignore = " \t\v\f"

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'IDENTIFIER')    # Check for reserved words
    return t

# String literal
def t_STRING_LITERAL(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t


def t_comment(t):
    r'(/\*(.|\n)*?\*/)|(//(.)*\n)'
    t.lexer.lineno += t.value.count('\n')

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_preprocessor(t):
    r'\#(.)*?\n'
    t.lexer.lineno += 1

def t_error(t):
    print("Illegal character '%s', lineno %s" % t.value[0] , t.lexer.lineno)
    t.lexer.skip(1)

