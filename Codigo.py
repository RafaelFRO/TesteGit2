from flask import Flask, jsonify, request, abort

app = Flask(__name__)

livros = [
    {
        'id': 1,
        'livro': 'Danny Astronauta',
        'autor': 'Rafael de Franca',
        'pág.': '850',
        'valor': '150'
    },
    {
        'id': 2,
        'livro': 'Senai é complicado',
        'autor': 'Vinny',
        'pág.': '500',
        'valor': '120'
    },
    {
        'id': 3,
        'livro': 'Olinda',
        'autor': 'Danny',
        'pág.': '350',
        'valor': '100'
    },
]

@app.route('/livros', methods=['GET'])
def consultar_livros():
    return jsonify(livros)

@app.route('/livros/<int:id>', methods=['GET'])
def consultar_livro_por_id(id):
    livro = next((livro for livro in livros if livro['id'] == id), None)
    if livro is None:
        return jsonify({'message': 'Livro não encontrado'}), 404
    return jsonify(livro)

@app.route('/livros', methods=['POST'])
def adicionar_livro():
    if not request.is_json:
        return jsonify({'message': 'Tipo de mídia não suportado. Envie JSON.'}), 415

    try:
        novo_livro = request.get_json()
    except Exception as e:
        return jsonify({'message': f'Erro ao decodificar JSON: {str(e)}'}), 400

    if not all(key in novo_livro for key in ('id', 'livro', 'autor', 'pág.', 'valor')):
        return jsonify({'message': 'Dados do livro incompletos ou inválidos.'}), 400
    
    if any(livro['id'] == novo_livro['id'] for livro in livros):
        return jsonify({'message': 'ID do livro já existe.'}), 400
    
    livros.append(novo_livro)
    return jsonify(novo_livro), 201

@app.route('/livros/<int:id>', methods=['PUT'])
def atualizar_livro_por_id(id):
    if not request.is_json:
        return jsonify({'message': 'Tipo de mídia não suportado. Envie JSON.'}), 415
    
    try:
        livro_atualizado = request.get_json()
    except Exception as e:
        return jsonify({'message': f'Erro ao decodificar JSON: {str(e)}'}), 400
    
    for indice, livro in enumerate(livros):
        if livro['id'] == id:
            livros[indice].update(livro_atualizado)
            return jsonify(livros[indice])
    return jsonify({'message': 'Livro não encontrado'}), 404

@app.route('/livros/<int:id>', methods=['DELETE'])
def excluir_livro_por_id(id):
    global livros
    livros = [livro for livro in livros if livro['id'] != id]
    if len(livros) == len(livros):
        return jsonify({'message': 'Livro não encontrado'}), 404
    return jsonify({'message': 'Livro excluído'}), 200

if __name__ == '__main__':
    app.run(port=8080, host='localhost', debug=True)