from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Criação do banco de dados
def init_db():
    conn = sqlite3.connect('chamados.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS chamados (
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

# Página inicial: lista de chamados
@app.route('/')
def index():
    conn = sqlite3.connect('chamados.db')
    chamados = conn.execute("SELECT * FROM chamados").fetchall()
    conn.close()
    return render_template('index.html', chamados=chamados)

# Formulário para novo chamado
@app.route('/novo', methods=['GET', 'POST'])
def novo():
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
        return redirect('/')
    return render_template('novo.html')

# Página de detalhes do chamado
@app.route('/chamado/<int:id>')
def detalhe(id):
    conn = sqlite3.connect('chamados.db')
    chamado = conn.execute("SELECT * FROM chamados WHERE id = ?", (id,)).fetchone()
    conn.close()
    return render_template('detalhe.html', chamado=chamado)

# Inicializa o banco e roda o app
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
