import threading
import cv2
import mediapipe as mp
import numpy as np
import requests
from math import acos, degrees
class ContadorFlexiones:
    def __init__(self, indicador_proceso):
        self.detener = threading.Event()
        self.indicador_proceso = indicador_proceso
        self.thread = threading.Thread(target=self.start_flexiones)
        self.thread.daemon = True



    def start_flexiones(self):
        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose
        cap = cv2.VideoCapture(0)

        up = False
        down = False
        contador = 0
        url = 'http://localhost:5000/upload'

        with mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5) as pose:
            while not self.detener.is_set():
                ret, frame = cap.read()
                if not ret:
                    continue

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame_rgb)

                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                    landmarks = results.pose_landmarks.landmark

                    # Ángulos del codo derecho
                    shoulder_right = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y])
                    elbow_right = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y])
                    wrist_right = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y])

                    # Ángulos del codo izquierdo
                    shoulder_left = np.array([landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y])
                    elbow_left = np.array([landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y])
                    wrist_left = np.array([landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y])

                    # Calculamos los ángulos para ambos codos
                    angle_left = degrees(acos(np.dot(np.array(shoulder_left) - np.array(elbow_left),
                                                     np.array(wrist_left) - np.array(elbow_left)) /
                                              (np.linalg.norm(
                                                  np.array(shoulder_left) - np.array(elbow_left)) * np.linalg.norm(
                                                  np.array(wrist_left) - np.array(elbow_left)))))

                    angle_right = degrees(acos(np.dot(np.array(shoulder_right) - np.array(elbow_right),
                                                      np.array(wrist_right) - np.array(elbow_right)) /
                                               (np.linalg.norm(
                                                   np.array(shoulder_right) - np.array(elbow_right)) * np.linalg.norm(
                                                   np.array(wrist_right) - np.array(elbow_right)))))

                    # Contar flexiones
                    if angle_left >= 160 and angle_right >= 160:
                        up = True
                    if up and (angle_left <= 70 or angle_right <= 70):
                        down = True
                    if up and down and angle_left >= 160 and angle_right >= 160:
                        contador += 1
                        up = False
                        down = False
                        self.send_data(url, contador, angle_left, angle_right)

                    cv2.putText(frame, f"Reps: {contador}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                cv2.imshow("Flexion Counter", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()

    def send_data(self, url, contador, angle_left, angle_right):
        data = {'type': 'flexiones', 'contador': contador, 'angulo_izquierdo': angle_left, 'angulo_derecho': angle_right}
        try:
            response = requests.post(url, json=data)
            print("Data sent to server:", data)
            print("Server response:", response.text)
        except requests.exceptions.RequestException as e:
            print("Failed to send data:", e)

    def run(self):
        if not self.thread.is_alive():
            self.thread.start()

    def stop(self):
        self.detener.set()
        if self.thread.is_alive():
            self.thread.join()
