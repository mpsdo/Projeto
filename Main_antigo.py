from sly import Lexer, Parser

class MatriculaLexer(Lexer):
    tokens = { NAME, COURSE, MATRICULAR, DESMATRICULAR, LISTAR }
    ignore = ' \t'

    # Tokens
    MATRICULAR = r'matricular'
    DESMATRICULAR = r'desmatricular'
    LISTAR = r'listar'
    NAME = r'[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ]+(\s[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ]+)*'
    COURSE = r'[A-Za-z]+[A-Za-z\d]*'


    @_(r'\n+')
    def ignore_newline(self, t):
        pass

    def error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        self.index += 1

class MatriculaParser(Parser):
    tokens = MatriculaLexer.tokens

    def __init__(self):
        self.students_courses = {}

    @_('MATRICULAR NAME COURSE')
    def matricula(self, p):
        self.matricular(p.NAME, p.COURSE)

    @_('DESMATRICULAR NAME COURSE')
    def desmatricula(self, p):
        self.desmatricular(p.NAME, p.COURSE)

    @_('LISTAR COURSE')
    def lista(self, p):
        self.listar(p.COURSE)

    def matricular(self, name, course):
        print(f"Tentando matricular: {name} no curso {course}")  # Diagnóstico
        if course not in self.students_courses:
            self.students_courses[course] = []
        if name not in self.students_courses[course]:
            self.students_courses[course].append(name)
            print(f"Aluno(a) {name} matriculado(a) no curso {course}.")
        else:
            print(f"Aluno(a) {name} já está matriculado(a) no curso {course}.")

    def desmatricular(self, name, course):
        print(f"Tentando desmatricular: {name} do curso {course}")  # Diagnóstico
        if course in self.students_courses and name in self.students_courses[course]:
            self.students_courses[course].remove(name)
            print(f"Aluno(a) {name} desmatriculado(a) do curso {course}.")
        else:
            print(f"Aluno(a) {name} não está matriculado(a) no curso {course} ou o curso não existe.")

    def listar(self, course):
        print(f"Tentando listar alunos do curso: {course}")  # Diagnóstico
        if course in self.students_courses:
            print(f"Alunos matriculados em {course}: {', '.join(self.students_courses[course])}")
        else:
            print(f"O curso {course} não tem alunos matriculados ou não existe.")

def main_loop():
    lexer = MatriculaLexer()
    parser = MatriculaParser()
    print("Digite 'sair' para finalizar o programa.")
    while True:
        try:
            text = input('Digite o comando (matricular/desmatricular/listar) > ')
            if text.lower() == 'sair':
                break
        except EOFError:
            break
        if text:
            parser.parse(lexer.tokenize(text))

if __name__ == '__main__':
    main_loop()
