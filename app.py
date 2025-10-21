from flask import Flask, request
import subprocess
import sqlite3
from config import SENHA_BANCO_DE_DADOS # Importa uma senha de outro arquivo


app = Flask(__name__)

# Falha de Segurança 1: Segredo diretamente no código (Detectado por Gitleaks)
CHAVE_API_INTERNA = "b4b8-4215-a052-a6345b34567SECRET"

@app.route('/')
def home():
    return "<h1>Mini-Aplicação Insegura para TCC</h1><p>Esta aplicação tem falhas de segurança propositais.</p>"

@app.route('/executar')
def executar_comando():
    # Pega o comando a ser executado da URL (ex: /executar?cmd=ls)
    comando = request.args.get('cmd')

    # Falha de Segurança 2: Injeção de Comando (Detectado por Semgrep)
    # O uso de 'shell=True' com input do usuário permite que um atacante execute qualquer comando no servidor.
    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
    
    return f"<h2>Comando executado: {comando}</h2><pre>{resultado.stdout}</pre>"

@app.route('/usuario')
def buscar_usuario():
    # Pega o nome do usuário da URL (ex: /usuario?nome=admin)
    nome_usuario = request.args.get('nome')

    # Conecta a um banco de dados em memória para o exemplo
    conexao = sqlite3.connect(':memory:')
    cursor = conexao.cursor()
    cursor.execute("CREATE TABLE usuarios (id INT, nome TEXT, senha TEXT)")
    cursor.execute("INSERT INTO usuarios VALUES (1, 'admin', '12345'), (2, 'visitante', 'abcde')")

    # Falha de Segurança 3: Injeção de SQL (Detectado por Semgrep)
    # A query é montada com formatação de string, permitindo que um atacante manipule a consulta SQL.
    query = f"SELECT id, nome FROM usuarios WHERE nome = '{nome_usuario}'"
    resultado = cursor.execute(query).fetchall()

    return f"<h2>Busca pelo usuário: {nome_usuario}</h2><pre>{resultado}</pre>"


if __name__ == "__main__":
    # Falha de Segurança 4: Modo Debug Ativado (Detectado por Semgrep)
    # Executar o Flask em modo debug em produção expõe informações sensíveis e permite execução de código.
    app.run(debug=True, host='0.0.0.0', port=5000)


