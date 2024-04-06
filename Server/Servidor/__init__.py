from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Estructura de almacenamiento para los datos recibidos
data_store = []

# Diccionario que mapea tipo de dato a claves esperadas
expected_keys_by_type = {
    "body_position": ["pose_landmarks", "face_landmarks", "left_hand_landmarks", "right_hand_landmarks"],
    "squat_counter": ["angle", "contador"],
}

# Validación de la estructura de datos esperada
def validate_data(data):
    # Determinar el tipo de dato
    data_type = data.get('type', 'body_position')  # Asume 'body_position' como tipo por defecto si no se especifica

    # Obtener las claves esperadas para el tipo de dato
    expected_keys = expected_keys_by_type.get(data_type, [])

    # Verificar que todas las claves esperadas están presentes
    return all(key in data for key in expected_keys)

@app.route('/upload', methods=['POST'])
def upload_data():
    data = request.json
    if not data or not validate_data(data):
        return jsonify({"error": "Invalid or missing data"}), 400

    # Añadir un timestamp a los datos recibidos
    data['timestamp'] = datetime.utcnow().isoformat() + 'Z'
    data_store.append(data)
    return jsonify({"message": "Data uploaded successfully"}), 200

@app.route('/data', methods=['GET'])
def get_data():
    # Filtros opcionales para tipo de dato y rango de tiempo
    data_type = request.args.get('type')
    start_time = request.args.get('start')
    end_time = request.args.get('end')

    filtered_data = data_store

    # Filtrar por tipo de dato si se especifica
    if data_type:
        filtered_data = [entry for entry in filtered_data if entry.get('type') == data_type]

    # Filtrar por rango de tiempo si se especifican tanto el inicio como el fin
    if start_time and end_time:
        start = datetime.fromisoformat(start_time)
        end = datetime.fromisoformat(end_time)
        filtered_data = [entry for entry in filtered_data if start <= datetime.fromisoformat(entry['timestamp']) <= end]

    return jsonify(filtered_data), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
