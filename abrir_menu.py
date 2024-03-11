import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

menu_options = ["Rutinas", "Noticias", "Tiempo", "Musica", "Cerrar"]
menu_rect = (50, 200, 400, 40)  # Coordenadas del menú (x_inicial, y_inicial, ancho, alto)
menu_displayed = True  # Iniciar con el menú desplegado
menu_visible_frame_count = 0
frame_count_threshold = 30  # Ajusta este valor para controlar la sensibilidad al movimiento

# Variables para el control de la apertura y cierre del menú
prev_x_index = 0

with mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5) as hands:
    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(frame_rgb)

        # Verificar el movimiento de la mano derecha de lado a lado para abrir/cerrar el menú
        if results.multi_hand_landmarks is not None:
            for hand_landmarks in results.multi_hand_landmarks:
                # Ajuste para usar la mano derecha (índice 12)
                x_index = int(hand_landmarks.landmark[12].x * width)

                # Verificar si la mano derecha se mueve de lado a lado
                if abs(x_index - prev_x_index) > 5:  # Ajusta este valor para controlar la sensibilidad al movimiento
                    menu_visible_frame_count += 1
                    if menu_visible_frame_count >= frame_count_threshold:
                        menu_displayed = not menu_displayed
                        menu_visible_frame_count = 0

                prev_x_index = x_index

        # Mostrar el menú si está activo
        if menu_displayed:
            cv2.rectangle(frame, (menu_rect[0], menu_rect[1]),
                          (menu_rect[0] + menu_rect[2], menu_rect[1] + menu_rect[3]), (0, 255, 0), -1)
            for i, option in enumerate(menu_options):
                cv2.putText(frame, option, (menu_rect[0] + 10, menu_rect[1] + 30 + i * 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
