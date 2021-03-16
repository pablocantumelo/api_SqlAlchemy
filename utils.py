from models import Pessoas, Usuarios

def InserePessoas(nm):
    pessoa = Pessoas(Nome=nm,Idade=40)
    pessoa.save()

def ConsultaPessoa():
    nome = Pessoas.query.all()
    for i in nome:
        print(i.Nome)

def AlteraPessoas():
    pessoa = Pessoas.query.filter_by(Nome='Fabiana').first()
    pessoa.Idade = 29
    pessoa.save()

def ExcluiPessoas(nm):
    pessoa = Pessoas.query.filter_by(Nome=nm).first()
    print(pessoa)
    pessoa.deleta()

def InsereUsuario(login,senha):
    usuario = Usuarios(login=login, senha=senha)
    usuario.save()

def ConsultaTodosUsuarios():
    dados=Usuarios.query.all()
    print(dados)

if __name__ == '__main__':
    # InserePessoas('Pablo')
    # ConsultaPessoa()
    # AlteraPessoas()
    # ExcluiPessoas('Pablo')
    # ConsultaPessoa()
    # InclusaoColuna('atividades','status','String(10)')
    # InsereUsuario('fabi','1212')
    # ConsultaTodosUsuarios()