from flask import Flask,request
from flask_restful import Resource, Api
from models import Pessoas,Atividades


app = Flask(__name__)

api = Api(app)



class Pessoa(Resource):
    def get(self,nome):
        pessoa = Pessoas.query.filter_by(Nome=nome).first()
        try:
            response= {'Nome':pessoa.Nome , 'Idade':pessoa.Idade,'id':pessoa.id}
        except AttributeError:
            response= {'status':'error','mensagem':'pessoa nao encontrada'}
        return response

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

    def delete(self,nome):
        pessoa=Pessoas.query.filter_by(Nome=nome).first()
        mensagem = 'Pessoa {} excluida com sucesso'.format(pessoa.Nome)
        pessoa.deleta()
        return {'status':'Sucesso','mensagem':mensagem}

class ListaPessoas(Resource):
    def get(self):
        pessoas = Pessoas.query.all()
        response = [ {'id':i.id,
                      'nome':i.Nome,
                      'idade':i.Idade
                      } for i in pessoas]
        return response

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
    def get(self):
        atividades = Atividades.query.all()
        response = [ {'id': i.id,
                      'pessoa': i.pessoa.Nome,
                      'nome': i.nome
                          } for i in atividades ]
        return response

    def post(self):
        dados = request.json
        pessoas = Pessoas.query.filter_by(Nome=dados['pessoa']).first()
        atividade = Atividades(nome=dados['nome'],pessoa=pessoas)
        atividade.save()
        response = {'pessoa': atividade.pessoa.Nome,
                    'nome': atividade.nome,
                    'id':atividade.id
                   }
        return response

api.add_resource(Pessoa,'/pessoa/<string:nome>/')
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(ListaAtividades, '/atividades/')

if __name__ == '__main__':
    app.run(debug=True)