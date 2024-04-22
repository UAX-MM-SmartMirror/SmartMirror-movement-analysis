from flask import Flask, request, jsonify, make_response
from datetime import datetime

from Python.AnalisisMovimientoServidor.VariablesComun import tipo_ejercicio
import time

app = Flask(__name__)
app.config ['DEBUG'] = False

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Methods'] = 'GET, POST'
    header['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


# Lista para almacenar los datos recibidos
data_store = []
# Diccionario: claves esperadas para cada tipo de datos.
expected_keys_by_type = {
    "body_position": ["pose_landmarks", "face_landmarks", "left_hand_landmarks", "right_hand_landmarks"],
    "squat_counter": ["angle", "contador"],
    "hand_signs": ["letter", "finger_coordinates"],
    "flexiones": ["contador", "angulo_izquierdo", "angulo_derecho"],
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
        if not (isinstance(angle, float) and isinstance(contador, int)):
            return False

    if data_type == 'hand_signs':
        letter = data.get('letter')
        finger_coordinates = data.get('finger_coordinates')
        if not (isinstance(letter, str) and isinstance(finger_coordinates, dict)):
            return False
        for finger, coords in finger_coordinates.items():
            if not ('x' in coords and 'y' in coords and isinstance(coords['x'], float) and isinstance(coords['y'],
                                                                                                      float)):
                return False

    if data_type == 'biceps':
        contador = data.get('contador')
        angulo = data.get('angulo_codo')
        if not (isinstance(contador, int) and isinstance(angulo, (int, float))):
            return False

    if data_type == 'flexiones':
        contador = data.get('contador')
        angulo_izq = data.get('angulo_izquierdo')
        angulo_der = data.get('angulo_derecho')
        # angulo_body_izq = data.get('angulo_cuerpo_izquierdo')
        # angulo_body_der = data.get('angulo_cuerpo_derecho')
        if not (isinstance(contador, int) and isinstance(angulo_izq, (int, float)) and isinstance(angulo_der, (int,
                                                                                                               float))):
            return False

    if data_type == 'analisis_movimiento':
        biceps = data.get('biceps')
        flexiones = data.get('flexiones')
        sentadillas = data.get('sentadillas')
        if not (isinstance(biceps, int) and isinstance(flexiones, int) and isinstance(sentadillas, int)):
            return False

    if data_type == 'face_mesh':
        face_landmarks = data.get('face_landmarks')
        if not (isinstance(face_landmarks, list)):
            return False

    return True


@app.route('/upload', methods=['POST'])
def upload_data():
    data = request.json
    print("Datos recibidos:", data)
    if not data or not validate_data(data):
        print("Validación fallida para:", data)
        return jsonify({"error": "Invalid or missing data"}), 400

    data['timestamp'] = datetime.utcnow().isoformat() + 'Z'
    data_store.append(data)
    return jsonify({"message": "Data uploaded successfully"}), 200

@app.route('/data', methods=['GET'])
def get_data():
    data_type = request.args.get('type')
    print(f"Tipo de dato recibido: {data_type}")
    filtered_data = data_store

    # Espera hasta que haya datos disponibles
    while not filtered_data:
        time.sleep(0.1)  # Espera 0.1 segundos antes de comprobar de nuevo
        filtered_data = [entry for entry in data_store if entry.get('type') == data_type]

    return jsonify(filtered_data), 200

@app.route('/start/<exercise_type>', methods=['POST', 'GET'])
def start_exercise(exercise_type):
    tipo_ejercicio.put(exercise_type)
    print(f"Tipo de ejercicio: {exercise_type}")
    return jsonify({"message": f"{exercise_type.capitalize()}, started"}), 200

@app.route('/start/stop', methods=['POST'])
def stop():
    tipo_ejercicio['type'] = 'stop'
    return jsonify({"message": "All counters stopped"}), 200

def lanzar_servidor():
    app.run(debug=False, port=5000, use_reloader=False)


if __name__ == '__main__':
    lanzar_servidor()
