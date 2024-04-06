from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Estructura de almacenamiento para los datos recibidos
data_store = []

# Validación de la estructura de datos esperada
def validate_data(data):
    expected_keys = ["pose_landmarks", "face_landmarks", "left_hand_landmarks", "right_hand_landmarks"]
    return all(key in data for key in expected_keys)

@app.route('/upload', methods=['POST'])
def upload_data():
    data = request.json
    if not data or not validate_data(data):
        return jsonify({"error": "Invalid or missing data"}), 400

    # Añadimos un timestamp a los datos recibidos
    data['timestamp'] = datetime.utcnow().isoformat() + 'Z'  # Z indica UTC
    data_store.append(data)
    return jsonify({"message": "Data uploaded successfully"}), 200

@app.route('/data', methods=['GET'])
def get_data():
    # Filtros opcionales para tipo de landmark y rango de tiempo
    landmark_type = request.args.get('type')
    start_time = request.args.get('start')
    end_time = request.args.get('end')

    filtered_data = data_store

    # Filtramos por tipo de landmark si se especifica
    if landmark_type:
        filtered_data = [entry for entry in filtered_data if entry.get(landmark_type)]

    # Filtramos por rango de tiempo si se especifican ambos, start y end
    if start_time and end_time:
        start = datetime.fromisoformat(start_time)
        end = datetime.fromisoformat(end_time)
        filtered_data = [entry for entry in filtered_data if start <= datetime.fromisoformat(entry['timestamp']) <= end]

    return jsonify(filtered_data), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
