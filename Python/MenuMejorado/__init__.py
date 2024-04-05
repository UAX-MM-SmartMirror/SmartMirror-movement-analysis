import cv2
import mediapipe as mp
import math
import time

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
x_inicial = 20
y_inicial = 20
x_final = 220
y_final = 1100
button_data = [
    {"text": "Ajustes", "rect": (50, 150, 150, 50), "clicked": False},
    {"text": "Boton 1", "rect": (50, 220, 150, 50), "clicked": False},
    {"text": "Boton 2", "rect": (50, 290, 150, 50), "clicked": False},
    {"text": "Boton 3", "rect": (50, 360, 150, 50), "clicked": False},
    {"text": "Boton 4", "rect": (50, 430, 150, 50), "clicked": False},
    {"text": "Boton 5", "rect": (50, 500, 150, 50), "clicked": False},
]
show_buttons = False
button_index = 0

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

        # Lógica para mostrar los botones
        for i, button in enumerate(button_data):
            if button["clicked"]:
                cv2.rectangle(frame, (button["rect"][0], button["rect"][1]),
                              (button["rect"][0] + button["rect"][2], button["rect"][1] + button["rect"][3]),
                              (0, 255, 0), -1)
                cv2.putText(frame, button["text"], (button["rect"][0] + 10, button["rect"][1] + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            elif show_buttons and i == button_index:
                cv2.rectangle(frame, (button["rect"][0], button["rect"][1]),
                              (button["rect"][0] + button["rect"][2], button["rect"][1] + button["rect"][3]), (255, 0, 0), 2)
                cv2.putText(frame, button["text"], (button["rect"][0] + 10, button["rect"][1] + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

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
                if button_data[0]["rect"][0] < x_index < button_data[0]["rect"][0] + button_data[0]["rect"][2] and \
                   button_data[0]["rect"][1] < y_index < button_data[0]["rect"][1] + button_data[0]["rect"][3] and distance < 50:
                    cv2.putText(frame, f'Boton "{button_data[0]["text"]}" pulsado!', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 255, 0), 2, cv2.LINE_AA)
                    button_data[0]["clicked"] = True
                    show_buttons = True

                    # Mostrar los botones uno por uno
                    time.sleep(0.5)
                    button_index += 1
                    if button_index >= len(button_data):
                        show_buttons = False

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()