from flask import Flask, request, jsonify
import oracledb

app = Flask(__name__)

# Configurações do banco de dados Oracle
connection = oracledb.connect(
    user="rm97850",
    password="120803",
    dsn="oracle.fiap.com.br:1521/ORCL"
)


# Funções CRUD para tabela de clientes
@app.route('/clientes', methods=['GET'])
def get_clientes():
    cursor = connection.cursor()
    cursor.execute("SELECT cliente_id, nome, email, telefone, endereco, data_cadastro FROM clientes")
    rows = cursor.fetchall()
    cursor.close()
    return jsonify([{
        'cliente_id': r[0],
        'nome': r[1],
        'email': r[2],
        'telefone': r[3],
        'endereco': r[4],
        'data_cadastro': r[5].strftime("%Y-%m-%d")
    } for r in rows])

@app.route('/clientes/<int:id>', methods=['GET'])
def get_cliente(id):
    cursor = connection.cursor()
    cursor.execute("SELECT cliente_id, nome, email, telefone, endereco, data_cadastro FROM clientes WHERE cliente_id = :id", [id])
    row = cursor.fetchone()
    cursor.close()
    return jsonify({
        'cliente_id': row[0],
        'nome': row[1],
        'email': row[2],
        'telefone': row[3],
        'endereco': row[4],
        'data_cadastro': row[5].strftime("%Y-%m-%d")
    }) if row else ('Cliente não encontrado', 404)

@app.route('/clientes', methods=['POST'])
def create_cliente():
    data = request.get_json()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO clientes (nome, email, telefone, endereco)
        VALUES (:nome, :email, :telefone, :endereco) RETURNING cliente_id INTO :id
    """, nome=data['nome'], email=data['email'], telefone=data.get('telefone'), endereco=data.get('endereco'))
    connection.commit()
    cliente_id = cursor.getimplicitresults()[0][0]
    cursor.close()
    return jsonify({'cliente_id': cliente_id}), 201

@app.route('/clientes/<int:id>', methods=['PUT'])
def update_cliente(id):
    data = request.get_json()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE clientes SET nome = :nome, email = :email, telefone = :telefone, endereco = :endereco
        WHERE cliente_id = :id
    """, nome=data['nome'], email=data['email'], telefone=data.get('telefone'), endereco=data.get('endereco'), id=id)
    connection.commit()
    cursor.close()
    return jsonify({'message': 'Cliente atualizado'})

@app.route('/clientes/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM clientes WHERE cliente_id = :id", [id])
    connection.commit()
    cursor.close()
    return jsonify({'message': 'Cliente deletado'})


# Funções CRUD para tabela de pedidos
@app.route('/pedidos', methods=['GET'])
def get_pedidos():
    cursor = connection.cursor()
    cursor.execute("SELECT pedido_id, cliente_id, data_pedido, valor_total, status, descricao, data_entrega FROM pedidos")
    rows = cursor.fetchall()
    cursor.close()
    return jsonify([{
        'pedido_id': r[0],
        'cliente_id': r[1],
        'data_pedido': r[2].strftime("%Y-%m-%d"),
        'valor_total': r[3],
        'status': r[4],
        'descricao': r[5],
        'data_entrega': r[6].strftime("%Y-%m-%d") if r[6] else None
    } for r in rows])

@app.route('/pedidos/<int:id>', methods=['GET'])
def get_pedido(id):
    cursor = connection.cursor()
    cursor.execute("SELECT pedido_id, cliente_id, data_pedido, valor_total, status, descricao, data_entrega FROM pedidos WHERE pedido_id = :id", [id])
    row = cursor.fetchone()
    cursor.close()
    return jsonify({
        'pedido_id': row[0],
        'cliente_id': row[1],
        'data_pedido': row[2].strftime("%Y-%m-%d"),
        'valor_total': row[3],
        'status': row[4],
        'descricao': row[5],
        'data_entrega': row[6].strftime("%Y-%m-%d") if row[6] else None
    }) if row else ('Pedido não encontrado', 404)

@app.route('/pedidos', methods=['POST'])
def create_pedido():
    data = request.get_json()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO pedidos (cliente_id, valor_total, status, descricao, data_entrega)
        VALUES (:cliente_id, :valor_total, :status, :descricao, :data_entrega) RETURNING pedido_id INTO :id
    """, cliente_id=data['cliente_id'], valor_total=data['valor_total'], status=data.get('status', 'Pendente'),
        descricao=data.get('descricao'), data_entrega=data.get('data_entrega'))
    connection.commit()
    pedido_id = cursor.getimplicitresults()[0][0]
    cursor.close()
    return jsonify({'pedido_id': pedido_id}), 201

@app.route('/pedidos/<int:id>', methods=['PUT'])
def update_pedido(id):
    data = request.get_json()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE pedidos SET cliente_id = :cliente_id, valor_total = :valor_total, status = :status,
        descricao = :descricao, data_entrega = :data_entrega WHERE pedido_id = :id
    """, cliente_id=data['cliente_id'], valor_total=data['valor_total'], status=data.get('status', 'Pendente'),
        descricao=data.get('descricao'), data_entrega=data.get('data_entrega'), id=id)
    connection.commit()
    cursor.close()
    return jsonify({'message': 'Pedido atualizado'})

@app.route('/pedidos/<int:id>', methods=['DELETE'])
def delete_pedido(id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM pedidos WHERE pedido_id = :id", [id])
    connection.commit()
    cursor.close()
    return jsonify({'message': 'Pedido deletado'})


if __name__ == '__main__':
    app.run(debug=True)
