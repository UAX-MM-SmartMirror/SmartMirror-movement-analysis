# Importar las librerías necesarias
import cv2
import mediapipe as mp

# Inicializar los módulos de dibujo y malla facial de MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

# Configurar las especificaciones de dibujo para los puntos y conexiones de la malla facial
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

# Para imágenes estáticas:
IMAGE_FILES = []  # Lista vacía, se supone que aquí irían los nombres de archivos de las imágenes a procesar
# Inicializar la detección de malla facial con configuraciones específicas
with mp_face_mesh.FaceMesh(
    static_image_mode=True,  # Modo de imagen estática activado
    max_num_faces=1,  # Número máximo de caras a detectar
    refine_landmarks=True,  # Refinamiento de puntos de referencia para incluir iris
    min_detection_confidence=0.5) as face_mesh:  # Umbral de confianza mínimo para la detección
  # Procesar cada archivo de imagen
  for idx, file in enumerate(IMAGE_FILES):
    image = cv2.imread(file)  # Leer la imagen
    # Convertir la imagen de BGR (OpenCV) a RGB (MediaPipe)
    results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Si se detectan marcas faciales, dibujarlas en la imagen
    if not results.multi_face_landmarks:
      continue  # Continuar con la siguiente imagen si no se encuentran marcas faciales
    annotated_image = image.copy()
    for face_landmarks in results.multi_face_landmarks:
      print('face_landmarks:', face_landmarks)
      mp_drawing.draw_landmarks(
          image=annotated_image,
          landmark_list=face_landmarks,
          connections=mp_face_mesh.FACEMESH_TESSELATION,
          landmark_drawing_spec=None,
          connection_drawing_spec=mp_drawing_styles
          .get_default_face_mesh_tesselation_style())
      mp_drawing.draw_landmarks(
          image=annotated_image,
          landmark_list=face_landmarks,
          connections=mp_face_mesh.FACEMESH_CONTOURS,
          landmark_drawing_spec=None,
          connection_drawing_spec=mp_drawing_styles
          .get_default_face_mesh_contours_style())
      mp_drawing.draw_landmarks(
          image=annotated_image,
          landmark_list=face_landmarks,
          connections=mp_face_mesh.FACEMESH_IRISES,
          landmark_drawing_spec=None,
          connection_drawing_spec=mp_drawing_styles
          .get_default_face_mesh_iris_connections_style())
    cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)

# Para entrada de webcam:
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(0)
with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # Marcar la imagen como no modificable para mejorar el rendimiento
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image)

    # Dibujar las mallas faciales en el frame de la webcam
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_face_landmarks:
      for face_landmarks in results.multi_face_landmarks:
          # Dibujar mallas faciales, contornos y iris
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_tesselation_style())
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_contours_style())
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_IRISES,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_iris_connections_style())
    # Mostrar el frame con una vista tipo selfie
    cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))
    # Salir si se presiona ESC
    if cv2.waitKey(5) & 0xFF == 27:
      break

# Liberar recursos al terminar
cap.release()