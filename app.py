from flask import Flask, request, jsonify, render_template_string
import csv
import os
from datetime import datetime

app = Flask(__name__)

# Ruta para guardar los datos
@app.route('/save_data', methods=['POST'])
def save_data():
    data = request.json  # Datos enviados desde el frontend

    if data:
        file_exists = os.path.isfile('data_log.csv')
        with open('data_log.csv', 'a', newline='') as file:
            writer = csv.writer(file)

            # Si el archivo no existe, agregar el encabezado
            if not file_exists:
                writer.writerow(['Sistema Operativo', 'Navegador', 'Tipo de Dispositivo', 'Resolución', 'Idioma', 'Zona Horaria', 'IP', 'Fecha'])

            # Agregar los datos
            writer.writerow([
                data.get('os'),
                data.get('browser'),
                data.get('device'),
                data.get('resolution'),
                data.get('language'),
                data.get('timezone'),
                data.get('ip'),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ])
    
    return jsonify({"status": "success"}), 200

# Nueva ruta para mostrar los datos del CSV
@app.route('/datos')
def datos():
    # Leer el archivo CSV
    if os.path.isfile('data_log.csv'):
        with open('data_log.csv', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)  # Convertir el archivo CSV en una lista de filas

            # Generar una tabla HTML a partir de los datos del CSV
            table = "<table border='1'>"
            for row in rows:
                table += "<tr><td>" + "</td><td>".join(row) + "</td></tr>"
            table += "</table>"

            return render_template_string(f"""
                <html>
                    <head><title>Datos de Visitantes</title></head>
                    <body>
                        <h1>Datos de los visitantes</h1>
                        {table}
                    </body>
                </html>
            """)
    else:
        return "No se ha registrado ningún dato aún."

if __name__ == '__main__':
    app.run(debug=True)
