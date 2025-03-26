from flask import Flask, request, jsonify # Importando o Flask, request e jsonify
import sqlite3 # Importando o sqlite3
from flask_cors import CORS # Importando o CORS

app = Flask(__name__) # Inicializando o Flask
CORS(app) # Inicializando o CORS

# Função para criar o banco de dados
def init_db():
  with sqlite3.connect('database.db') as conn:
    conn.execute("""CREATE TABLE IF NOT EXISTS livros(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      titulo TEXT NOT NULL,
      categoria TEXT NOT NULL,
      autor TEXT NOT NULL,
      imagem_url TEXT NOT NULL
      )""")
    print("Banco de dados criado!")

# Chamando a função para criar o banco de dados
init_db()

# Rota para a página inicial
@app.route('/')
def home_page():
  return '<h2>Livros Vai na Web</h2>'

# Rota para cadastrar um novo livro
@app.route('/doar', methods=['POST'])
def doar():
  
  dados = request.get_json()
  
  titulo = dados.get('titulo')
  categoria = dados.get('categoria')
  autor = dados.get('autor')
  imagem_url = dados.get('imagem_url')
  
  if not all([titulo, categoria, autor, imagem_url]):
    return jsonify({'erro': 'Todos os campos são obrigatórios!'}), 400
  
  with sqlite3.connect('database.db') as conn:
    conn.execute(""" INSERT INTO livros (titulo, categoria, autor, imagem_url)
                 VALUES (?,?,?,?)
                 """,(titulo, categoria, autor, imagem_url))
    
    conn.commit()
    
    return jsonify({"mensagem": "Livro cadastrado com sucesso!"}), 201
  
# Rota para listar todos os livros
@app.route('/livros', methods=['GET'])
def livros():
  with sqlite3.connect('database.db') as conn:
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM livros""")
    livros = cursor.fetchall()
    
    livros_json = []
    
    for livro in livros:
      livro_id, titulo, categoria, autor, imagem_url = livro
      livros_json.append({
        'id': livro_id,
        'titulo': titulo,
        'categoria': categoria,
        'autor': autor,
        'imagem_url': imagem_url
      })
    
    return jsonify(livros_json)

# Rota para deletar um livro
@app.route('/livros/<int:id>', methods=['DELETE'])
def deletar_livro(id):
  with sqlite3.connect('database.db') as conn:
    conn.execute("""DELETE FROM livros WHERE id = ?""", (id,))
    conn.commit()
    
    return jsonify({"mensagem": "Livro deletado com sucesso!"})

# Tratamento de Erro
if __name__ == '__main__':
  app.run(debug=True)

