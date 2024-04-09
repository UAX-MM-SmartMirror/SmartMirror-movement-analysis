import mediapipe as mp
import cv2
import numpy as np
from math import acos, degrees
import requests

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
cap = cv2.VideoCapture(0)

up = False
down = False
contador = 0

url = 'http://localhost:5000/upload'

with mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5) as pose:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks is not None:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            shoulder = (int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * width),
                        int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * height))
            elbow = (int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].x * width),
                     int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].y * height))
            wrist = (int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x * width),
                     int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y * height))

            angle = degrees(acos(np.dot(np.array(shoulder) - np.array(elbow), np.array(wrist) - np.array(elbow)) /
                                (np.linalg.norm(np.array(shoulder) - np.array(elbow)) * np.linalg.norm(np.array(wrist) - np.array(elbow)))))

            if angle >= 160:
                up = True
            if up and angle <= 70:
                down = True
            if up and down and angle >= 160:
                contador += 1
                up = False
                down = False

                # Preparación de los datos
                data = {
                    'type': 'biceps',
                    'contador': contador,
                    'angulo_codo': angle
                }

                # Envío de los datos al servidor
                try:
                    response = requests.post(url, json=data)
                    print("Datos enviados al servidor:", data)
                    print("Respuesta del servidor:", response.text)
                except requests.exceptions.RequestException as e:
                    print("Error al enviar datos:", e)

            cv2.putText(frame, f"Repeticiones: {contador}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
