from flask import Flask, request, jsonify, render_template # Importa o Flask, request, jsonify e render_template
import sqlite3 # Importa o sqlite3
from flask_cors import CORS # Importa o CORS para permitir requisições de diferentes origens

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
def homepage():
  return render_template('index.html')

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
    
     # Verifica se algum registro foi afetado (se o livro foi encontrado e excluído).
    if sqlite3.Cursor.rowcount == 0:
        # Retorna um erro 400 (Bad Request) se o livro não foi encontrado.
        return jsonify({"erro": "Livro não encontrado"}), 400

    # Retorna uma mensagem de sucesso com o código 200 (OK).
    return jsonify({"menssagem": "Livro excluído com sucesso"}), 200

# Rota para atualizar um livro
@app.route('/livros/<int:id>', methods=['PUT'])
def atualizar_livro(id):
  dados = request.get_json()
  
  titulo = dados.get('titulo')
  categoria = dados.get('categoria')
  autor = dados.get('autor')
  imagem_url = dados.get('imagem_url')
  
  if not all([titulo, categoria, autor, imagem_url]):
    return jsonify({'erro': 'Todos os campos são obrigatórios!'}), 400
  
  with sqlite3.connect('database.db') as conn:
    conn.execute("""UPDATE livros SET titulo = ?, categoria = ?, autor = ?, imagem_url = ? WHERE id = ?""", (titulo, categoria, autor, imagem_url, id))
    conn.commit()
    
    return jsonify({"mensagem": "Livro atualizado com sucesso!"}), 200

# Ponto de entrada da aplicação: inicia o servidor em modo de depuração (debug)
if __name__ == '__main__':
  app.run(debug=True)
