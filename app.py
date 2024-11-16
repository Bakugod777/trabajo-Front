from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app, resources={r"/usuarios/*": {"origins": "http://127.0.0.1:5500"}})

# Función para obtener la conexión a la base de datos
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        database='tienda_peluches',  # Nombre de la base de datos de la tienda
        user='root',
        password=''  # Cambia la contraseña según tu configuración
    )
    if connection.is_connected():
        return connection
    else:
        return None

# Lista de productos disponibles
products = [
    { 'id': 1, 'name': 'Osos de Peluche', 'price': 20000, 'description': 'Tiernos y suaves osos de peluche, ideales para regalar o decorar cualquier espacio.', 'image': '/IMG/oso.jpg' },
    { 'id': 2, 'name': 'Mapache', 'price': 15000, 'description': 'Encantador mapache de peluche con detalles realistas y un diseño adorable, perfecto para todas las edades.', 'image': '/IMG/mapache.jpg' },
    { 'id': 3, 'name': 'Oso Grande', 'price': 30000, 'description': 'Un oso de peluche extra grande para los abrazos más grandes. Perfecto como regalo especial.', 'image': '/IMG/oso_grande.jpg' },
    { 'id': 4, 'name': 'Pack de 6 Peluches', 'price': 100000, 'description': 'Set de seis peluches variados, con diferentes personajes y tamaños. Ideal para coleccionar o regalar en grupo.', 'image': '/IMG/pack6.jpg' },
    { 'id': 5, 'name': 'Pack de 3 Gatos de Peluche', 'price': 60000, 'description': 'Set de tres adorables gatos de peluche con diferentes poses. El regalo perfecto para los amantes de los gatos.', 'image': '/IMG/gatos.jpg' },
]

cart = []

# Ruta para obtener productos
@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify(products)

# Ruta para agregar un producto al carrito
@app.route('/api/cart', methods=['POST'])
def add_to_cart():
    product_id = request.json.get('id')
    product = next((item for item in products if item['id'] == product_id), None)
    if product:
        cart.append(product)
        return jsonify({"message": "Producto agregado al carrito"}), 201
    return jsonify({"error": "Producto no encontrado"}), 404

# Ruta para obtener el carrito de compras
@app.route('/api/cart', methods=['GET'])
def get_cart():
    return jsonify(cart)

# Ruta para eliminar un producto del carrito
@app.route('/api/cart/<int:product_id>', methods=['DELETE'])
def remove_from_cart(product_id):
    global cart
    cart = [item for item in cart if item['id'] != product_id]
    return jsonify({"message": "Producto eliminado del carrito"}), 200

# Ruta de registro de usuario
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        query = "INSERT INTO usuarios (email, contraseña) VALUES (%s, %s)"
        cursor.execute(query, (email, password))
        connection.commit()
        return jsonify({'message': 'Usuario registrado exitosamente'}), 201
    else:
        return jsonify({'message': 'Error de conexión a la base de datos'}), 500

# Ruta para inicio de sesión
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('username')
    password = data.get('password')

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM usuarios WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if user and user['contraseña'] == password:
            return jsonify({'user': user, 'message': 'Inicio de sesión exitoso'}), 200
        else:
            return jsonify({'message': 'Usuario o contraseña incorrectos'}), 401
    else:
        return jsonify({'message': 'Error de conexión a la base de datos'}), 500

if __name__ == '__main__':
    app.run(debug=True)
