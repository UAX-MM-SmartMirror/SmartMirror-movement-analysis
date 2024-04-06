# Importación de las bibliotecas OpenCV y MediaPipe para el procesamiento de imágenes y detección de manos.
import cv2
import mediapipe as mp

# Inicialización del módulo de dibujo de MediaPipe y el módulo de manos para la detección de las mismas.
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Inicialización del objeto de captura de vídeo para la webcam (primer dispositivo de captura).
cap = cv2.VideoCapture(0)

# Definición de coordenadas iniciales y finales para calcular la proporción de aspecto.
x_inicial = 20
y_inicial = 20
x_final = 220
y_final = 1100

# Cálculo de la proporción de aspecto de la pantalla basada en las coordenadas proporcionadas.
aspect_ratio_screen = (x_final - x_inicial) / (y_final - y_inicial)
print(aspect_ratio_screen)

# Inicio del procesamiento de las manos con MediaPipe.
with mp_hands.Hands(
        static_image_mode=False,  # Modo dinámico, adecuado para video.
        max_num_hands=1,  # Número máximo de manos a detectar.
        min_detection_confidence=0.5  # Umbral mínimo de confianza para la detección.
) as hands:
    # Bucle de captura y procesamiento de vídeo.
    while True:
        ret, frame = cap.read()  # Lectura de un cuadro del vídeo.
        if ret == False:
            break  # Si no hay cuadro, sale del bucle.

        # Obtención de las dimensiones del cuadro y espejo horizontal para obtener una vista tipo espejo.
        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1)

        # Conversión del cuadro a RGB, que es el formato requerido por MediaPipe.
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Procesamiento del cuadro para detectar las manos.
        results = hands.process(frame_rgb)

        # Si se detectan marcas de mano, procesa cada una.
        if results.multi_hand_landmarks is not None:
            for hand_landmarks in results.multi_hand_landmarks:
                # Calcula las coordenadas del punto de referencia #9 (punta del dedo medio).
                x = int(hand_landmarks.landmark[9].x * width)
                y = int(hand_landmarks.landmark[9].y * height)

                # Dibuja un círculo en la punta del dedo medio.
                cv2.circle(frame, (x, y), 16, (0, 255, 0), 5, 2)

        # Muestra el cuadro procesado en una ventana.
        cv2.imshow("Frame", frame)

        # Si se presiona la tecla ESC, sale del bucle.
        if cv2.waitKey(1) & 0xFF == 27:
            break

# Liberación de la cámara y destrucción de todas las ventanas de OpenCV.
cap.release()
cv2.destroyAllWindows()
