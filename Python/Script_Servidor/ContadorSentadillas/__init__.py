import cv2
import numpy as np
import mediapipe as mp
from math import acos, degrees
import requests
import threading

class ContadorSentadillas:
    def __init__(self, indicador_proceso):
        self.indicador_proceso = indicador_proceso
        self.detener = threading.Event()
        self.thread = threading.Thread(target=self.iniciar)
        self.contador = 0

    def run(self):
        if not self.thread.is_alive():
            self.thread.start()

    def stop(self):
        self.detener.set()
        if self.thread.is_alive():
            self.thread.join()

    def iniciar(self):
        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose
        cap = cv2.VideoCapture(0)

        url = 'http://localhost:5000/upload'
        up = False
        down = False

        with mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5) as pose:
            while not self.detener.is_set():
                ret, frame = cap.read()
                if not ret:
                    break

                height, width, _ = frame.shape
                frame = cv2.flip(frame, 1)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame_rgb)

                if results.pose_landmarks is not None:
                    x1, y1 = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].x * width), int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y * height)
                    x2, y2 = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].x * width), int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].y * height)
                    x3, y3 = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].x * width), int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].y * height)

                    p1, p2, p3 = np.array([x1, y1]), np.array([x2, y2]), np.array([x3, y3])
                    angle = self.calcular_angulo(p1, p2, p3)

                    if angle >= 160:
                        up = True
                    if up and not down and angle <= 70:
                        down = True
                    if up and down and angle >= 160:
                        self.contador += 1
                        up = False
                        down = False
                        self.send_data(url, self.contador, angle)

                    # Visualización
                    self.visualizar(frame, p1, p2, p3, angle)

                if cv2.waitKey(1) & 0xFF == 27:
                    break

        cap.release()
        cv2.destroyAllWindows()

    def calcular_angulo(self, p1, p2, p3):
        l1 = np.linalg.norm(p2-p3)
        l2 = np.linalg.norm(p1-p3)
        l3 = np.linalg.norm(p1-p2)
        angle = degrees(acos((l1**2 + l3**2 - l2**2) / (2 * l1 * l3)))
        return angle

    def send_data(self, url, contador, angle):
        data = {'type': 'squat_counter', 'contador': contador, 'angle': angle}
        try:
            response = requests.post(url, json=data)
            print("Data sent to server:", data)
            print("Server response:", response.text)
        except requests.exceptions.RequestException as e:
            print("Failed to send data:", e)

    def visualizar(self, frame, p1, p2, p3, angle):
        cv2.circle(frame, tuple(p1), 6, (0, 255, 255), 4)
        cv2.circle(frame, tuple(p2), 6, (0, 255, 255), 4)
        cv2.circle(frame, tuple(p3), 6, (0, 255, 255), 4)
        cv2.putText(frame, str(int(angle)), (p2[0] + 30, p2[1]), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (128, 0, 250), 2)
        cv2.line(frame, tuple(p1), tuple(p2), (255, 255, 0), 20)
        cv2.line(frame, tuple(p2), tuple(p3), (255, 255, 0), 20)
        cv2.line(frame, tuple(p1), tuple(p3), (255, 255, 0), 5)
        cv2.putText(frame, str(self.contador), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 3.5, (128, 0, 250), 2)
        cv2.imshow("Squat Counter", frame)
