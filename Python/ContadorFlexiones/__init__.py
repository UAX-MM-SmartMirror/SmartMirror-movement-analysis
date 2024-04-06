# Importación de las librerías necesarias para el procesamiento de imagen y cálculos matemáticos.
import mediapipe as mp
import cv2
import numpy as np
from math import acos, degrees

# Inicialización de los módulos de MediaPipe para dibujo y detección de posturas.
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Inicialización de la captura de video a través de la cámara web predeterminada.
cap = cv2.VideoCapture(0)

# Variables de control para el estado de las flexiones.
up = False
down = False
contador = 0

# Creación del objeto Pose de MediaPipe para el seguimiento de la postura con configuraciones específicas.
with mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5) as pose:
    # Bucle para leer y procesar cada frame capturado por la cámara web.
    while True:
        ret, frame = cap.read()
        # Si no hay frame, salir del bucle.
        if not ret:
            break

        # Obtener las dimensiones del frame y ajustar la imagen.
        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1)  # Voltear el frame horizontalmente.
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convertir de BGR a RGB.

        # Procesamiento del frame para detectar la postura con MediaPipe.
        results = pose.process(frame_rgb)

        # Si se detectan marcas de postura, ejecutar el siguiente bloque de código.
        if results.pose_landmarks is not None:
            # Puntos para el brazo izquierdo
            shoulder_left = (
            int(results.pose_landmarks.landmark[11].x * width), int(results.pose_landmarks.landmark[11].y * height))
            elbow_left = (
            int(results.pose_landmarks.landmark[13].x * width), int(results.pose_landmarks.landmark[13].y * height))
            wrist_left = (
            int(results.pose_landmarks.landmark[15].x * width), int(results.pose_landmarks.landmark[15].y * height))

            # Puntos para el brazo derecho
            shoulder_right = (
            int(results.pose_landmarks.landmark[12].x * width), int(results.pose_landmarks.landmark[12].y * height))
            elbow_right = (
            int(results.pose_landmarks.landmark[14].x * width), int(results.pose_landmarks.landmark[14].y * height))
            wrist_right = (
            int(results.pose_landmarks.landmark[16].x * width), int(results.pose_landmarks.landmark[16].y * height))

            # Calcular ángulos para ambos codos
            angle_left = degrees(acos(
                np.dot(np.array(shoulder_left) - np.array(elbow_left), np.array(wrist_left) - np.array(elbow_left)) /
                (np.linalg.norm(np.array(shoulder_left) - np.array(elbow_left)) * np.linalg.norm(
                    np.array(wrist_left) - np.array(elbow_left)))))

            angle_right = degrees(acos(np.dot(np.array(shoulder_right) - np.array(elbow_right),
                                              np.array(wrist_right) - np.array(elbow_right)) /
                                       (np.linalg.norm(
                                           np.array(shoulder_right) - np.array(elbow_right)) * np.linalg.norm(
                                           np.array(wrist_right) - np.array(elbow_right)))))

            # Contar flexiones
            if angle_left >= 160 and angle_right >= 160:
                up = True
            if up and (angle_left <= 70 or angle_right <= 70):
                down = True
            if up and down and angle_left >= 160 and angle_right >= 160:
                contador += 1
                up = False
                down = False

            # Mostrar el contador de flexiones en el frame.
            cv2.putText(frame, f"Count: {contador}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
                        cv2.LINE_AA)
        # Mostrar el frame procesado en una ventana.
        cv2.imshow("Frame", frame)
        # Esperar por la tecla ESC para salir del bucle.
        if cv2.waitKey(1) & 0xFF == 27:
            break

# Liberar la cámara y destruir todas las ventanas creadas.
cap.release()
cv2.destroyAllWindows()