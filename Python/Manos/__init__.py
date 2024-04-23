# Importamos la librería de OpenCV para manejar la captura y procesamiento de imágenes
import cv2
# Importamos la librería de MediaPipe para el procesamiento de gestos de manos
import mediapipe as mp

# Inicializamos el módulo de dibujo de MediaPipe y el módulo de detección de manos
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Configuramos la captura de video usando la primera cámara web del sistema
cap = cv2.VideoCapture(0)

# Creamos un objeto de manos utilizando el módulo de manos de MediaPipe
# Configuramos para detectar múltiples manos y especificamos la confianza mínima para la detección
with mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5) as hands:
    # Entramos en un bucle infinito para procesar cada frame capturado por la cámara web
    while True:
        ret, frame = cap.read()  # Leemos un frame del objeto de captura
        # Si la captura falló, salimos del bucle
        if not ret:
            break

        # Obtenemos las dimensiones del frame para su uso posterior
        height, width, _ = frame.shape
        # Volteamos el frame horizontalmente para que actúe como un espejo
        frame = cv2.flip(frame, 1)
        # Convertimos el frame de color BGR (que usa OpenCV) a RGB (que usa MediaPipe)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Procesamos el frame para detectar las manos
        results = hands.process(frame_rgb)

        # Si encontramos marcas de manos, las dibujamos en el frame
        if results.multi_hand_landmarks is not None:
            for hand_landmarks in results.multi_hand_landmarks:
                # Utilizamos la función de dibujo de MediaPipe para dibujar las conexiones entre los puntos de la mano
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Mostramos el frame resultante en una ventana llamada "Frame"
        cv2.imshow("Frame", frame)
        # Esperamos por la tecla ESC para salir del bucle
        if cv2.waitKey(1) & 0xFF == 27:
            break

# Liberamos el objeto de captura y destruimos todas las ventanas creadas
cap.release()
cv2.destroyAllWindows()

