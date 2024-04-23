# Importaciones necesarias para el procesamiento de imágenes y detección de gestos.
import cv2
import mediapipe as mp
import math
import time

# Configuración de MediaPipe para el dibujo y la detección de manos.
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Inicialización de la cámara.
cap = cv2.VideoCapture(0)

# Definición de variables para la interfaz de usuario.
x_inicial = 20
y_inicial = 20
x_final = 220
y_final = 1100
button_data = [
    {"text": "Ajustes", "rect": (50, 150, 150, 50), "clicked": False},
    # Más botones definidos con su texto, posición y si se ha hecho clic en ellos.
]
show_buttons = False  # Control para mostrar o no los botones.
button_index = 0  # Índice para recorrer los botones.

# Calcula la proporción de aspecto de la pantalla.
aspect_ratio_screen = (x_final - x_inicial) / (y_final - y_inicial)
print(aspect_ratio_screen)

# Configuración de MediaPipe Hands para el procesamiento de las manos.
with mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5) as hands:
    # Bucle principal de captura de vídeo.
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Si no hay frame, salir del bucle.
        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1)  # Voltear la imagen para que actúe como un espejo.
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convertir BGR a RGB.

        # Procesamiento de las manos con MediaPipe.
        results = hands.process(frame_rgb)

        # Lógica para mostrar y gestionar los botones.
        for i, button in enumerate(button_data):
            if button["clicked"]:
                # Si se ha hecho clic en un botón, mostrarlo como presionado.
                cv2.rectangle(frame, (button["rect"][0], button["rect"][1]),
                              (button["rect"][0] + button["rect"][2], button["rect"][1] + button["rect"][3]),
                              (0, 255, 0), -1)
                cv2.putText(frame, button["text"], (button["rect"][0] + 10, button["rect"][1] + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            elif show_buttons and i == button_index:
                # Mostrar el botón actual en el índice.
                cv2.rectangle(frame, (button["rect"][0], button["rect"][1]),
                              (button["rect"][0] + button["rect"][2], button["rect"][1] + button["rect"][3]), (255, 0, 0), 2)
                cv2.putText(frame, button["text"], (button["rect"][0] + 10, button["rect"][1] + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

        # Verificar si se detectan manos y realizar acciones si es así.
        if results.multi_hand_landmarks is not None:
            for hand_landmarks in results.multi_hand_landmarks:
                # Coordenadas del dedo índice.
                x_index = int(hand_landmarks.landmark[8].x * width)
                y_index = int(hand_landmarks.landmark[8].y * height)
                # Coordenadas del pulgar.
                x_thumb = int(hand_landmarks.landmark[4].x * width)
                y_thumb = int(hand_landmarks.landmark[4].y * height)

                # Calcula la distancia entre el dedo índice y el pulgar.
                distance = math.sqrt((x_index - x_thumb) ** 2 + (y_index - y_thumb) ** 2)

                # Comprobar si se ha "clicado" un botón.
                if button_data[0]["rect"][0] < x_index < button_data[0]["rect"][0] + button_data[0]["rect"][2] and \
                   button_data[0]["rect"][1] < y_index < button_data[0]["rect"][1] + button_data[0]["rect"][3] and distance < 50:
                    # Acción a realizar cuando se pulsa un botón.
                    cv2.putText(frame, f'Boton "{button_data[0]["text"]}" pulsado!', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 255, 0), 2, cv2.LINE_AA)
                    button_data[0]["clicked"] = True
                    show_buttons = True

                    # Pausar momentáneamente para evitar clics múltiples.
                    time.sleep(0.5)
                    button_index += 1  # Mover al siguiente botón.
                    if button_index >= len(button_data):
                        # Si hemos llegado al final, ocultar los botones.
                        show_buttons = False

        # Mostrar el frame con los botones.
        cv2.imshow("Frame", frame)
        # Salir con la tecla ESC.
        if cv2.waitKey(1) & 0xFF == 27:
            break

# Liberar la cámara y cerrar todas las ventanas de OpenCV al finalizar.
cap.release()
cv2.destroyAllWindows()