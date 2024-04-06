# Importar las librerías necesarias para el procesamiento de vídeo e imágenes.
import cv2
import mediapipe as mp

# Configurar los módulos de dibujo y manos de MediaPipe.
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Inicializar la captura de vídeo con la primera cámara web disponible.
cap = cv2.VideoCapture(0)

# Crear un objeto 'Hands' con parámetros específicos para procesar las manos detectadas.
with mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5) as hands:
    # Iniciar un bucle para leer los frames de la cámara.
    while True:
        # Leer un frame de la cámara.
        ret, frame = cap.read()
        # Si la lectura falla, salir del bucle.
        if not ret:
            break

        # Obtener las dimensiones del frame y voltear el frame horizontalmente.
        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1)

        # Convertir el frame de BGR a RGB para el procesamiento con MediaPipe.
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Procesar el frame RGB para detectar las manos.
        results = hands.process(frame_rgb)

        # Si se detectan puntos de referencia de las manos, dibujarlos en el frame.
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Obtener las coordenadas de los puntos de referencia de la punta de los dedos.
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
                pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

                # Identificar gestos específicos para letras del abecedario basándose en la posición de los dedos.
                # Ejemplo: 'A' cuando el dedo índice es el más elevado.
                if index_tip.y < middle_tip.y < ring_tip.y < pinky_tip.y:
                    cv2.putText(frame, 'A', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                # Ejemplo: 'B' cuando los dedos están en orden de izquierda a derecha.
                elif thumb_tip.x < index_tip.x < middle_tip.x < ring_tip.x < pinky_tip.x:
                    cv2.putText(frame, 'B', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                # Aquí se pueden agregar más condiciones para detectar otras letras.

        # Mostrar el frame procesado en una ventana.
        cv2.imshow("Frame", frame)

        # Esperar la tecla ESC para salir del bucle.
        if cv2.waitKey(1) & 0xFF == 27:
            break

# Liberar la cámara y cerrar todas las ventanas cuando se termina.
cap.release()
cv2.destroyAllWindows()

