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




elif is_letter_i(hand_landmarks):
                print("Letra: I")