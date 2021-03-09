# Import
from sqlalchemy import create_engine,Column, Integer, String,ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Crianto o banco de dados
engine = create_engine('sqlite:///atividades.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         bind=engine))
base = declarative_base()
base.query = db_session.query_property()

# Criando as classes
class Pessoas(base):
    __tablename__ = 'pessoas'
    id = Column(Integer, primary_key=True)
    Nome = Column(String(40),index=True)
    Idade = Column(Integer)

    def __repr__(self):
        return '<Pessoa {}>'.format(self.Nome)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def deleta(self):
        db_session.delete(self)
        db_session.commit()


class Atividades(base):
    __tablename__ = 'atividades'
    id = Column(Integer, primary_key=True)
    nome = Column(String(80))
    pessoa_id  = Column(Integer, ForeignKey('pessoas.id'))
    pessoa = relationship("Pessoas")

def iniciar_banco():
    base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    iniciar_banco()