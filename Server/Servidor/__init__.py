from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Lista para almacenar los datos recibidos
data_store = []

# Diccionario: claves esperadas para cada tipo de datos.
expected_keys_by_type = {
    "body_position": ["pose_landmarks", "face_landmarks", "left_hand_landmarks", "right_hand_landmarks"],
    "squat_counter": ["angle", "contador"],
    "hand_signs": ["letter", "finger_coordinates"],
    "flexiones": ["contador", "angulo_izquierdo", "angulo_derecho"]
}

# Validamos la estructura de los datos
def validate_data(data):
    data_type = data.get('type', 'body_position')
    expected_keys = expected_keys_by_type.get(data_type, [])

    # Verifica que todas las claves esperadas estén presentes
    if not all(key in data for key in expected_keys):
        return False

    # Validación específica para 'squat_counter'
    if data_type == 'squat_counter':
        angle = data.get('angle')
        contador = data.get('contador')
        # Comprueba que 'angle' sea numérico y 'contador' un entero
        if not (isinstance(angle, (int, float)) and isinstance(contador, int)):
            return False

    # Validación específica para 'hand_signs'
    if data_type == 'hand_signs':
        letter = data.get('letter')
        finger_coordinates = data.get('finger_coordinates')
        # Comprueba que 'letter' sea una cadena y 'finger_coordinates' un diccionario
        if not (isinstance(letter, str) and isinstance(finger_coordinates, dict)):
            return False
        # Comprueba que las coordenadas sean números flotantes
        for finger, coords in finger_coordinates.items():
            if not ('x' in coords and 'y' in coords and isinstance(coords['x'], float) and isinstance(coords['y'], float)):
                return False

    # Validación específica para 'flexiones'
    elif data_type == 'flexiones':
        contador = data.get('contador')
        angulo_izquierdo = data.get('angulo_izquierdo')
        angulo_derecho = data.get('angulo_derecho')
        if not (isinstance(contador, int) and isinstance(angulo_izquierdo, (int, float)) and isinstance(angulo_derecho,
                                                                                                        (int, float))):
            return False

    return True

# Ruta para subir datos
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
