import cv2
import mediapipe as mp


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)
x_inicial= 20
y_inicial = 20
x_final = 220
y_final = 1100


aspect_ratio_screen = ( x_final - x_inicial )/(y_final - y_inicial)
print(aspect_ratio_screen)

with mp_hands.Hands(static_image_mode = False, max_num_hands = 1, min_detection_confidence = 0.5) as hands:
    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        height, width, _ = frame.shape
        frame = cv2.flip(frame,1)
        frame_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks is not None:
            for hand_landmarks in results.multi_hand_landmarks:
               x = int(hand_landmarks.landmark[9].x * width)
               y = int(hand_landmarks.landmark[9].y * height)

               cv2.circle(frame,(x,y),16,5,2)

        cv2.imshow("Frame",frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()