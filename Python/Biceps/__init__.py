import mediapipe as mp
import cv2
import numpy as np
from math import acos, degrees

# Inicialización de Mediapipe y OpenCV
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
cap = cv2.VideoCapture(0)

# Variables para el control del conteo
up = False
down = False
contador = 0

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
            # Dibujar puntos de referencia
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Obteniendo puntos de referencia para el brazo derecho (o izquierdo si sostiene la mancuerna)
            shoulder = (int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * width),
                        int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * height))
            elbow = (int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].x * width),
                     int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].y * height))
            wrist = (int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x * width),
                     int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y * height))

            # Calcular ángulo del codo
            angle = degrees(acos(np.dot(np.array(shoulder) - np.array(elbow), np.array(wrist) - np.array(elbow)) /
                                (np.linalg.norm(np.array(shoulder) - np.array(elbow)) * np.linalg.norm(np.array(wrist) - np.array(elbow)))))

            # Lógica para contar las repeticiones
            if angle >= 160:
                up = True
            if up and angle <= 70:
                down = True
            if up and down and angle >= 160:
                contador += 1
                up = False
                down = False

            # Visualización
            cv2.putText(frame, f"Repeticiones: {contador}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # cv2.imshow("Frame", frame)
        print ("Repeticiones: ", contador)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()