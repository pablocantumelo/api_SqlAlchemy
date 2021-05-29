from flask import Flask,request
from flask_restful import Resource, Api
from models import Pessoas,Atividades,Usuarios
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

app = Flask(__name__)

api = Api(app)


# user = {'pablo':'123','cantu':'999'}
# @auth.verify_password
# def verificacao(login,senha):
#     print(user.get(login) == senha)
#     if not (login,senha):
#         return False
#     return user.get(login) == senha


@auth.verify_password
def Verificacao(login,senha):
    if not (login,senha):
        return False
    return Usuarios.query.filter_by(login=login,senha=senha).first()


class Pessoa(Resource):
    @auth.login_required
    def get(self,nome):
        pessoa = Pessoas.query.filter_by(Nome=nome).first()
        try:
            response= {'Nome':pessoa.Nome , 'Idade':pessoa.Idade,'id':pessoa.id}
        except AttributeError:
            response= {'status':'error','mensagem':'pessoa nao encontrada'}
        return response

    @auth.login_required
    def post(self,nome):
        pessoa = Pessoas.query.filter_by(Nome=nome).first()
        dados = request.json
        try:
            if 'nome' in dados:
                pessoa.Nome = dados['nome']
            if 'idade' in dados:
                pessoa.Idade = dados['idade']
        except AttributeError:
            response = {'status': 'error', 'mensagem': 'pessoa nao encontrada'}
        else:
            pessoa.save()
            response={'id':pessoa.id,
                      'Nome':pessoa.Nome,
                      'Idade':pessoa.Idade}
        return response

    @auth.login_required
    def delete(self,nome):
        pessoa=Pessoas.query.filter_by(Nome=nome).first()
        mensagem = 'Pessoa {} excluida com sucesso'.format(pessoa.Nome)
        pessoa.deleta()
        return {'status':'Sucesso','mensagem':mensagem}

class ListaPessoas(Resource):
    @auth.login_required
    def get(self):
        pessoas = Pessoas.query.all()
        response = [ {'id':i.id,
                      'nome':i.Nome,
                      'idade':i.Idade
                      } for i in pessoas]
        return response

    @auth.login_required
    def post(self):
        dados = request.json
        pessoa = Pessoas(Nome=dados['nome'], Idade=dados['idade'])
        pessoa.save()
        response = {'nome': pessoa.Nome,
                    'id': pessoa.id,
                    'idade':pessoa.Idade
                   }
        return response


class ListaAtividades(Resource):
    @auth.login_required
    def get(self):
        atividades = Atividades.query.all()
        response = [ {'id': i.id,
                      'pessoa': i.pessoa.Nome,
                      'nome': i.nome
                      } for i in atividades]


        return response

    @auth.login_required
    def post(self):
        dados = request.json
        pessoas = Pessoas.query.filter_by(Nome=dados['pessoa']).first()
        atividade = Atividades(nome=dados['nome'],pessoa=pessoas,status=dados['status'])
        atividade.save()
        response = {'pessoa': atividade.pessoa.Nome,
                    'nome': atividade.nome,
                    'id':atividade.id,
                    'status':atividade.status
                   }
        return response

class AtividadesPessoa(Resource):
    @auth.login_required
    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(Nome=dados['pessoa']).first()
        atividades = Atividades.query.filter_by(pessoa_id=pessoa.id)
        response = [ {'id': i.id,
                      'pessoa': i.pessoa.Nome,
                      'nome': i.nome
                          } for i in atividades ]
        return response


api.add_resource(Pessoa,'/pessoa/<string:nome>/')
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(ListaAtividades, '/atividades/')
api.add_resource(AtividadesPessoa, '/atividades/pessoa/')

if __name__ == '__main__':
    app.run(debug=True)