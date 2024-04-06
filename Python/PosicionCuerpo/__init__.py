# Importación de las bibliotecas para el procesamiento de imágenes y visión por computadora
import cv2
import mediapipe as mp
import numpy as np

# Inicialización de los módulos de dibujo y estilos de MediaPipe para la anotación de imágenes
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Inicialización del módulo Holistic de MediaPipe para la detección de poses y características faciales
mp_holistic = mp.solutions.holistic

# Definición de las imágenes estáticas a procesar, lista vacía por defecto
IMAGE_FILES = []

# Color de fondo para la imagen anotada en formato RGB (gris)
BG_COLOR = (192, 192, 192)

# Contexto de MediaPipe Holistic que procesa cada imagen estática
with mp_holistic.Holistic(
        static_image_mode=True,  # Modo para imágenes estáticas
        model_complexity=2,  # Complejidad del modelo
        enable_segmentation=True,  # Habilita la segmentación de fondo
        refine_face_landmarks=True  # Refina las marcas faciales
) as holistic:
    # Iteración sobre cada archivo de imagen en la lista
    for idx, file in enumerate(IMAGE_FILES):
        image = cv2.imread(file)  # Lectura de la imagen
        image_height, image_width, _ = image.shape  # Obtención de las dimensiones de la imagen
        # Conversión de la imagen de BGR a RGB antes de procesarla
        results = holistic.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Si se encontraron marcas de poses, imprimir las coordenadas de la nariz
        if results.pose_landmarks:
            print(
                f'Nose coordinates: ('
                f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].x * image_width}, '
                f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].y * image_height})'
            )

        # Copia de la imagen para anotarla
        annotated_image = image.copy()
        # Creación de una condición basada en la máscara de segmentación para mejorar la segmentación de bordes
        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
        # Creación de una imagen de fondo
        bg_image = np.zeros(image.shape, dtype=np.uint8)
        bg_image[:] = BG_COLOR  # Aplicación del color de fondo
        # Aplicación de la condición para combinar la imagen anotada con el fondo
        annotated_image = np.where(condition, annotated_image, bg_image)

        # Dibujo de las marcas de la pose, manos y rostro en la imagen anotada
        mp_drawing.draw_landmarks(
            annotated_image,
            results.face_landmarks,
            mp_holistic.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_tesselation_style())
        mp_drawing.draw_landmarks(
            annotated_image,
            results.pose_landmarks,
            mp_holistic.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.
            get_default_pose_landmarks_style())

        # Guardado de la imagen anotada
        cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)
        # Representación gráfica de las marcas de la pose en el mundo 3D
        mp_drawing.plot_landmarks(
            results.pose_world_landmarks, mp_holistic.POSE_CONNECTIONS)

# Procesamiento de entrada de la webcam
cap = cv2.VideoCapture(0)
with mp_holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")  # Ignorar si no hay cuadro de cámara
            # Si se carga un video, usar 'break' en lugar de 'continue'
            continue

        # Para mejora del rendimiento, opcionalmente marcar la imagen como no escribible
        image.flags.writeable = False
        # Conversión de la imagen a RGB y procesamiento
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = holistic.process(image)

        # Marcar la imagen como escribible y convertirla de vuelta a BGR para dibujar las anotaciones
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # Dibujo de las anotaciones de las marcas de pose y rostro en la imagen
        mp_drawing.draw_landmarks(
            image,
            results.face_landmarks,
            mp_holistic.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_contours_style())
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_holistic.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles
            .get_default_pose_landmarks_style())
        # Inversión horizontal de la imagen para mostrarla como si fuera un reflejo (selfie)
        cv2.imshow('MediaPipe Holistic', cv2.flip(image, 1))
        # Si se presiona ESC: salir del bucle
        if cv2.waitKey(1) & 0xFF == 27:
            break
# Liberación de la cámara
cap.release()