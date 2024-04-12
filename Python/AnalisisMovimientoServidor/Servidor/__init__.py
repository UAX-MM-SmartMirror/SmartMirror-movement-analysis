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
    "flexiones": ["contador", "angulo"],
    "biceps": ["contador", "angulo_codo"],
    "face_mesh": ["face_landmarks"]
}

def validate_data(data):
    data_type = data.get('type', 'body_position')
    expected_keys = expected_keys_by_type.get(data_type, [])

    if not all(key in data for key in expected_keys):
        return False

    if data_type == 'squat_counter':
        angle = data.get('angle')
        contador = data.get('contador')
        if not (isinstance(angle, (int, float)) and isinstance(contador, int)):
            return False

    if data_type == 'hand_signs':
        letter = data.get('letter')
        finger_coordinates = data.get('finger_coordinates')
        if not (isinstance(letter, str) and isinstance(finger_coordinates, dict)):
            return False
        for finger, coords in finger_coordinates.items():
            if not ('x' in coords and 'y' in coords and isinstance(coords['x'], float) and isinstance(coords['y'], float)):
                return False

    if data_type == 'biceps':
        contador = data.get('contador')
        angulo = data.get('angulo_codo')
        if not (isinstance(contador, int) and isinstance(angulo, (int, float))):
            return False

    if data_type == 'flexiones':
        contador = data.get('contador')
        angulo = data.get('angulo')
        if not (isinstance(contador, int) and isinstance(angulo, (int, float))):
            return False

    if data_type == 'face_mesh':
        face_landmarks = data.get('face_landmarks')
        if not (isinstance(face_landmarks, list)):
            return False

    return True

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
    data_type = request.args.get('type')
    filtered_data = data_store

    # Filtramos por tipo de dato si se especifica
    if data_type:
        filtered_data = [entry for entry in filtered_data if entry.get('type') == data_type]

    return jsonify(filtered_data), 200

def lanzar_servidor():
    app.run(debug=False, port=5000, use_reloader=False)

if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)
