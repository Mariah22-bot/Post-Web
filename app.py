from flask import Flask, render_template, request, url_for, flash, redirect
import os,datetime
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.exceptions import abort

# Configuração do caminho do projeto
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))

app = Flask('__name__')
app.config['SECRET_KEY'] = 'cocodepombo'
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
db = SQLAlchemy(app)

# Definição do Modelo do Banco de Dados
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.now)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(200), nullable=False)

# Rota Principal
@app.route('/')
def index():
    posts = Posts.query.all()
    return render_template('index.html', posts=posts)

def get_post(post_id):
    post = Posts.query.filter_by(id=post_id).first()
    if post is None:
        abort(404)
    return post

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

# Rota para a página de criação de novos posts
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('O título é obrigatório!')
        else:
            # Cria o objeto, adiciona e salva no banco
            post = Posts(title=title, content=content)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('index'))

    return render_template('create.html')

# NOVA: Rota para editar posts existentes
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Título é obrigatório!')
        else:
            post.title = title
            post.content = content
            db.session.commit()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

# Rota para deletar um post existente
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id) # Usa a sua função auxiliar para garantir que o post existe
    db.session.delete(post) # Comando que marca o post para ser removido
    db.session.commit() # Salva a alteração definitivamente no banco de dados
    flash('"{}" foi apagado com sucesso!'.format(post.title)) # Mensagem de confirmação
    return redirect(url_for('index')) # Redireciona de volta para a página principal

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)