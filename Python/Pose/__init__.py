import cv2  # Importar OpenCV para el procesamiento de imágenes
import mediapipe as mp  # Importar MediaPipe para detección de poses
import numpy as np  # Importar numpy para operaciones matemáticas

# Inicialización de los módulos de dibujo de MediaPipe y configuración de poses
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose  # Módulo de pose de MediaPipe

# Lista de archivos de imagen estáticos para procesar
IMAGE_FILES = []
# Color de fondo para la imagen anotada (gris en RGB)
BG_COLOR = (192, 192, 192)

# Creación de un objeto de pose de MediaPipe con parámetros específicos
with mp_pose.Pose(
        static_image_mode=True,  # Procesar cada imagen como si fuera la única
        model_complexity=2,  # Modelo de complejidad 2 para mayor precisión
        enable_segmentation=True,  # Habilitar la segmentación de fondo
        min_detection_confidence=0.5) as pose:  # Umbral de confianza para la detección

    # Procesar cada archivo de imagen
    for idx, file in enumerate(IMAGE_FILES):
        image = cv2.imread(file)  # Leer la imagen
        image_height, image_width, _ = image.shape  # Obtener dimensiones de la imagen
        # Convertir la imagen de BGR a RGB antes del procesamiento
        results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Continuar solo si se encuentran marcas de pose
        if not results.pose_landmarks:
            continue

        # Imprimir coordenadas de la nariz
        print(
            f'Nose coordinates: ('
            f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * image_width}, '
            f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * image_height})'
        )

        # Copiar la imagen para anotarla
        annotated_image = image.copy()
        # Crear una condición para la segmentación de la imagen
        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
        # Crear una imagen de fondo
        bg_image = np.zeros(image.shape, dtype=np.uint8)
        bg_image[:] = BG_COLOR  # Asignar color de fondo
        # Aplicar la condición a la imagen anotada
        annotated_image = np.where(condition, annotated_image, bg_image)
        # Dibujar las marcas de la pose en la imagen anotada
        mp_drawing.draw_landmarks(
            annotated_image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        # Guardar la imagen anotada
        cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)
        # Representación gráfica de las marcas de la pose en el mundo 3D
        mp_drawing.plot_landmarks(
            results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

# Procesamiento de entrada de la webcam
cap = cv2.VideoCapture(0)
# Creación de un objeto de pose para la webcam
with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:  # Umbral de confianza para seguimiento

    # Bucle de captura de vídeo
    while cap.isOpened():
        success, image = cap.read()  # Leer un cuadro de la cámara web
        if not success:
            print("Ignoring empty camera frame.")  # Ignorar si el cuadro está vacío
            # Si se carga un video, usar 'break' en lugar de 'continue'
            continue

        # Opcionalmente marcar la imagen como no modificable para mejorar el rendimiento
        image.flags.writeable = False
        # Convertir la imagen a RGB y procesar
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        # Dibujar las anotaciones de la pose en la imagen
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        # Voltear la imagen horizontalmente para una visualización tipo selfie
        cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
        # Salir del bucle si se presiona la tecla ESC
        if cv2.waitKey(1) & 0xFF == 27:
            break
# Liberar la cámara al finalizar
cap.release()
