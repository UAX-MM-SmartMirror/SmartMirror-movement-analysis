import cv2
import mediapipe as mp

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7)


def is_letter_s(hand_landmarks):
    # Puntos de referencia para la punta de los dedos y las articulaciones inferiores
    tip_ids = [4, 8, 12, 16, 20]  # Pulgar, Índice, Medio, Anular, Meñique
    lower_joint_ids = [2, 5, 9, 13, 17]  # Articulaciones inferiores de cada dedo

    # Verificar que los dedos (excepto el pulgar) estén cerrados
    fingers_folded = all(
        hand_landmarks.landmark[tip_ids[i]].y > hand_landmarks.landmark[lower_joint_ids[i]].y for i in range(1, 5))

    # Verificar que el pulgar esté sobre los dedos o al menos cerca de ellos
    thumb_over_fingers = hand_landmarks.landmark[tip_ids[0]].x > hand_landmarks.landmark[tip_ids[1]].x

    return fingers_folded and thumb_over_fingers


def is_letter_g(hand_landmarks):
    # Puntos de referencia para la punta de los dedos y las articulaciones inferiores
    tip_ids = [4, 8, 12, 16, 20]  # Pulgar, Índice, Medio, Anular, Meñique
    lower_joint_ids = [2, 5, 9, 13, 17]  # Articulaciones inferiores de cada dedo

    # Verificar que el índice y el pulgar estén extendidos
    index_and_thumb_extended = (
                hand_landmarks.landmark[tip_ids[1]].y < hand_landmarks.landmark[lower_joint_ids[1]].y and
                hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[lower_joint_ids[0]].x)

    # Verificar que los otros dedos no estén extendidos
    others_folded = all(
        hand_landmarks.landmark[tip_ids[i]].y > hand_landmarks.landmark[lower_joint_ids[i]].y for i in range(2, 5))

    return index_and_thumb_extended and others_folded


def is_letter_u(hand_landmarks):
    # Puntos de referencia para la punta de los dedos y las articulaciones inferiores
    tip_ids = [4, 8, 12, 16, 20]  # Pulgar, Índice, Medio, Anular, Meñique
    mcp_joint_ids = [1, 5, 9, 13, 17]  # Articulaciones Metacarpofalángicas (MCP)

    # Verificar que el índice y el medio estén extendidos y separados
    index_and_middle_extended = (hand_landmarks.landmark[tip_ids[1]].y < hand_landmarks.landmark[mcp_joint_ids[1]].y and
                                 hand_landmarks.landmark[tip_ids[2]].y < hand_landmarks.landmark[mcp_joint_ids[2]].y)

    # Verificar que el pulgar esté extendido hacia adelante
    thumb_extended_forward = hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[mcp_joint_ids[0]].x

    # Verificar que los otros dedos (anular y meñique) estén cerrados
    others_folded = all(
        hand_landmarks.landmark[tip_ids[i]].y > hand_landmarks.landmark[mcp_joint_ids[i]].y for i in range(3, 5))

    return index_and_middle_extended and thumb_extended_forward and others_folded


def is_letter_n(hand_landmarks):
    # En la letra N, el índice y el medio están extendidos
    return (hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y and
            hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y and
            all(hand_landmarks.landmark[i].y > hand_landmarks.landmark[0].y for i in [16, 20]))


def is_letter_p(hand_landmarks):
    # Puntos de referencia para la punta de los dedos y las articulaciones inferiores
    tip_ids = [4, 8, 12, 16, 20]  # Pulgar, Índice, Medio, Anular, Meñique
    pip_joint_ids = [3, 6, 10, 14, 18]  # Articulaciones Proximales Interfalángicas (PIP)

    # Verificar que el índice, medio y anular estén extendidos
    three_fingers_extended = (hand_landmarks.landmark[tip_ids[1]].y < hand_landmarks.landmark[pip_joint_ids[1]].y and
                              hand_landmarks.landmark[tip_ids[2]].y < hand_landmarks.landmark[pip_joint_ids[2]].y and
                              hand_landmarks.landmark[tip_ids[3]].y < hand_landmarks.landmark[pip_joint_ids[3]].y)

    # Verificar que el pulgar y el meñique estén cerrados
    thumb_and_pinky_folded = (hand_landmarks.landmark[tip_ids[0]].y > hand_landmarks.landmark[pip_joint_ids[0]].y and
                              hand_landmarks.landmark[tip_ids[4]].y > hand_landmarks.landmark[pip_joint_ids[4]].y)

    return three_fingers_extended and thumb_and_pinky_folded


def is_letter_c(hand_landmarks):
    # Puntos de referencia para la punta de los dedos y la base de la palma
    tip_ids = [4, 8, 12, 16, 20]  # Pulgar, Índice, Medio, Anular, Meñique
    base_id = 0  # Base de la palma

    # Verificar que los dedos no estén completamente extendidos ni completamente cerrados
    fingers_partially_folded = all(
        hand_landmarks.landmark[base_id].y < hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[
            base_id].y + 0.1 for i in range(1, 5))

    # Verificar que el pulgar esté en una posición similar a los otros dedos (formando una C)
    thumb_in_position = hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[1]].x

    return fingers_partially_folded and thumb_in_position


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
                cv2.putText(image, "Letra: S", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                # Mostrar que es la letra S
            elif is_letter_g(hand_landmarks):
                cv2.putText(image, "Letra: G", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                # Mostrar que es la letra G
            elif is_letter_n(hand_landmarks):
                cv2.putText(image, "Letra: N", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                # Mostrar que es la letra N
            elif is_letter_p(hand_landmarks):
                cv2.putText(image, "Letra: P", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                # Mostrar que es la letra N

            elif is_letter_u(hand_landmarks):
                cv2.putText(image, "Letra: U", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                # Mostrar que es la letra N

            elif is_letter_c(hand_landmarks):
                cv2.putText(image, "Letra: C", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                # Mostrar que es la letra N
            elif is_letter_o(hand_landmarks):
                cv2.putText(image, "Letra: O", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                # Mostrar que es la letra O
            else:
                cv2.putText(image, ".", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                # Mostrar que no es ninguna de estas letras
    cv2.imshow('Mano Detectada', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()