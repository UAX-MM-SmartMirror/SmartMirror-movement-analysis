# Importación de bibliotecas necesarias para el procesamiento de imagen y cálculos matemáticos.
import mediapipe as mp
import cv2
import numpy as np
from math import acos, degrees

# Inicialización de las soluciones de dibujo y postura de MediaPipe, junto con la captura de video de OpenCV.
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
cap = cv2.VideoCapture(0)

# Inicialización de variables para el control del conteo de las repeticiones del ejercicio.
up = False
down = False
contador = 0

# Configuración de la detección de postura con parámetros específicos.
with mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5) as pose:
    # Bucle para leer y procesar cada frame capturado por la cámara web.
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Preprocesamiento del frame para la detección de postura.
        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1)  # Voltear el frame horizontalmente para una vista especular.
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Conversión de BGR a RGB.
        results = pose.process(frame_rgb)

        # Si se detectan landmarks (puntos de referencia) de postura en el frame, se procede con el siguiente bloque.
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

            # Calcular ángulo del codo utilizando el producto punto y la norma de los vectores.
            angle = degrees(acos(np.dot(np.array(shoulder) - np.array(elbow), np.array(wrist) - np.array(elbow)) /
                                (np.linalg.norm(np.array(shoulder) - np.array(elbow)) * np.linalg.norm(np.array(wrist) - np.array(elbow)))))

            # Lógica para contar las repeticiones basado en el ángulo del codo.
            if angle >= 160:
                up = True
            if up and angle <= 70:
                down = True
            if up and down and angle >= 160:
                contador += 1  # Incremento del contador de repeticiones.
                up = False
                down = False

            # Mostrar el número de repeticiones en el frame.
            cv2.putText(frame, f"Repeticiones: {contador}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # cv2.imshow("Frame", frame) # Esta línea está comentada en el código original.
        print ("Repeticiones: ", contador) # Imprimir el contador de repeticiones en la consola.
        if cv2.waitKey(1) & 0xFF == 27:
            break

# Liberación de la cámara y destrucción de todas las ventanas abiertas por OpenCV al terminar el bucle.
cap.release()
cv2.destroyAllWindows()