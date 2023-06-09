from flask import Flask, render_template, jsonify, url_for
import datetime
import base64
import requests
import psycopg2

app = Flask(__name__)

host = "c.clu.postgres.database.azure.com"
dbname = "citus"
port = "5432"
user = "citus"
password = "Admin1234"
sslmode = "require"


def create_connection():
    connection = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password,
        sslmode=sslmode

    )
    return connection


@app.route('/main')
def main_content():
    # Realiza una solicitud GET a la ruta /menu
    response = requests.get('http://localhost:4000/menu')

    # Verifica si la solicitud fue exitosa (código de respuesta 200)
    if response.status_code == 200:
        # Obtiene los datos del menú en formato JSON
        menu_data = response.json()

        # Renderiza el archivo mainContent.html y pasa los datos del menú como argumento
        return render_template('mainContent.html', menu=menu_data)
    
    else:
        # Si la solicitud no fue exitosa, muestra un mensaje de error
        return 'Error al obtener el menú del día'


        

@app.route('/menu')
def obtener_menu_dia():
    # Obten la fecha actual
    fecha_actual = datetime.datetime.now()  # Utiliza la fecha actual en lugar de una fecha fija

    try:
        # Crea un cursor para ejecutar consultas
        connection = create_connection()
        cursor = connection.cursor()
        # Ejecuta la consulta para obtener el menu del dia
        cursor.execute("""
            SELECT m.Fecha,
                   d.Bebida, d.Fruta, d.Acompanamiento,
                   a.Entrada, a.Refresco, a.PlatoFondo, a.Fruta,
                   c.PlatoFondo, c.Refresco, c.Postre
            FROM Menu m
            JOIN Desayuno d ON m.ID = d.MenuID
            JOIN Almuerzo a ON m.ID = a.MenuID
            JOIN Cena c ON m.ID = c.MenuID
            WHERE m.Fecha = %s
        """, (fecha_actual,))

        # Obtiene los resultados de la consulta
        menu = cursor.fetchone()

        # Verifica si se encontró el menú del día
        if menu is None:
            return jsonify({'mensaje': 'No se encontró el menú del día'})

        # Convierte los datos del menú en un diccionario
        menu_dict = {
            'fecha': str(menu[0]),
            'desayuno': {
                'bebida': menu[1],
                'fruta': menu[2],
                'acompanamiento': menu[3],
            },
            'almuerzo': {
                'entrada': menu[5],
                'refresco': menu[6],
                'plato_fondo': menu[7],
                'fruta': menu[8],
            },
            'cena': {
                'plato_fondo': menu[10],
                'refresco': menu[11],
                'postre': menu[12],
               
            }
        }

        # Devuelve el menú del día en formato JSON
        return jsonify(menu_dict)

    except psycopg2.Error as e:
        return jsonify({'error': str(e)})



@app.route('/ticket')
def ticket():
    return render_template('Ticket.html')

@app.route("/")
def index():
    return render_template('Login.html')


@app.route('/register')
def register():
    return render_template('Register.html')


if __name__ == "__main__":
    app.run()
