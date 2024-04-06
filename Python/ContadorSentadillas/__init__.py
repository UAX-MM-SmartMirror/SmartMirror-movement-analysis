# Importar las librerías necesarias para el procesamiento de imágenes y cálculo numérico.
import mediapipe as mp
import cv2
import numpy as np
from math import acos, degrees

# Inicializar el módulo de dibujo y el módulo de postura de MediaPipe.
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Inicializar la captura de video desde la cámara web.
cap = cv2.VideoCapture(0)

# Variables para controlar el estado de la sentadilla (arriba o abajo) y contarlas.
up = False
down = False
contador = 0

# Inicializar el objeto Pose con configuraciones específicas.
with mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5) as pose:
    # Bucle infinito para procesar los frames capturados por la cámara web.
    while True:
        ret, frame = cap.read()
        # Si no se captura el frame, romper el bucle.
        if not ret:
            break
        # Obtener dimensiones del frame y voltearlo horizontalmente.
        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1)
        # Convertir el frame de BGR (OpenCV) a RGB (MediaPipe).
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Procesar el frame para detectar la postura.
        results = pose.process(frame_rgb)

        # Si se detectan puntos de referencia de postura, ejecutar el siguiente bloque.
        if results.pose_landmarks is not None:
            # Coordenadas para el cálculo del ángulo de la rodilla.
            x1 = int(results.pose_landmarks.landmark[24].x * width)
            y1 = int(results.pose_landmarks.landmark[24].y * height)

            x2 = int(results.pose_landmarks.landmark[26].x * width)
            y2 = int(results.pose_landmarks.landmark[26].y * height)

            x3 = int(results.pose_landmarks.landmark[28].x * width)
            y3 = int(results.pose_landmarks.landmark[28].y * height)

            # Convertir las coordenadas en arrays de NumPy para facilitar el cálculo.
            p1 = np.array([x1, y1])
            p2 = np.array([x2, y2])
            p3 = np.array([x3, y3])

            # Calcular las longitudes de los lados del triángulo formado por los puntos.
            l1 = np.linalg.norm(p2 - p3)
            l2 = np.linalg.norm(p1 - p3)
            l3 = np.linalg.norm(p1 - p2)

            # Calcular el angulo en la rodilla usando la ley de cosenos.
            angle = degrees(acos((l1 ** 2 + l3 ** 2 - l2 ** 2) / (2 * l1 * l3)))

            # Contar sentadillas basándose en el ángulo de la rodilla
            if angle >= 160:
                up = True
            if up == True and down == False and angle <= 70:
                down = True
            if up == True and down == True and angle >= 160:
                contador += 1
                up = False
                down = False

            # Mostrar el contador y los ángulos calculados en el frame.
            print("count", contador)

            # Dibujar círculos y líneas para visualizar el ángulo calculado.
            cv2.circle(frame, (x1, y1), 6, (0, 255, 255), 4)
            cv2.circle(frame, (x2, y2), 6, (0, 255, 255), 4)
            cv2.circle(frame, (x3, y3), 6, (0, 255, 255), 4)
            aux_image = np.zeros(frame.shape, np.uint8)
            cv2.putText(aux_image, str(int(angle)), (x2 + 30, y2), 1, 1.5, (128, 0, 250), 2)

            cv2.line(aux_image, (x1, y1), (x2, y2), (255, 255, 0), 20)
            cv2.line(aux_image, (x2, y2), (x3, y3), (255, 255, 0), 20)
            cv2.line(aux_image, (x1, y1), (x3, y3), (255, 255, 0), 5)

            contorno = np.array([[x1, y1], [x2, y2], [x3, y3]])
            output = cv2.addWeighted(frame, 1, aux_image, 0.8, 0)
            cv2.imshow("aux_image", aux_image)
            cv2.fillPoly(aux_image, pts=[contorno], color=(128, 0, 250))
            # contador
            cv2.rectangle(frame, (0, 0), (60, 60), (255, 255, 0), -1)
            cv2.putText(frame, str(contador), (10, 50), 1, 3.5, (128, 0, 250), 2)

        # Mostrar el frame con las anotaciones en una ventana.
        cv2.imshow("Frame", frame)
        # Si se presiona la tecla ESC, salir del bucle.
        if cv2.waitKey(1) & 0xFF == 27:
            break

# Liberar la cámara y destruir todas las ventanas abiertas por OpenCV.
cap.release()
cv2.destroyAllWindows()
