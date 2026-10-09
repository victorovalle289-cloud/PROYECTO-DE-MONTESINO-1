# =====================================================================
#  Gestor de contraseñas - Backend (API REST con Flask)
#  Proyecto de Montesino - Actividad CRUD en Python-Flask
# =====================================================================
from flask import Flask, jsonify, request   # Flask: servidor web; jsonify: respuestas JSON; request: datos recibidos
from flask_cors import CORS                 # Permite que el frontend (otro origen) consuma la API
import pymysql                              # Conector para la base de datos MySQL
import bcrypt                               # Librería para encriptar las claves
from flasgger import Swagger                # Documentación automática en /apidocs

app = Flask(__name__)   # Se crea la aplicación Flask
CORS(app)               # Se habilita CORS para todas las rutas
Swagger(app)            # Se habilita Swagger (http://127.0.0.1:5000/apidocs)

# Datos de conexión (cámbialos según tu MySQL)
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = '1234'
DB_NAME = 'gestor_contrasena'


# ---------------------------------------------------------------------
# Conexión a la base de datos
# ---------------------------------------------------------------------
def conectar(vhost, vuser, vpass, vdb):
    """Abre y retorna una conexión a MySQL."""
    conn = pymysql.connect(host=vhost, user=vuser, passwd=vpass, db=vdb, charset='utf8mb4')
    return conn


# ---------------------------------------------------------------------
# Ruta para consulta general (GET /)
# ---------------------------------------------------------------------
@app.route("/", methods=['GET'])
def consulta_general():
    """
    Consulta general del baúl de contraseñas
    ---
    responses:
      200:
        description: Lista de registros
    """
    try:
        conn = conectar(DB_HOST, DB_USER, DB_PASS, DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT * FROM baul")      # Trae todos los registros
        datos = cur.fetchall()
        data = []
        for row in datos:                       # Convierte cada fila en un diccionario
            dato = {'id_baul': row[0], 'Plataforma': row[1], 'usuario': row[2], 'clave': row[3]}
            data.append(dato)
        cur.close()
        conn.close()
        return jsonify({'baul': data, 'mensaje': 'Baúl de contraseñas'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})


# ---------------------------------------------------------------------
# Ruta para consulta individual (GET /consulta_individual/<id>)
# ---------------------------------------------------------------------
@app.route("/consulta_individual/<codigo>", methods=['GET'])
def consulta_individual(codigo):
    """
    Consulta individual por ID
    ---
    parameters:
      - name: codigo
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Registro encontrado
    """
    try:
        conn = conectar(DB_HOST, DB_USER, DB_PASS, DB_NAME)
        cur = conn.cursor()
        # Consulta parametrizada (%s) para evitar inyección SQL
        cur.execute("SELECT * FROM baul WHERE id_baul = %s", (codigo,))
        datos = cur.fetchone()
        cur.close()
        conn.close()
        if datos:
            dato = {'id_baul': datos[0], 'Plataforma': datos[1], 'usuario': datos[2], 'clave': datos[3]}
            return jsonify({'baul': dato, 'mensaje': 'Registro encontrado'})
        else:
            return jsonify({'mensaje': 'Registro no encontrado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})


# ---------------------------------------------------------------------
# Ruta para registro (POST /registro/)
# ---------------------------------------------------------------------
@app.route("/registro/", methods=['POST'])
def registro():
    """
    Registrar nueva contraseña
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            plataforma:
              type: string
            usuario:
              type: string
            clave:
              type: string
    responses:
      200:
        description: Registro agregado
    """
    try:
        data = request.get_json()               # Lee el JSON enviado
        plataforma = data['plataforma']
        usuario = data['usuario']
        # Encripta la clave con bcrypt antes de guardarla
        clave = bcrypt.hashpw(data['clave'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        conn = conectar(DB_HOST, DB_USER, DB_PASS, DB_NAME)
        cur = conn.cursor()
        cur.execute("INSERT INTO baul (plataforma, usuario, clave) VALUES (%s, %s, %s)",
                    (plataforma, usuario, clave))
        conn.commit()                           # Guarda los cambios
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Registro agregado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})


# ---------------------------------------------------------------------
# Ruta para eliminar registro (DELETE /eliminar/<id>)
# ---------------------------------------------------------------------
@app.route("/eliminar/<codigo>", methods=['DELETE'])
def eliminar(codigo):
    """
    Eliminar registro por ID
    ---
    parameters:
      - name: codigo
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Registro eliminado
    """
    try:
        conn = conectar(DB_HOST, DB_USER, DB_PASS, DB_NAME)
        cur = conn.cursor()
        cur.execute("DELETE FROM baul WHERE id_baul = %s", (codigo,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Eliminado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})


# ---------------------------------------------------------------------
# Ruta para actualizar registro (PUT /actualizar/<id>)
# ---------------------------------------------------------------------
@app.route("/actualizar/<codigo>", methods=['PUT'])
def actualizar(codigo):
    """
    Actualizar registro por ID
    ---
    parameters:
      - name: codigo
        in: path
        required: true
        type: integer
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            plataforma:
              type: string
            usuario:
              type: string
            clave:
              type: string
    responses:
      200:
        description: Registro actualizado
    """
    try:
        data = request.get_json()
        plataforma = data['plataforma']
        usuario = data['usuario']
        clave = bcrypt.hashpw(data['clave'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        conn = conectar(DB_HOST, DB_USER, DB_PASS, DB_NAME)
        cur = conn.cursor()
        cur.execute("UPDATE baul SET plataforma = %s, usuario = %s, clave = %s WHERE id_baul = %s",
                    (plataforma, usuario, clave, codigo))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Registro actualizado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})


# Punto de entrada: ejecuta el servidor en modo desarrollo
if __name__ == '__main__':
    app.run(debug=True)
