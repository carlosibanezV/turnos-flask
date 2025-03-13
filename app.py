from flask import Flask, request, render_template_string
import pandas as pd

app = Flask(__name__)

# Cargar datos desde el archivo Excel
def cargar_datos():
    file_path = "lista_de_turnos.xlsx"  # Asegúrate de que el archivo esté en la misma carpeta que app.py
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip().str.lower()  # Elimina espacios y convierte nombres a minúsculas
    return df

# Plantilla HTML mejorada con estilos CSS para hacerla más atractiva
template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Consulta de Turnos</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            text-align: center;
            padding: 50px;
        }
        .container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            max-width: 500px;
            margin: auto;
        }
        h2 {
            color: #333;
        }
        input {
            padding: 10px;
            width: 80%;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            background-color: #28a745;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #218838;
        }
        table {
            width: 100%;
            margin-top: 20px;
            border-collapse: collapse;
        }
        th, td {
            padding: 10px;
            border: 1px solid #ddd;
        }
        th {
            background-color: #28a745;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Ingrese su RUT (con puntos y guión) para ver sus turnos</h2>
        <form method="post">
            <input type="text" name="rut" placeholder="Ejemplo: 12.345.678-9" required>
            <button type="submit">Consultar</button>
        </form>
        {% if turnos %}
            <h3>Turnos de {{ nombre }}</h3>
            <table>
                <tr>
                    <th>Nombre</th>
                    <th>Turno</th>
                    <th>Inicio</th>
                    <th>Fin</th>
                </tr>
                {% for turno in turnos %}
                <tr>
                    <td>{{ turno["nombre"] }}</td>
                    <td>{{ turno["turno"] }}</td>
                    <td>{{ turno["inicio"] }}</td>
                    <td>{{ turno["fin"] }}</td>
                </tr>
                {% endfor %}
            </table>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    turnos = []
    nombre = ""
    if request.method == "POST":
        rut = request.form.get("rut", "").strip()
        df = cargar_datos()
        if "rut" in df.columns:
            datos_filtrados = df[df["rut"].astype(str).str.contains(rut, case=False, na=False)]
            turnos = datos_filtrados.to_dict(orient="records")
            if turnos:
                nombre = turnos[0]["nombre"]  # Tomar el nombre de la primera coincidencia
    
    return render_template_string(template, turnos=turnos, nombre=nombre)

if __name__ == "__main__":
    app.run(debug=True)
