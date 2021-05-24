import sys
from LexerCompiller import *
import ply.lex as lex
import ply.yacc as yacc
import AST

def lexer():
    lex.lex()

class Three(AST.Three):
    pass

def p_start(p):
    '''start : body_programm
             | function_declaration_list body_programm'''
    if len(p) == 2:
        p[0] = Three('Start Programm', [p[1]])
    else:
        p[0] = Three('Start Programm', [p[1], p[2]])
def p_function_declaration_list(p):
    '''function_declaration_list : function
                                 | function_declaration_list function'''
    if len(p) == 2:
        p[0] = Three('function', [p[1]])
    else:
        p[0] = p[1].add_children([p[2]])
def p_body_programm(p):
    '''body_programm : identifier_list compound_statement'''
    p[0] = Three('Body', [p[1], p[2]])
def p_identifier_list(p):
    '''identifier_list : identifier
                       | identifier_list ';' identifier'''
    if len(p) == 2:
        p[0] = Three('variables', [p[1]])
    else:
        p[0] = p[1].add_children([p[3]])
def p_identifier(p):
    '''identifier : type declaration_list'''
    p[0] = Three('declaration', [p[2], p[1]])

def p_type_1(p):
    '''type : INT'''
    p[0] = Three('type', [p[1]])

def p_type_2(p):
    '''type : FLOAT'''
    p[0] = Three('type', [p[1]])

def p_type_3(p):
    '''type : STRING'''
    p[0] = Three('type', [p[1]])

def p_declaration_list(p):
    '''declaration_list : IDENTIFIER
                        | declaration_list ',' IDENTIFIER '''
    if len(p) == 2:
        p[0] = Three('identifier', [p[1]])
    else:
        p[0] = p[1].add_children([p[3]])

def p_function(p):
    '''function : FUNCTION IDENTIFIER '(' identifier_list ')' '{' function_statement_list '}'
                | FUNCTION IDENTIFIER '(' identifier_list ')' '{' identifier_list function_statement_list '}'
                 '''
    if len(p) == 9:
        p[0] = Three(p[2], [p[4], p[7]])
    else:
        p[0] = Three(p[2], [p[4], p[8], p[9]])
def p_function_calling(p):
    '''function_calling : IDENTIFIER '(' arguments ')' '''
    p[0] = Three(p[1], [p[3]])
def p_arguments(p):
    '''arguments : argument
                 | arguments ',' argument'''
    if len(p) == 2:
        p[0] = Three('args', [p[1]])
    else:
        p[0] = p[1].add_children([p[3]])
def p_argument_1(p):
    '''argument : IDENTIFIER'''
    p[0] = p[1]
def p_argument_2(p):
    '''argument : INT_N'''
    p[0] = p[1]
def p_argument_3(p):
    '''argument : FLOAT_N'''
    p[0] = p[1]
def p_argument_4(p):
    '''argument : '(' expression ')' '''
    p[0] = p[2]
def p_compound_statement(p):
    '''compound_statement : '{' statement_list '}' '''
    p[0] = p[2]
def p_statement_list(p):
    '''statement_list : statement
                      | statement_list ';' statement'''
    if len(p) == 2:
        p[0] = Three('stmt', [p[1]])
    else:
        p[0] = p[1].add_children([p[3]])
def p_statement(p):
    '''statement : assigment_statement
                 | print_statement
                 | while_statement
                 | if_statement'''
    p[0] = p[1]
def p_statement_list_if(p):
    '''statement_list_if : statement_if
                         | statement_list_if ';' statement_if'''
    if len(p) == 2:
        p[0] = Three('stmt', [p[1]])
    else:
        p[0] = p[1].add_children([p[3]])
def p_statement_if(p):
    '''statement_if : if_statement
                    | assigment_statement
                    | print_statement
                    | while_statement
                    | CONTINUE
                    | BREAK'''
    p[0] = p[1]
def p_function_statement_list(p):
    '''function_statement_list : function_statement
                               | function_statement_list ';' function_statement'''
    if len(p) == 2:
        p[0] = Three('stmt', [p[1]])
    else:
        p[0] = p[1].add_children([p[3]])
def p_function_statement(p):
    '''function_statement : if_statement
                          | assigment_statement
                          | print_statement
                          | while_statement
                          | return_statement'''
    p[0] = p[1]
def p_return_statement(p):
    '''return_statement : RETURN expression'''
    p[0] = Three(p[1], [p[2]])
def p_assigment_statement(p):
    '''assigment_statement : IDENTIFIER '=' expression
                           | IDENTIFIER '=' STRING_LITERAL'''
    p[0] = Three('equals', [p[1], p[3]])
def p_expression(p):
    '''expression : multiplication
                  | expression  '+' multiplication
                  | expression  '-' multiplication'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Three(p[2], [p[1], p[3]])
def p_multiplication(p):
    '''multiplication : item
                      | multiplication '*' item
                      | multiplication '/' item '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Three(p[2], [p[1], p[3]])
def p_item(p):
    '''item : function_calling
            | IDENTIFIER
            | INT_N
            | FLOAT_N
            | '(' expression ')' '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]
def p_print_statement(p):
    '''print_statement : PRINT '(' expression ')'
                       | PRINT '(' STRING_LITERAL ')' '''
    p[0] = Three('write', [p[3]])
def p_if_statement(p):
    '''if_statement : IF logical_expression '{' statement_list_if '}' '''
    p[0] = Three('if', [p[2], p[4]])
def p_while_statement(p):
    '''while_statement : WHILE logical_expression '{' statement_list '}' '''
    p[0] = Three('while', [p[2], p[4]])
def p_logical_expression(p):
    '''logical_expression : logical_or_expression
                          | '!' logical_or_expression'''
    if len(p) == 3:
        p[0] = Three(p[1], [p[2]])
    else:
        p[0] = p[1]
def p_logical_or_expression(p):
    '''logical_or_expression : logical_and_expression
                             | logical_or_expression '|' logical_and_expression
                          '''
    if len(p) == 4:
        p[0] = Three(p[2], [p[1], p[3]])
    else:
        p[0] = p[1]
def p_logical_and_expression(p):
    '''logical_and_expression : logical_and_expression '&' boolean
                              | boolean'''
    if len(p) == 4:
        p[0] = Three(p[2], [p[1], p[3]])
    else:
        p[0] = p[1]
def p_boolean(p):
    '''boolean : '(' expression EQ_OP expression ')'
               | '(' expression '>' expression ')'
               | '(' expression '<' expression ')'  '''
    p[0] = Three(p[3], [p[2], p[4]])

def p_error(p):
    print ('Unexpected token:', p)

def main():
    lexer()
    if len(sys.argv) >= 2:
        code_file = sys.argv[1]
        parser = yacc.yacc(start='start')
        with open(code_file, 'r') as myfile:
            code = myfile.read()
        print('File read complete........')
        three = parser.parse(code)
        print('Parsed successfully.......')
        print('Three generation...........')
        print(three)
        return three
    else:
        yacc.yacc(start='start')
        yacc.parse('')
        print('Please provide file to be parsed')
if __name__ == '__main__':
  main()