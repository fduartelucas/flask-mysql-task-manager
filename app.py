from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect




app = Flask(__name__)

app.secret_key = 'segredo'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'root',
        servidor = 'localhost',
        database = 'gerenciador_de_tarefas'
    )

db = SQLAlchemy(app)

csrf = CSRFProtect(app)

from views import *

if __name__ == '__main__':
    app.run(debug=True)