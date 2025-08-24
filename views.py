from flask import render_template, url_for, request, redirect, session
from app import app, db
from models import Usuarios, Tarefas, FormularioTarefas, FormularioUsuarios




@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'usuario' not in session:
            form = FormularioUsuarios()
            return render_template('login.html', form=form)
        
        return redirect(url_for('tarefas'))
    
    elif request.method == 'POST':
        form = FormularioUsuarios(request.form)

        usuario = Usuarios.query.get(form.usuario.data)

        if usuario:
            if form.senha.data == usuario.senha:
                session['usuario'] = usuario.usuario

                return redirect(url_for('tarefas'))
        
        return redirect(url_for('login'))
    
@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'GET':
        if 'usuario' not in session:
            form = FormularioUsuarios()
            return render_template('cadastrar.html', form=form)
        
        return redirect(url_for('tarefas'))
    
    elif request.method == 'POST':
        form = FormularioUsuarios(request.form)

        if form.validate_on_submit():
            nome = form.nome.data
            usuario = form.usuario.data
            senha = form.senha.data

            usuario = Usuarios(nome=nome, usuario=usuario, senha=senha)
            db.session.add(usuario)
            db.session.commit()

            session['usuario'] = usuario.usuario

            return redirect(url_for('tarefas'))
        
        form = FormularioUsuarios()
        return render_template('cadastrar.html', form=form)

@app.route('/logout')
def logout():
    if 'usuario' in session:
        session.clear()
    return redirect(url_for('login'))




@app.route('/tarefas')
def tarefas():

    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    tarefas = Tarefas.query.order_by(Tarefas.id)
    
    return render_template('tarefas.html', tarefas=tarefas, usuarios=Usuarios)

@app.route('/tarefas/adicionar', methods=['GET', 'POST'])
def tarefas_adicionar():

    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        form = FormularioTarefas()

        for u in Usuarios.query.order_by(Usuarios.nome).all():
            form.responsavel.choices.append((u.usuario, u.nome))
 
        return render_template('tarefas_adicionar.html', form=form)
    
    elif request.method == 'POST':
        form = FormularioTarefas(request.form)

        for u in Usuarios.query.order_by(Usuarios.nome).all():
            form.responsavel.choices.append((u.usuario, u.nome))

        if form.validate_on_submit():         
            descricao = form.descricao.data
            id_estado = form.id_estado.data
            responsavel = form.responsavel.data

            nova_tarefa = Tarefas(descricao=descricao, id_estado=id_estado, responsavel=responsavel)
            db.session.add(nova_tarefa)
            db.session.commit()

        return redirect(url_for('tarefas'))

@app.route('/tarefas/editar/<int:id>', methods=['GET', 'POST'])
def tarefas_editar(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    tarefa = Tarefas.query.get(id)

    if session['usuario'] == tarefa.responsavel or session['usuario'] == 'adm':
        if request.method == 'GET':
            if tarefa:
                form = FormularioTarefas()
                for u in Usuarios.query.order_by(Usuarios.nome).all():
                    form.responsavel.choices.append((u.usuario, u.nome))

                form.descricao.data = tarefa.descricao
                form.id_estado.data = tarefa.id_estado
                form.responsavel.data = tarefa.responsavel

                return render_template('tarefas_editar.html', id=id, form=form)
        
        elif request.method == 'POST':
            form = FormularioTarefas(request.form)

            for u in Usuarios.query.order_by(Usuarios.nome).all():
                form.responsavel.choices.append((u.usuario, u.nome))

            if form.validate_on_submit(): 

                tarefa = Tarefas.query.get(id)     
                tarefa.descricao = form.descricao.data
                tarefa.id_estado = form.id_estado.data
                tarefa.responsavel = form.responsavel.data

                db.session.add(tarefa)
                db.session.commit()

    return redirect(url_for('tarefas'))
    
@app.route('/tarefas/alterar_estado/<int:id>')
def tarefas_alterar_estado(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    tarefa = Tarefas.query.get(id)

    if session['usuario'] == tarefa.responsavel or session['usuario'] == 'adm':
    
        if tarefa:
            if tarefa.id_estado < 3:
                tarefa.id_estado += 1
            else:
                tarefa.id_estado = 1
            
            db.session.add(tarefa)
            db.session.commit()

    return redirect(url_for('tarefas'))

@app.route('/tarefas/excluir/<int:id>')
def tarefas_excluir(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    tarefa = Tarefas.query.get(id)

    if session['usuario'] == tarefa.responsavel or session['usuario'] == 'adm':
    
        if tarefa:
            db.session.delete(tarefa)
            db.session.commit()
        
    return redirect(url_for('tarefas'))