from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField, validators
from app import db




class Tarefas(db.Model):
    __tablename__ = 'tarefas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(50), nullable=False)
    id_estado = db.Column(db.Integer, db.ForeignKey('tarefas_estados.id_estado'), nullable=False)
    responsavel = db.Column(db.String(20), db.ForeignKey('usuarios.usuario'), nullable=False)

class TarefasEstados(db.Model):
    __tablename__ = 'tarefas_estados'
    id_estado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estado = db.Column(db.String(10), nullable=False)

class Usuarios(db.Model):
    usuario = db.Column(db.String(20), primary_key = True)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(30), nullable=False)




class FormularioTarefas(FlaskForm):
    descricao = StringField('Descrição', [validators.data_required(), validators.Length(min=3, max=50)])
    id_estado = SelectField('Estado', [validators.data_required()], choices=[(1, 'Para fazer'), (2, 'Fazendo'), (3, 'Feito')])

    responsavel = SelectField('Responsável', [validators.data_required()], choices=[])
    
    adicionar = SubmitField('Adicionar')
    editar = SubmitField('Atualizar')

class FormularioUsuarios(FlaskForm):
    nome = StringField('Nome', [validators.data_required(), validators.Length(min=3, max=20)])
    usuario = StringField('Usuário', [validators.data_required(), validators.Length(min=3, max=20)])
    senha = PasswordField('Senha', [validators.data_required()])
    entrar = SubmitField('Entrar')
    cadastrar = SubmitField('Cadastrar')