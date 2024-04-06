import cv2  # Importar la biblioteca de OpenCV
import mediapipe as mp  # Importar la biblioteca de MediaPipe
import math  # Importar la biblioteca de matemáticas

# Inicialización de los módulos de dibujo y de detección de manos de MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Inicialización del objeto de captura de vídeo para la cámara web
cap = cv2.VideoCapture(0)

# Definición de coordenadas iniciales y finales para la región de interés
x_inicial = 20
y_inicial = 20
x_final = 220
y_final = 1100

# Definición de texto y parámetros del botón 'Ajustes'
button_text = "Ajustes"
button_rect = (100, 50, 120, 40)  # Coordenadas del botón 'Ajustes' (x, y, ancho, alto)
button_clicked = False  # Estado del clic del botón 'Ajustes'

# Definición de variables para la lógica de interacción del botón
show_login_button = False  # Control de visualización del botón 'Iniciar Sesión'
show_welcome_button = False  # Control de visualización del botón de bienvenida
welcome_button_rect = (50, 150, 400, 60)  # Coordenadas del botón de bienvenida (x, y, ancho, alto)
welcome_button_clicked = False  # Estado del clic del botón de bienvenida

# Cálculo de la relación de aspecto de la pantalla basada en las coordenadas proporcionadas
aspect_ratio_screen = (x_final - x_inicial) / (y_final - y_inicial)
print(aspect_ratio_screen)  # Imprimir la relación de aspecto

# Configuración y utilización del modelo de detección de manos de MediaPipe
with mp_hands.Hands(
        static_image_mode=False,  # Modo de imagen estática desactivado para flujo continuo
        max_num_hands=1,  # Número máximo de manos a detectar
        min_detection_confidence=0.5  # Confianza mínima de detección
) as hands:
    while True:
        ret, frame = cap.read()  # Lectura de un cuadro de la cámara web
        if not ret:
            break  # Si no se puede leer el cuadro, salir del bucle

        height, width, _ = frame.shape  # Obtención de las dimensiones del cuadro
        frame = cv2.flip(frame, 1)  # Voltear el cuadro horizontalmente para efecto espejo
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Conversión del cuadro a RGB

        results = hands.process(frame_rgb)  # Procesamiento del cuadro con el modelo de manos

        # Mostrar botones y gestionar su interacción
        if button_clicked:  # Si se ha pulsado el botón 'Ajustes'
            if show_welcome_button:  # Si el botón de bienvenida debe mostrarse
                # Dibujar el botón de bienvenida
                cv2.rectangle(frame, (welcome_button_rect[0], welcome_button_rect[1]),
                              (welcome_button_rect[0] + welcome_button_rect[2],
                               welcome_button_rect[1] + welcome_button_rect[3]),
                              (0, 255, 0), -1)
                # Colocar texto en el botón de bienvenida
                cv2.putText(frame, '¡Bienvenido!', (welcome_button_rect[0] + 10, welcome_button_rect[1] + 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        else:
            # Dibujar el botón 'Ajustes' sin rellenar
            cv2.rectangle(frame, (button_rect[0], button_rect[1]),
                          (button_rect[0] + button_rect[2], button_rect[1] + button_rect[3]), (255, 0, 0), 2)
            # Colocar texto en el botón 'Ajustes'
            cv2.putText(frame, button_text, (button_rect[0] + 10, button_rect[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 255, 255), 2, cv2.LINE_AA)

            # Si se detectan manos, realizar la lógica de interacción con el botón 'Ajustes'
            if results.multi_hand_landmarks is not None:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Obtener las coordenadas de la punta del dedo índice y el pulgar
                    x_index = int(hand_landmarks.landmark[8].x * width)
                    y_index = int(hand_landmarks.landmark[8].y * height)
                    x_thumb = int(hand_landmarks.landmark[4].x * width)
                    y_thumb = int(hand_landmarks.landmark[4].y * height)

                    # Calcular la distancia entre el dedo índice y el pulgar
                    distance = math.sqrt((x_index - x_thumb) ** 2 + (y_index - y_thumb) ** 2)

                    # Si la distancia es pequeña y la punta del dedo índice está sobre el botón 'Ajustes': consideramos que se ha hecho clic
                    if (button_rect[0] < x_index < button_rect[0] + button_rect[2] and
                            button_rect[1] < y_index < button_rect[1] + button_rect[3] and
                            distance < 50):
                        # Indicar que el botón 'Ajustes' ha sido pulsado
                        cv2.putText(frame, 'Boton "Ajustes" pulsado!', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0, 255, 0), 2, cv2.LINE_AA)
                        button_clicked = True
                        show_login_button = True

        # Verificar la acción del botón de "Iniciar Sesión"
        if show_login_button:  # Si se debe mostrar el botón 'Iniciar Sesión'
            if welcome_button_clicked:  # Si se ha pulsado el botón de bienvenida
                show_login_button = False
                show_welcome_button = False
                welcome_button_clicked = False

            # Lógica para mostrar el botón 'Iniciar Sesión'
            cv2.rectangle(frame, (50, 150), (250, 200), (0, 0, 255), -1)  # Dibujar el botón 'Iniciar Sesión'
            cv2.putText(frame, 'Iniciar Sesion', (80, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2,
                        cv2.LINE_AA)

            # Si se detectan manos, realizar la lógica de interacción con el botón 'Iniciar Sesión'
            if results.multi_hand_landmarks is not None:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Obtener las coordenadas de la punta del dedo índice y el pulgar
                    x_index = int(hand_landmarks.landmark[8].x * width)
                    y_index = int(hand_landmarks.landmark[8].y * height)

                    # Calcular la distancia entre el dedo índice y el pulgar
                    distance = math.sqrt((x_index - x_thumb) ** 2 + (y_index - y_thumb) ** 2)

                    # Si la distancia es pequeña y la punta del dedo índice está sobre el botón 'Iniciar Sesión': consideramos que se ha hecho clic
                    if (250 > x_index > 50 > distance and
                            150 < y_index < 200):
                        # Indicar que el botón 'Iniciar Sesión' ha sido pulsado
                        cv2.putText(frame, 'Botón "Iniciar Sesion" pulsado!', (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0, 255, 0), 2, cv2.LINE_AA)
                        show_welcome_button = True
                        welcome_button_clicked = True

        cv2.imshow("Frame", frame)  # Mostrar el cuadro en una ventana
        if cv2.waitKey(1) & 0xFF == 27:  # Salir con la tecla ESC
            break

cap.release()  # Liberar la cámara
cv2.destroyAllWindows()  # Cerrar todas las ventanas de OpenCV
