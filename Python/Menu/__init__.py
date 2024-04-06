# Importación de las bibliotecas necesarias para el procesamiento de imágenes y detección de gestos de manos.
import cv2
import mediapipe as mp

# Configuración de MediaPipe para el módulo de detección de manos.
mp_hands = mp.solutions.hands

# Inicialización del objeto de captura de vídeo para la webcam.
cap = cv2.VideoCapture(0)

# Definición de las opciones del menú y las coordenadas del rectángulo del menú.
menu_options = ["Rutinas", "Noticias", "Tiempo", "Musica", "Cerrar"]
menu_rect = (50, 200, 400, 40)  # x, y, ancho, alto del rectángulo del menú
menu_displayed = True  # Controla si el menú se muestra o no al inicio
menu_visible_frame_count = 0  # Contador para la visibilidad del menú basado en los movimientos de la mano
frame_count_threshold = 30  # Umbral de recuento de cuadros para controlar la sensibilidad al movimiento

# Variable para el seguimiento del movimiento de la mano para abrir/cerrar el menú.
prev_x_index = 0

# Configuración y uso del modelo de detección de manos de MediaPipe.
with mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5) as hands:
    # Bucle principal de captura de vídeo.
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Si no hay frame, salir del bucle.
        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1)  # Voltear la imagen horizontalmente para efecto espejo.
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convertir a RGB para procesamiento de MediaPipe.

        # Procesamiento de las manos con MediaPipe.
        results = hands.process(frame_rgb)

        # Detectar el movimiento de la mano para controlar la visibilidad del menú.
        if results.multi_hand_landmarks is not None:
            for hand_landmarks in results.multi_hand_landmarks:
                # Coordenadas 'x' del índice de la mano derecha (índice 12).
                x_index = int(hand_landmarks.landmark[12].x * width)

                # Verificar si hay un movimiento significativo de lado a lado.
                if abs(x_index - prev_x_index) > 5:  # Ajustar sensibilidad de movimiento aquí.
                    menu_visible_frame_count += 1
                    # Alternar la visualización del menú si el movimiento se mantiene.
                    if menu_visible_frame_count >= frame_count_threshold:
                        menu_displayed = not menu_displayed
                        menu_visible_frame_count = 0

                prev_x_index = x_index  # Actualizar la posición 'x' anterior.

        # Mostrar el menú si está activado.
        if menu_displayed:
            # Dibujar el rectángulo del menú.
            cv2.rectangle(frame, (menu_rect[0], menu_rect[1]),
                          (menu_rect[0] + menu_rect[2], menu_rect[1] + menu_rect[3]), (0, 255, 0), -1)
            # Mostrar cada opción del menú.
            for i, option in enumerate(menu_options):
                cv2.putText(frame, option, (menu_rect[0] + 10, menu_rect[1] + 30 + i * 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Mostrar el frame con los botones en la ventana.
        cv2.imshow("Frame", frame)
        # Salir con la tecla ESC.
        if cv2.waitKey(1) & 0xFF == 27:
            break

# Liberar la cámara y cerrar todas las ventanas de OpenCV al finalizar.
cap.release()
cv2.destroyAllWindows()

