from flask import Flask, jsonify, render_template
import pyodbc
import webbrowser
import json
import base64

app = Flask(__name__)


conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-2CVMTJT\SQLEXPRESS;'
                      'Database=MenuCatalog;'
                      'Trusted_Connection=yes;')

@app.route('/menu')
def obtener_menu_dia():
    # Obten la fecha actual
    fecha_actual = '2023-05-24'  # Aqui puedes utilizar la fecha actual en lugar de una fecha fija

    try:
        # Crea un cursor para ejecutar consultas
        cursor = conn.cursor()

        # Ejecuta la consulta para obtener el menu del dia
        cursor.execute("""
            SELECT m.Fecha,
                   d.Bebida, d.Fruta, d.Acompanamiento, d.ImagenDesayuno,
                   a.Entrada, a.Refresco, a.PlatoFondo, a.Fruta, a.ImagenAlmuerzo,
                   c.PlatoFondo, c.Refresco, c.Postre, c.ImagenCena
            FROM Menu m
            JOIN Desayuno d ON m.ID = d.MenuID
            JOIN Almuerzo a ON m.ID = a.MenuID
            JOIN Cena c ON m.ID = c.MenuID
            WHERE m.Fecha = ?
        """, fecha_actual)

        # Obtiene los resultados de la consulta
        menu = cursor.fetchone()

        # Verifica si se encontro el menu del dia
        if menu is None:
            return jsonify({'mensaje': 'No se encontro el menu del dia'})
        #else:
            #return "Se encontro el menu"

        # Convierte los datos del menu en un diccionario
        menu_dict = {
            'fecha': str(menu.Fecha),
            'desayuno': {
                'bebida': menu.Bebida,
                'fruta': menu.Fruta,
                'acompanamiento': menu.Acompanamiento,
                'imagen_desayuno': base64.b64encode(menu.ImagenDesayuno).decode('utf-8')
            },
            'almuerzo': {
                'entrada': menu.Entrada,
                'refresco': menu.Refresco,
                'plato_fondo': menu.PlatoFondo,
                'fruta': menu.Fruta,
                'imagen_almuerzo': base64.b64encode(menu.ImagenAlmuerzo).decode('utf-8')
            },
            'cena': {
                'plato_fondo': menu.PlatoFondo,
                'refresco': menu.Refresco,
                'postre': menu.Postre,
                'imagen_cena': base64.b64encode(menu.ImagenCena).decode('utf-8')
            }
        }
        # Devuelve el menu del dia en formato JSON
        return jsonify(menu_dict)

    except pyodbc.Error as e:
        # Manejo de errores en caso de fallos en la conexion o consulta
        return jsonify({'error': str(e)})


@app.route('/')
def index():
    return render_template('menu.html')

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
