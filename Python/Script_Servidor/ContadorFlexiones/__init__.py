import mediapipe as mp
import cv2
import numpy as np
from math import acos, degrees
import requests

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
cap = cv2.VideoCapture(0)

# Variables para el estado de las flexiones
up = False
down = False
contador = 0

# URL del servidor
url = 'http://localhost:5000/upload'

with mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5) as pose:
    while True:
        try:
            ret, frame = cap.read()
            if not ret:
                raise ValueError("No se pudo capturar el frame de la cámara.")

            height, width, _ = frame.shape
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(frame_rgb)

            if results.pose_landmarks is not None:
                # Extracción de puntos para los brazos izquierdo y derecho
                shoulder_left = (
                int(results.pose_landmarks.landmark[11].x * width), int(results.pose_landmarks.landmark[11].y * height))
                elbow_left = (
                int(results.pose_landmarks.landmark[13].x * width), int(results.pose_landmarks.landmark[13].y * height))
                wrist_left = (
                int(results.pose_landmarks.landmark[15].x * width), int(results.pose_landmarks.landmark[15].y * height))

                shoulder_right = (
                int(results.pose_landmarks.landmark[12].x * width), int(results.pose_landmarks.landmark[12].y * height))
                elbow_right = (
                int(results.pose_landmarks.landmark[14].x * width), int(results.pose_landmarks.landmark[14].y * height))
                wrist_right = (
                int(results.pose_landmarks.landmark[16].x * width), int(results.pose_landmarks.landmark[16].y * height))

                # Cálculo de ángulos para ambos codos
                angle_left = degrees(acos(
                    np.dot(np.array(shoulder_left) - np.array(elbow_left), np.array(wrist_left) - np.array(elbow_left)) /
                    (np.linalg.norm(np.array(shoulder_left) - np.array(elbow_left)) * np.linalg.norm(
                        np.array(wrist_left) - np.array(elbow_left)))))

                angle_right = degrees(acos(np.dot(np.array(shoulder_right) - np.array(elbow_right),
                                                  np.array(wrist_right) - np.array(elbow_right)) /
                                           (np.linalg.norm(
                                               np.array(shoulder_right) - np.array(elbow_right)) * np.linalg.norm(
                                               np.array(wrist_right) - np.array(elbow_right)))))

                # Contar flexiones y enviar datos cuando corresponda
                if angle_left >= 160 and angle_right >= 160:
                    up = True
                if up and (angle_left <= 70 or angle_right <= 70):
                    down = True
                if up and down and angle_left >= 160 and angle_right >= 160:
                    contador += 1
                    up = False
                    down = False

                    # Preparación de los datos para enviar
                    data = {
                        'type': 'flexiones',
                        'contador': contador,
                        'angulo_izquierdo': angle_left,
                        'angulo_derecho': angle_right
                    }

                    # Envío de los datos al servidor
                    try:
                        response = requests.post(url, json=data)
                        print("Datos enviados al servidor:", data)
                        print("Respuesta del servidor:", response.text)
                    except requests.exceptions.RequestException as e:
                        print("Error al enviar datos:", e)

                # Mostrar el contador de flexiones en el frame
                cv2.putText(frame, f"Count: {contador}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # Mostrar el frame procesado en una ventana
            cv2.imshow("Frame", frame)

            # Esperar por la tecla ESC para salir del bucle
            if cv2.waitKey(1) & 0xFF == 27:
                break
        except Exception as ex:
            print("Se produjo un error:", ex)

# Liberar la cámara y destruir todas las ventanas creadas
cap.release()
cv2.destroyAllWindows()