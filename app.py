from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'forte'  # troque por uma chave forte

# Usuários fixos
USUARIOS = {
    'admin1': 'senha123',
    'admin2': 'senha456',
    'admin3': 'senha789'
}

# Criação do banco de dados (se não existir)
def init_db():
    if not os.path.exists('chamados.db'):
        conn = sqlite3.connect('chamados.db')
        conn.execute('''
            CREATE TABLE chamados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT NOT NULL,
                status TEXT DEFAULT 'Aberto',
                prioridade TEXT,
                solicitante TEXT
            )
        ''')
        conn.commit()
        conn.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        if usuario in USUARIOS and USUARIOS[usuario] == senha:
            session['usuario'] = usuario
            flash('Login realizado com sucesso.')
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha incorretos.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Você saiu com sucesso.')
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('chamados.db')
    chamados = conn.execute("SELECT * FROM chamados").fetchall()
    conn.close()
    return render_template('index.html', chamados=chamados, usuario=session['usuario'])

@app.route('/novo', methods=['GET', 'POST'])
def novo():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        prioridade = request.form['prioridade']
        solicitante = request.form['solicitante']
        conn = sqlite3.connect('chamados.db')
        conn.execute("INSERT INTO chamados (titulo, descricao, prioridade, solicitante) VALUES (?, ?, ?, ?)",
                     (titulo, descricao, prioridade, solicitante))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('novo.html')

@app.route('/chamado/<int:id>')
def detalhe(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('chamados.db')
    chamado = conn.execute("SELECT * FROM chamados WHERE id = ?", (id,)).fetchone()
    conn.close()
    return render_template('detalhe.html', chamado=chamado)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
