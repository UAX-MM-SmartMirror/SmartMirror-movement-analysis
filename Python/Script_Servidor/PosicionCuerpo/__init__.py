import cv2
import mediapipe as mp
import numpy as np
import requests  # Para realizar peticiones HTTP

# Inicialización de MediaPipe Holistic para detección de pose, manos y rostro
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

# Función para enviar datos al servidor
def send_data_to_server(data):
    url = 'http://localhost:5000/upload'  # URL del servidor
    try:
        # Para cada tipo de landmarks, imprime su descripción y las coordenadas
        if data.get("pose_landmarks"):
            print("Pose Landmarks: ", data["pose_landmarks"])
        if data.get("face_landmarks"):
            print("Cara Landmarks: ", data["face_landmarks"])
        if data.get("left_hand_landmarks"):
            print("Mano Iquierda Landmarks: ", data["left_hand_landmarks"])
        if data.get("right_hand_landmarks"):
            print("Mano Derecha Landmarks: ", data["right_hand_landmarks"])

        # Enviar los datos al servidor
        response = requests.post(url, json=data)
        print(f"Respuesta del servidor: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión al servidor: {e}")
    except Exception as e:
        print(f"Error general al enviar datos: {e}")


# Función para extraer coordenadas de landmarks
def get_landmark_coordinates(landmarks, image_width, image_height):
    if landmarks is None:
        return None
    return [{
        "x": landmark.x * image_width,
        "y": landmark.y * image_height,
        "z": landmark.z * image_width
    } for landmark in landmarks.landmark]

# Procesamiento de la entrada de la webcam
cap = cv2.VideoCapture(0)  # Inicio de la captura de vídeo
if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        success, image = cap.read()  # Lectura de cada frame
        if not success:
            print("Error: No se pudo obtener un frame de la cámara.")
            break  # Salir del bucle si no hay frames

        # Procesamiento del frame actual
        image_height, image_width, _ = image.shape
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = holistic.process(image)

        # Preparar datos de landmarks detectados para enviar
        pose_landmarks = get_landmark_coordinates(results.pose_landmarks, image_width, image_height)
        face_landmarks = get_landmark_coordinates(results.face_landmarks, image_width, image_height)
        left_hand_landmarks = get_landmark_coordinates(results.left_hand_landmarks, image_width, image_height)
        right_hand_landmarks = get_landmark_coordinates(results.right_hand_landmarks, image_width, image_height)

        # Crear un diccionario con toda la información recopilada
        data_to_send = {
            "pose_landmarks": pose_landmarks,
            "face_landmarks": face_landmarks,
            "left_hand_landmarks": left_hand_landmarks,
            "right_hand_landmarks": right_hand_landmarks
        }

        # Envío de datos al servidor
        send_data_to_server(data_to_send)

        if cv2.waitKey(1) & 0xFF == 27:  # Salir con la tecla ESC
            break

cap.release()  # Liberación de la cámara
cv2.destroyAllWindows()  # Cerrar todas las ventanas abiertas
