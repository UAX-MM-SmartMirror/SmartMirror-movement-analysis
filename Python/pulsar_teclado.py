import cv2
import mediapipe as mp
import math



mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands



cap = cv2.VideoCapture(0)
x_inicial = 20
y_inicial = 20
x_final = 220
y_final = 1100
button_text = "Ajustes"
button_rect = (100, 50, 120, 40)  # Nuevas coordenadas del botón (x_inicial, y_inicial, ancho, alto)
button_clicked = False
show_login_button = False
show_welcome_button = False
welcome_button_rect = (50, 150, 400, 60)  # Coordenadas del botón de bienvenida
welcome_button_clicked = False

aspect_ratio_screen = (x_final - x_inicial) / (y_final - y_inicial)
print(aspect_ratio_screen)

with mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5) as hands:
    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(frame_rgb)

        # Mostrar los botones si el botón "Ajustes" está pulsado
        if button_clicked:
            # Lógica para mostrar el botón de "Bienvenido" después de iniciar sesión
            if show_welcome_button:
                cv2.rectangle(frame, (welcome_button_rect[0], welcome_button_rect[1]),
                              (welcome_button_rect[0] + welcome_button_rect[2], welcome_button_rect[1] + welcome_button_rect[3]),
                              (0, 255, 0), -1)
                cv2.putText(frame, '¡Bienvenido!', (welcome_button_rect[0] + 10, welcome_button_rect[1] + 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        else:
            # Dibujar el contorno del botón "Ajustes" en lugar de rellenarlo
            cv2.rectangle(frame, (button_rect[0], button_rect[1]),
                          (button_rect[0] + button_rect[2], button_rect[1] + button_rect[3]), (255, 0, 0), 2)
            cv2.putText(frame, button_text, (button_rect[0] + 10, button_rect[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 255, 255), 2, cv2.LINE_AA)

            # Verificar la distancia entre el dedo índice y el pulgar para simular un clic
            if results.multi_hand_landmarks is not None:
                for hand_landmarks in results.multi_hand_landmarks:
                    x_index = int(hand_landmarks.landmark[8].x * width)
                    y_index = int(hand_landmarks.landmark[8].y * height)
                    x_thumb = int(hand_landmarks.landmark[4].x * width)
                    y_thumb = int(hand_landmarks.landmark[4].y * height)

                    # Calcular la distancia entre el dedo índice y el pulgar
                    distance = math.sqrt((x_index - x_thumb) ** 2 + (y_index - y_thumb) ** 2)

                    # Verificar la distancia y simular un clic si está por debajo de un umbral
                    if button_rect[0] < x_index < button_rect[0] + button_rect[2] and button_rect[1] < y_index < button_rect[1] + button_rect[3] and distance < 50:
                        cv2.putText(frame, 'Botón "Ajustes" pulsado!', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0, 255, 0), 2, cv2.LINE_AA)
                        button_clicked = True
                        show_login_button = True

        # Verificar la acción del botón de "Iniciar Sesión"
        if show_login_button:
            if welcome_button_clicked:
                show_login_button = False
                show_welcome_button = False
                welcome_button_clicked = False

            # Lógica para mostrar el botón de "Iniciar Sesión"
            cv2.rectangle(frame, (50, 150), (250, 200), (0, 0, 255), -1)
            cv2.putText(frame, 'Iniciar Sesión', (80, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

            # Verificar la distancia entre el dedo índice y el pulgar para simular un clic en el botón de "Iniciar Sesión"
            if results.multi_hand_landmarks is not None:
                for hand_landmarks in results.multi_hand_landmarks:
                    x_index = int(hand_landmarks.landmark[8].x * width)
                    y_index = int(hand_landmarks.landmark[8].y * height)
                    x_thumb = int(hand_landmarks.landmark[4].x * width)
                    y_thumb = int(hand_landmarks.landmark[4].y * height)

                    # Calcular la distancia entre el dedo índice y el pulgar
                    distance = math.sqrt((x_index - x_thumb) ** 2 + (y_index - y_thumb) ** 2)

                    # Verificar la distancia y simular un clic si está por debajo de un umbral
                    if 50 < x_index < 250 and 150 < y_index < 200 and distance < 50:
                        cv2.putText(frame, 'Botón "Iniciar Sesión" pulsado!', (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0, 255, 0), 2, cv2.LINE_AA)
                        show_welcome_button = True
                        welcome_button_clicked = True

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
