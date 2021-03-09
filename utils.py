from models import Pessoas

def InserePessoas(nm):
    pessoa = Pessoas(Nome=nm,Idade=40)
    pessoa.save()

def ConsultaPessoa():
    nome = Pessoas.query.all()
    for i in nome:
        print(i.Nome)

    # nome = Pessoas.query.filter_by(Nome='Fabiana')
    # for p in nome:
    #     print(p.Nome)
    # res = Pessoas.query.filter_by(Nome='Fabiana').first()
    # print(res.Idade)

def AlteraPessoas():
    pessoa = Pessoas.query.filter_by(Nome='Fabiana').first()
    pessoa.Idade = 29
    pessoa.save()

def ExcluiPessoas(nm):
    pessoa = Pessoas.query.filter_by(Nome=nm).first()
    print(pessoa)
    pessoa.deleta()


if __name__ == '__main__':
    InserePessoas('Pablo')
    ConsultaPessoa()
    AlteraPessoas()
    ExcluiPessoas('Pablo')
    ConsultaPessoa()