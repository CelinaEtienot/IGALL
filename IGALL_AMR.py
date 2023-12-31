from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from werkzeug.utils import secure_filename
import os
import time

app = Flask(__name__)
CORS(app, resources={
    r"/documentos/*": {"origins": ["https://celinaetienot.pythonanywhere.com/", "http://127.0.0.1:5500"]},
    r"/lineas/*": {"origins": ["https://celinaetienot.pythonanywhere.com/", "http://127.0.0.1:5500"]}
}, methods=["GET", "POST", "PUT", "DELETE"])


class Biblioteca:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor(dictionary=True)

        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS `biblioteca` (
                            `No` varchar(255) NOT NULL,
                            `Title` text DEFAULT NULL,
                            `Area` text DEFAULT NULL,
                            `url` text DEFAULT NULL,
                            `Last_valid_version` float DEFAULT NULL,
                            `Igall_owner` text DEFAULT NULL
                            )''')
        self.conn.commit()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS `amrtable` (
                                `id` VARCHAR(255) PRIMARY KEY,
                                `table_no` INT,
                                `igall_no` INT,
                                `system_name` VARCHAR(255),
                                `structure_component` VARCHAR(255),
                                `critical_location_part` VARCHAR(255),
                                `material` VARCHAR(255),
                                `environment` VARCHAR(255),
                                `ageing_effect` VARCHAR(255),
                                `degradation_mechanism` VARCHAR(255),
                                `Document` VARCHAR(255),
                                `design` VARCHAR(255)
                            )''')
        self.conn.commit()

    def listar_documentos(self):
        self.cursor.execute("SELECT * FROM biblioteca")
        documentos = self.cursor.fetchall()
        return documentos

    def agregar_documento(self, No, Title, Area, url, Last_valid_version, Igall_owner):
        self.cursor.execute("SELECT * FROM Biblioteca WHERE No = %s", (No,))
        documento_existe = self.cursor.fetchone()
        if documento_existe:
            return False
        else:
            sql = "INSERT INTO biblioteca (No, Title, Area, url, `Last_valid_version`, Igall_owner) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (No, Title, Area, url, Last_valid_version, Igall_owner)
            self.cursor.execute(sql, values)
            self.conn.commit()
            return True

    def consultar_documento(self, No):
        self.cursor.execute("SELECT * FROM biblioteca WHERE No =  %s", (No,))
        documento = self.cursor.fetchone()
        self.conn.commit()
        return documento


    def modificar_documento(self, No, Title, Area, url, Last_valid_version, Igall_owner):
        sql = "UPDATE biblioteca SET Title = %s, Area = %s, url = %s, Last_valid_version = %s, Igall_owner = %s WHERE No = %s"
        values = (Title, Area, url, Last_valid_version, Igall_owner, No)

        self.cursor.execute(sql, values)
        self.conn.commit()

        return self.cursor.rowcount > 0

    def mostrar_documentos(self, No):
        self.cursor.execute("SELECT * FROM biblioteca WHERE No = %s", (No,))
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
        self.cursor.execute("DELETE FROM biblioteca WHERE No = %s", (No,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def agregar_linea(self, table_no, igall_no, system_name, structure_component, critical_location_part, material, environment, ageing_effect, degradation_mechanism, document, design):
        self.cursor.execute("SELECT * FROM amrtable WHERE table_no = %s AND igall_no = %s", (table_no, igall_no))
        linea_existe = self.cursor.fetchone()

        if linea_existe:
            return False
        else:
            sql = "INSERT INTO amrtable (id, table_no, igall_no, system_name, structure_component, critical_location_part, material, environment, ageing_effect, degradation_mechanism, document, design) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = ("%s_%s" % (table_no, igall_no), table_no, igall_no, system_name, structure_component, critical_location_part, material, environment, ageing_effect, degradation_mechanism, document, design)
            self.cursor.execute(sql, values)
            self.conn.commit()
            return True

    def eliminar_lineas(self, table_no, igall_no):
        self.cursor.execute("SELECT * FROM amrtable WHERE table_no = %s AND igall_no = %s", (table_no, igall_no))
        linea_existe = self.cursor.fetchone()

        if linea_existe:
            sql = "DELETE FROM amrtable WHERE table_no = %s AND igall_no = %s"
            self.cursor.execute(sql, (table_no, igall_no))
            self.conn.commit()
            return self.cursor.rowcount > 0
        else:
            return False

    def mostrar_lineas(self, table_no=None, igall_no=None, system_name=None, structure_component=None, critical_location_part=None, material=None, environment=None, ageing_effect=None, degradation_mechanism=None, document=None, design=None):
        sql = "SELECT amrtable.*, biblioteca.url FROM amrtable LEFT JOIN biblioteca ON amrtable.document = biblioteca.No WHERE 1=1"
        conditions = []
        values = []

        if table_no is not None:
            conditions.append(" AND table_no = %s")
            values.append(table_no)
        if igall_no is not None:
            conditions.append(" AND igall_no = %s")
            values.append(igall_no)
        if system_name is not None:
            conditions.append(" AND system_name = %s")
            values.append(system_name)
        if structure_component is not None:
            conditions.append(" AND structure_component = %s")
            values.append(structure_component)
        if critical_location_part is not None:
            conditions.append(" AND critical_location_part = %s")
            values.append(critical_location_part)
        if material is not None:
            conditions.append(" AND material = %s")
            values.append(material)
        if environment is not None:
            conditions.append(" AND environment = %s")
            values.append(environment)
        if ageing_effect is not None:
            conditions.append(" AND ageing_effect = %s")
            values.append(ageing_effect)
        if degradation_mechanism is not None:
            conditions.append(" AND degradation_mechanism = %s")
            values.append(degradation_mechanism)
        if document is not None:
            conditions.append(" AND document = %s")
            values.append(document)
        if design is not None:
            conditions.append(" AND `design` = %s")
            values.append(design)

        if conditions:
            sql += " ".join(conditions)

        self.cursor.execute(sql, values)
        lineas = self.cursor.fetchall()
        return lineas

BIBLIOTECA = Biblioteca(host='Celinaetienot.mysql.pythonanywhere-services.com', user='Celinaetienot', password='JaPaCe2023', database='Celinaetienot$IGALL')

ruta_destino = '/home/Celinaetienot/mysite/static/documents/'

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
        return "Documento no encontrado", 404

@app.route("/documentos", methods=["POST"])
def agregar_documento():
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

        url = os.path.join(ruta_destino, documento['url'])
        if os.path.exists(url):
            os.remove(url)

        if BIBLIOTECA.eliminar_documento(No):
            print("Documento eliminado correctamente")
            return jsonify({"mensaje": "Documento eliminado correctamente"}), 200
        else:
            print("Error interno al eliminar el documento de la biblioteca")
            return jsonify({"mensaje": "Error al eliminar el documento"}), 500

    else:
        return jsonify({"mensaje": "Documento no encontrado"}), 404

@app.route("/lineas", methods=["GET"])
def mostrar_lineas():
    table_no = request.args.get('table_no')
    igall_no = request.args.get('igall_no')
    system_name = request.args.get('system_name')
    structure_component = request.args.get('structure_component')
    critical_location_part = request.args.get('critical_location_part')
    material = request.args.get('material')
    environment = request.args.get('environment')
    ageing_effect = request.args.get('ageing_effect')
    degradation_mechanism = request.args.get('degradation_mechanism')
    document = request.args.get('document')
    design = request.args.get('design')

    lineas = BIBLIOTECA.mostrar_lineas(
        table_no, igall_no, system_name, structure_component, critical_location_part,
        material, environment, ageing_effect, degradation_mechanism, document, design
    )

    if lineas:
        return jsonify(lineas)
    else:
        return "No se encontraron registros con esos parámetros", 404

if __name__ == "__main__":
    app.run(debug=True)

    
#Database host address:Celinaetienot.mysql.pythonanywhere-services.com
#User:Celinaetienot
#password: JaPaCe2023
#Database:Celinaetienot$IGALL
#ruta_documentos:'/home/Celinaetienot/mysite/static/documents/'
