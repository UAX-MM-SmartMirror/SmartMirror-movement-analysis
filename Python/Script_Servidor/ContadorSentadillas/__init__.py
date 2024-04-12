import threading
import cv2
import mediapipe as mp
import numpy as np
from math import acos, degrees
import requests


class ContadorSentadillas:
    def __init__(self, indicador_proceso):
        self.detener = threading.Event()
        self.indicador_proceso = indicador_proceso
        self.thread = threading.Thread(target=self.start_sentadillas)
        self.thread.daemon = True  # Asegura que el hilo se cierre si la aplicación principal termina
        self.running = False

    def start_sentadillas(self):
        self.running = True
        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: No se pudo acceder a la cámara web.")
            return

        up = False
        down = False
        contador = 0
        url = 'http://localhost:5000/upload'

        with mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5) as pose:
            while not self.detener.is_set() and self.running:
                ret, frame = cap.read()
                if not ret:
                    print("Error: No se pudo leer el frame de la cámara.")
                    break

                frame = cv2.flip(frame, 1)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame_rgb)

                if results.pose_landmarks:
                    x1, y1 = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].x * cap.get(3)), int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y * cap.get(4))
                    x2, y2 = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].x * cap.get(3)), int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].y * cap.get(4))
                    x3, y3 = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].x * cap.get(3)), int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].y * cap.get(4))
                    p1, p2, p3 = np.array([x1, y1]), np.array([x2, y2]), np.array([x3, y3])
                    angle = degrees(acos((np.linalg.norm(p2 - p3) ** 2 + np.linalg.norm(p1 - p3) ** 2 - np.linalg.norm(p1 - p2) ** 2) / (2 * np.linalg.norm(p2 - p3) * np.linalg.norm(p1 - p3))))

                    if angle > 160:
                        up = True
                    if up and angle < 90:
                        down = True
                    if up and down and angle > 160:
                        contador += 1
                        up = False
                        down = False
                        print(f"Ángulo: {angle}, Contador: {contador}")
                        self.send_data(url, contador, angle)

                cv2.imshow("Sentadillas", frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break

        cap.release()
        cv2.destroyAllWindows()

    def send_data(self, url, contador, angle):
        data = {'type': 'squat_counter', 'contador': contador, 'angle': angle}
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
