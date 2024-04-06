# Importar las librerías necesarias para el procesamiento de imágenes, cálculo numérico y envío de datos
import mediapipe as mp
import cv2
import numpy as np
from math import acos, degrees
import requests

# Inicializar el módulo de dibujo y el módulo de postura de MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Inicializar la captura de video desde la cámara web
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: No se pudo acceder a la cámara web.")
    exit()

# Variables para controlar el estado de la sentadilla (arriba o abajo) y contarlas
up = False
down = False
contador = 0

# Inicializar el objeto Pose con configuraciones específicas
with mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5) as pose:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: No se pudo leer el frame de la cámara.")
            break

        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = pose.process(frame_rgb)

        if results.pose_landmarks is not None:
            x1, y1 = int(results.pose_landmarks.landmark[24].x * width), int(
                results.pose_landmarks.landmark[24].y * height)
            x2, y2 = int(results.pose_landmarks.landmark[26].x * width), int(
                results.pose_landmarks.landmark[26].y * height)
            x3, y3 = int(results.pose_landmarks.landmark[28].x * width), int(
                results.pose_landmarks.landmark[28].y * height)

            p1, p2, p3 = np.array([x1, y1]), np.array([x2, y2]), np.array([x3, y3])

            l1, l2, l3 = np.linalg.norm(p2 - p3), np.linalg.norm(p1 - p3), np.linalg.norm(p1 - p2)

            angle = degrees(acos((l1 ** 2 + l3 ** 2 - l2 ** 2) / (2 * l1 * l3)))

            if angle >= 160:
                up = True
            if up and not down and angle <= 70:
                down = True
            if up and down and angle >= 160:
                contador += 1
                up = False
                down = False

                # Mostrar la información en la consola antes de enviar
                print(f"Ángulo: {angle}, Contador: {contador}")

                data_to_send = {
                    "type": "squat_counter",
                    "angle": angle,
                    "contador": contador,
                }

                try:
                    response = requests.post('http://localhost:5000/upload', json=data_to_send)
                    print(f"Respuesta del servidor: {response.json()}")
                except Exception as e:
                    print(f"Error al enviar datos: {e}")

        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # Presionar ESC para salir
            break

cap.release()
cv2.destroyAllWindows()

