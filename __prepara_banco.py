import mysql.connector
from mysql.connector import errorcode

print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='root'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `gerenciador_de_tarefas`;")

cursor.execute("CREATE DATABASE `gerenciador_de_tarefas`;")

cursor.execute("USE `gerenciador_de_tarefas`;")

# criando tabelas
TABLES = {}
TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `usuario` varchar(20),
      `nome` varchar(20) NOT NULL,
      `senha` varchar(30) NOT NULL,
      PRIMARY KEY (`usuario`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')
TABLES['TarefasEstados'] = ('''
      CREATE TABLE `tarefas_estados` (
      `id_estado` int(1) AUTO_INCREMENT,
      `estado` varchar(10) NOT NULL,
      PRIMARY KEY (`id_estado`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')
TABLES['Tarefas'] = ('''
      CREATE TABLE `tarefas` (
      `id` int(8) AUTO_INCREMENT,
      `descricao` varchar(50) NOT NULL,
      `id_estado` int(1) NOT NULL,
      `responsavel` varchar(20) NOT NULL,
      PRIMARY KEY (`id`),
      FOREIGN KEY (id_estado) REFERENCES tarefas_estados(id_estado),
      FOREIGN KEY (responsavel) REFERENCES usuarios(usuario)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')


for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')


# inserindo usuarios
usuarios_sql = 'INSERT INTO usuarios (usuario, nome, senha) VALUES (%s, %s, %s)'
usuarios = [
    ('adm', 'Admin', 'adm'),
    ('lucas', 'Lucas', 'abcd'),
    ('pedro', 'Pedro', 'efgh')
]
cursor.executemany(usuarios_sql, usuarios)

cursor.execute('select * from gerenciador_de_tarefas.usuarios')
print(' -------------  estados:  -------------')
for tarefa in cursor.fetchall():
    print(tarefa[1])




# inserindo estados
tarefas_estados_sql = 'INSERT INTO tarefas_estados (estado) VALUES (%s)'
tarefas_estados = [
      ('Para fazer',),
      ('Fazendo',),
      ('Feito',),
]
cursor.executemany(tarefas_estados_sql, tarefas_estados)

cursor.execute('select * from gerenciador_de_tarefas.tarefas_estados')
print(' -------------  estados:  -------------')
for tarefa in cursor.fetchall():
    print(tarefa[1])




# inserindo tarefas
tarefas_sql = 'INSERT INTO tarefas (descricao, id_estado, responsavel) VALUES (%s, %s, %s)'
tarefas = [
      ('Estudar Python POO', 3, 'lucas'),
      ('Estudar Flask', 2, 'lucas'),
      ('Testar aplicação', 2, 'pedro'),
      ('Estudar Django', 2, 'lucas'),
      ('Corrigir bugs', 1, 'pedro'),
      ('Sugerir melhorias', 1, 'pedro'),
      ('Analisar banco de dados', 1, 'lucas'),
]
cursor.executemany(tarefas_sql, tarefas)

cursor.execute('select * from gerenciador_de_tarefas.tarefas')
print(' -------------  tarefas:  -------------')
for tarefa in cursor.fetchall():
    print(tarefa[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()
