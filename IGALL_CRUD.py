
from flask import Flask, request, jsonify
from flask import request

from flask_cors import CORS


import mysql.connector

from werkzeug.utils import secure_filename

import os
import time

app = Flask(__name__)
CORS(app, resources={r"/documentos/*": {"origins": "http://127.0.0.1:5500"}}, methods=["GET", "POST", "PUT", "DELETE"])

#-------------------------------------------------
#    definicion clase biblioteca
#-------------------------------------------------
class Biblioteca:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
        )
        self.cursor = self.conn.cursor()
        self.cursor = self.conn.cursor(dictionary=True)
        
        # Intentamos seleccionar la base de datos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err
        # Una vez que la base de datos está establecida, creamos la tabla si no existe
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS `Biblioteca` (
                            `No` varchar(255) NOT NULL,
                            `Title` text DEFAULT NULL,
                            `Area` text DEFAULT NULL,
                            `url` text DEFAULT NULL,
                            `Last_valid_version` float DEFAULT NULL,
                            `Igall_owner` text DEFAULT NULL
                            )''')
        self.conn.commit()
 # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)

    def listar_documentos(self):
        self.cursor.execute("SELECT * FROM Biblioteca")
        documentos = self.cursor.fetchall()
        return documentos

    def agregar_documento(self, No, Title, Area, url, Last_valid_version, Igall_owner):
        self.cursor.execute("SELECT * FROM Biblioteca WHERE No = %s", (No,))
        documento_existe = self.cursor.fetchone()
        if documento_existe:
            return False
        else:
            sql = "INSERT INTO Biblioteca (No, Title, Area, url, `Last_valid_version`, Igall_owner) VALUES (%s, %s, %s, %s, %s, %s)" 
            values = (No, Title, Area, url, Last_valid_version, Igall_owner)
            self.cursor.execute(sql,values)
            self.conn.commit()
            return True
    
    def consultar_documento(self, No):
        self.cursor.execute("SELECT * FROM Biblioteca WHERE No =  %s", (No,))
        documento = self.cursor.fetchone()
        return documento
    
    def modificar_documento(self, No, Title, Area, url, Last_valid_version, Igall_owner):
        sql = "UPDATE Biblioteca SET Title = %s, Area = %s, url = %s, Last_valid_version = %s, Igall_owner = %s WHERE No = %s"
        values = (Title, Area, url, Last_valid_version, Igall_owner, No)

        self.cursor.execute(sql, values)
        self.conn.commit()
        
        return self.cursor.rowcount > 0

    
    def mostrar_documentos(self, No):
        self.cursor.execute("SELECT * FROM Biblioteca WHERE No = %s", (No,))
        documentos = self.cursor.fetchall()
        print("-" * 50)
        for documento in documentos:
            print(f"Código..................: {documento['No']}")
            print(f"Título..................: {documento['Title']}")
            print(f"Área....................: {documento['Area']}")
            print(f"URL.....................: {documento['url']}")
            print(f"Última versión válida...: {documento['Last_valid_version']}")
            print(f"Propietario..............: {documento['Igall_owner']}")
            print("-" * 50)

    
    
    def eliminar_documento(self, No):
        sql = "DELETE FROM Biblioteca WHERE No = %s"
        self.cursor.execute(sql, (No,))
        self.conn.commit()
        # Consumir resultados para evitar el "Unread result found"
        self.cursor.fetchall()
        return self.cursor.rowcount > 0


#-------------------------------------------------
#    PROGRAMA PRINCIPAL
#-------------------------------------------------
    
BIBLIOTECA = Biblioteca(host='localhost', user='root', password='', database='mechanical')


# Carpeta para almacenar los documentos
ruta_destino= 'static\documentos'

@app.route("/documentos", methods=["GET"])
def listar_documentos():
    documentos = BIBLIOTECA.listar_documentos()
    return jsonify(documentos)

@app.route("/documentos/<No>", methods=["GET"])
def mostrar_documento(No):
    BIBLIOTECA.mostrar_documentos(No)
    documento = BIBLIOTECA.consultar_documento(No)
    if documento:
        return jsonify(documento)
    else:
        return "Producto no encontrado", 404
    
@app.route("/documentos", methods=["POST"])
def agregar_documento():
    # Recojo los datos del form
    No = request.form['No']
    Title = request.form['Title']
    Area = request.form['Area']
    archivo = request.files['Archivo']
    Last_valid_version = request.form['Last_valid_version']
    Igall_owner = request.form['Igall_owner']
    
    nombre_url = secure_filename(archivo.filename)

    nombre_base, extension = os.path.splitext(nombre_url)
    nombre_url = f"{nombre_base}_{int(time.time())}{extension}"
    archivo.save(os.path.join(ruta_destino, nombre_url))

    if BIBLIOTECA.agregar_documento(No, Title, Area, nombre_url, Last_valid_version, Igall_owner):
        return jsonify({"mensaje": "Documento agregado"}), 201
    else:
        return jsonify({"mensaje": "Documento existente"}), 400

@app.route("/documentos/<No>", methods=["PUT"])
def modificar_documento(No):
    # Recojo los datos del form
    No = request.form['No']
    Title = request.form['Title']
    Area = request.form['Area']
    Last_valid_version = request.form['Last_valid_version']
    Igall_owner = request.form['Igall_owner']

    archivo = request.files['Archivo']
    nombre_url = secure_filename(archivo.filename)
    nombre_base, extension = os.path.splitext(nombre_url)
    nombre_archivo = f"{nombre_base}_{int(time.time())}{extension}"
    archivo.save(os.path.join(ruta_destino, nombre_archivo))

    if BIBLIOTECA.modificar_documento(No, Title, Area, nombre_archivo, Last_valid_version, Igall_owner):
        return jsonify({"mensaje": "Documento modificado"}), 200
    else:
        return jsonify({"mensaje": "Documento no encontrado"}), 404

@app.route("/documentos/<No>", methods=["DELETE"])
def eliminar_documento(No):
    documento = BIBLIOTECA.consultar_documento(No)
    if documento:
        try:
            # Eliminar el documento si existe
            url = os.path.join(ruta_destino, documento['url'])
            if os.path.exists(url):
                os.remove(url)

            # Luego, elimina el documento de la biblioteca
            if BIBLIOTECA.eliminar_documento(No):
                print("Documento eliminado correctamente")
                return jsonify({"mensaje": "Documento eliminado correctamente"}), 200
            else:
                print("Error interno al eliminar el documento de la biblioteca")
                return jsonify({"error": True, "message": "Error interno al eliminar el documento"}), 500
        except Exception as e:
            print("Error al eliminar el documento:", str(e))
            return jsonify({"error": True, "message": str(e)}), 500
    else:
        return jsonify({"error": True, "message": "Documento no encontrado"}), 404



    
if __name__ == "__main__":
    app.run(debug=True)


#Database host address:Celinaetienot.mysql.pythonanywhere-services.com
#User:Celinaetienot
#password: JaPaCe2023
#Database:Celinaetienot$IGALL
#ruta_documentos:'/home/Celinaetienot/mysite/static/documents/'
