import threading
import cv2
import mediapipe as mp
import numpy as np
import requests

class ContadorBiceps:
    def __init__(self, indicador_proceso):
        self.detener = threading.Event()
        self.indicador_proceso = indicador_proceso
        self.thread = threading.Thread(target=self.start_biceps)
        self.thread.daemon = True  # Asegura que el hilo se cierre si la aplicación principal termina

    def start_biceps(self):
        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose
        cap = cv2.VideoCapture(0)

        up = False
        down = False
        contador = 0
        url = 'http://127.0.0.1:5000/upload'

        with mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5) as pose:
            while not self.detener.is_set():
                ret, frame = cap.read()
                if not ret:
                    break

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame_rgb)

                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                    landmarks = results.pose_landmarks.landmark
                    shoulder = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y])
                    elbow = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y])
                    wrist = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y])
                    angle = self.calculate_angle(shoulder, elbow, wrist)

                    if angle > 160:
                        up = True
                    if up and angle < 70:
                        down = True
                    if up and down and angle > 160:
                        contador += 1
                        up = False
                        down = False
                        self.send_data(url, contador, angle)

                    cv2.putText(frame, f"Reps: {contador}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                cv2.imshow("Biceps Counter", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()

    @staticmethod
    def calculate_angle(a, b, c):
        ba = a - b
        bc = c - b
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)
        return np.degrees(angle)

    def send_data(self, url, contador, angle):
        data = {'type': 'biceps', 'contador': contador, 'angulo_codo': angle}
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
