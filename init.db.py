import sqlite3

# Cria a conexão com o arquivo do banco de dados
connection = sqlite3.connect('database.db')

# Abre o arquivo 'schema.sql' e executa os comandos para criar as tabelas
with open('schema.sql') as f:
    connection.executescript(f.read())

# Cria um cursor para interagir com o banco
cur = connection.cursor()

# Insere o primeiro post de teste
cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First Post', 'Content for the first post')
            )

# Insere o segundo post de teste
cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for the second post')
            )

# Salva as alterações (commit) e fecha a conexão
connection.commit()
connection.close()