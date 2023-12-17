import cv2
import mediapipe as mp

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7)

# Función para contar dedos levantados
def is_letter_i(hand_landmarks):
    # Puntos de referencia para la punta de los dedos y las articulaciones
    tip_ids = [4, 8, 12, 16, 20]
    middle_joint_ids = [3, 7, 11, 15, 19]

    finger_up = [False, False, False, False, False]

    # Pulgar
    # Se compara en el eje x ya que el pulgar es horizontal
    if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[middle_joint_ids[0]].x:
        finger_up[0] = True

    # Otros dedos
    for i in range(1, 5):
        if hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[middle_joint_ids[i]].y:
            finger_up[i] = True

    # Contar dedos levantados
    if finger_up.count(True) == 1:
        cv2.putText(image, "Letra: I", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    
def is_letter_s(hand_landmarks):
    # En la letra S, el puño está cerrado
    return all(hand_landmarks.landmark[i].y > hand_landmarks.landmark[0].y for i in range(1, 5))

def is_letter_g(hand_landmarks):
    # En la letra G, el índice y el pulgar están extendidos
    return (hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y and
            hand_landmarks.landmark[4].y < hand_landmarks.landmark[3].y and
            all(hand_landmarks.landmark[i].y > hand_landmarks.landmark[0].y for i in [12, 16, 20]))

def is_letter_n(hand_landmarks):
    # En la letra N, el índice y el medio están extendidos
    return (hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y and
            hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y and
            all(hand_landmarks.landmark[i].y > hand_landmarks.landmark[0].y for i in [16, 20]))

def is_letter_o(hand_landmarks):
    # En la letra O, el índice y el pulgar forman un círculo
    return (abs(hand_landmarks.landmark[8].x - hand_landmarks.landmark[4].x) < 0.05 and
            abs(hand_landmarks.landmark[8].y - hand_landmarks.landmark[4].y) < 0.05)


# Capturar video de la cámara
cap = cv2.VideoCapture(0)
while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    # Procesar la imagen
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Dibujar las manos y comprobar gestos
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            if is_letter_s(hand_landmarks):
                cv2.putText(image, "Letra: N", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                 # Mostrar que es la letra S
            elif is_letter_i(hand_landmarks):
                print("Letra: I")
                # Mostrar que es la letra I
            elif is_letter_g(hand_landmarks):
                cv2.putText(image, "Letra: G", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                # Mostrar que es la letra G
            elif is_letter_n(hand_landmarks):
                cv2.putText(image, "Letra: N", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                # Mostrar que es la letra N
            elif is_letter_o(hand_landmarks):
                cv2.putText(image, "Letra: O", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                # Mostrar que es la letra O
            else:
                cv2.putText(image, "No es ninguna letra", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            
                # Mostrar que no es ninguna de estas letras
    cv2.imshow('Mano Detectada', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
