import os
import json
from flask import Flask, jsonify, request, send_from_directory, send_file

app = Flask(__name__)
PORT = 8000
HISTORY_FILE = os.path.join(os.path.dirname(__file__), 'history.json')

import sqlite3
import datetime

# Cópia em memória para fallback caso o sistema de ficheiros seja apenas de leitura
_memory_history = []
# Se estiver no Render com disco persistente, o disco é montado em /data
if os.path.exists('/data'):
    DATABASE = '/data/history.db'
else:
    # No Vercel ou plataformas serverless, a raiz é apenas de leitura.
    # Testamos se conseguimos escrever localmente, senão usamos a pasta /tmp (que é gravável).
    try:
        test_file = os.path.join(os.path.dirname(__file__), '.write_test')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        DATABASE = os.path.join(os.path.dirname(__file__), 'history.db')
    except Exception:
        DATABASE = '/tmp/history.db'

def init_db():
    """Inicializa a base de dados SQLite e cria a tabela se não existir."""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phrase TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        print("Base de dados SQLite inicializada com sucesso.")
    except Exception as e:
        print(f"Erro ao inicializar base de dados SQLite (a usar fallback em memória): {e}")

# Inicializa a BD no arranque
init_db()

def load_history():
    """Carrega o histórico de frases a partir do SQLite, com fallback para memória."""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT id, phrase, timestamp FROM history ORDER BY id DESC')
        rows = cursor.fetchall()
        conn.close()
        
        history = []
        for row in rows:
            history.append({
                "id": row[0],
                "phrase": row[1],
                "timestamp": row[2]
            })
        return history
    except Exception as e:
        print(f"Erro ao ler do SQLite (usando fallback em memória): {e}")
        return _memory_history

def add_to_history_db(phrase):
    """Adiciona uma nova frase ao SQLite com fallback em memória."""
    global _memory_history
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Atualiza também o fallback em memória
    _memory_history.insert(0, {
        "id": len(_memory_history) + 1,
        "phrase": phrase,
        "timestamp": timestamp
    })
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO history (phrase, timestamp) VALUES (?, ?)', (phrase, timestamp))
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return {
            "id": new_id,
            "phrase": phrase,
            "timestamp": timestamp
        }
    except Exception as e:
        print(f"Erro ao gravar no SQLite (guardado apenas em memória): {e}")
        return _memory_history[0]

def clear_history_db():
    """Limpa todo o histórico no SQLite e na memória."""
    global _memory_history
    _memory_history = []
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM history')
        conn.commit()
        conn.close()
        print("Histórico apagado do SQLite com sucesso.")
    except Exception as e:
        print(f"Erro ao limpar SQLite: {e}")

@app.route('/')
def index():
    """Serve a aplicação principal desktop."""
    return send_file('index.html')

@app.route('/mobile/')
@app.route('/mobile/<path:path>')
def serve_mobile(path='index.html'):
    """Serve ficheiros estáticos da versão mobile."""
    return send_from_directory('mobile', path)

@app.route('/api/history', methods=['GET'])
def get_history():
    """Devolve a lista de frases traduzidas e guardadas."""
    return jsonify(load_history())

@app.route('/api/history', methods=['POST'])
def add_history():
    """Adiciona uma nova frase traduzida ao histórico persistente."""
    data = request.json or {}
    phrase = data.get('phrase', '').strip()
    if not phrase:
        return jsonify({"error": "A frase não pode estar vazia."}), 400
    
    new_entry = add_to_history_db(phrase)
    return jsonify(new_entry), 201

@app.route('/api/history', methods=['DELETE'])
def clear_history():
    """Limpa todo o histórico de frases guardadas no servidor."""
    clear_history_db()
    return jsonify([]), 200

@app.route('/<path:path>')
def serve_root_files(path):
    """Serve ficheiros no diretório raiz (ex: modelos, manifestos, etc.)."""
    return send_from_directory('.', path)

if __name__ == '__main__':
    print(f"LGP Tradutor rodando em http://localhost:{PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=True)
