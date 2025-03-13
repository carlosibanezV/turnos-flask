from flask import Flask, request, render_template_string
import pandas as pd

app = Flask(__name__)

# Cargar datos desde el archivo Excel
def cargar_datos():
    file_path = "lista_de_turnos.xlsx"  # Asegúrate de que el archivo esté en la misma carpeta que app.py
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip().str.lower()  # Elimina espacios y convierte nombres a minúsculas
    return df

# Plantilla HTML básica para mostrar el formulario y los resultados
template = """
<!DOCTYPE html>
<html>
<head>
    <title>Consulta de Turnos</title>
</head>
<body>
    <h2>Ingrese su RUT para ver sus turnos</h2>
    <form method="post">
        RUT: <input type="text" name="rut" required>
        <input type="submit" value="Consultar">
    </form>
    {% if turnos %}
        <h3>Turnos de {{ nombre }}</h3>
        <table border="1">
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