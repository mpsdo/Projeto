import ply.lex as lex
import ply.yacc as yacc

# -----------------------------------------------------------------------------
# Lexer
# -----------------------------------------------------------------------------
tokens = (
    'NAME', 'COMMAND', 'COURSECODE'
)

t_COMMAND = r'(matricular|listar|desmatricular)'
t_COURSECODE = r'([a-zA-Z]{3}\d{2}|\d{2}[a-zA-Z]{3})'
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# -----------------------------------------------------------------------------
# Parser
# -----------------------------------------------------------------------------
def p_statement_matricular(p):
    'statement : COMMAND NAME COURSECODE'
    if p[1] == 'matricular':
        if p[3] not in students:
            students[p[3]] = p[2]
            print(f"Matriculado(a) {p[2]} com código {p[3]}.")
        else:
            print(f"Erro: Código {p[3]} já está em uso.")

def p_statement_listar(p):
    'statement : COMMAND'
    if p[1] == 'listar':
        if students:
            print("Alunos matriculados:")
            for code, name in students.items():
                print(f"{name} - {code}")
        else:
            print("Não há alunos matriculados no momento.")

def p_statement_desmatricular(p):
    'statement : COMMAND NAME'
    if p[1] == 'desmatricular':
        # Encontrar o aluno pelo nome e remover sua matrícula
        to_remove = None
        for code, name in students.items():
            if name == p[2]:
                to_remove = code
                break
        if to_remove:
            del students[to_remove]
            print(f"Desmatriculado(a) {p[2]}.")
        else:
            print(f"Erro: Aluno(a) {p[2]} não encontrado.")

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

# -----------------------------------------------------------------------------
# Main program
# -----------------------------------------------------------------------------
students = {}  # Dicionário para armazenar os alunos

if __name__ == '__main__':
    while True:
        try:
            s = input('> ')
            if s.lower() == 'sair':
                break
            lexer.input(s)
            while True:
                tok = lexer.token()
                if not tok:
                    break
                print(tok)
        except EOFError:
            break
        if s:
            parser.parse(s)
