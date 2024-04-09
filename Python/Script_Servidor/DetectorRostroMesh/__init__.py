import cv2
import mediapipe as mp
import requests

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

url = 'http://localhost:5000/upload'
confirmed_by_server = False  # Bandera para realizar un seguimiento del estado de confirmación

# Procesamiento de imágenes estáticas
IMAGE_FILES = []  # Lista vacía para almacenar los nombres de archivos de imágenes a procesar

# Inicializamos la detección de malla facial para imágenes estáticas
with mp_face_mesh.FaceMesh(
        static_image_mode=True,  # Modo de imagen estática activado
        max_num_faces=1,  # Número máximo de caras a detectar
        refine_landmarks=True,  # Refinar los landmarks para incluir iris
        min_detection_confidence=0.5) as face_mesh:  # Umbral de confianza mínimo para la detección

    # Procesamos cada archivo de imagen en la lista
    for idx, file in enumerate(IMAGE_FILES):
        image = cv2.imread(file)  # Leer la imagen desde el archivo
        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # Procesar la imagen con MediaPipe

        # Si no se detectan landmarks faciales, pasamos a la siguiente imagen
        if not results.multi_face_landmarks:
            continue

        # Extraemos las coordenadas de los landmarks y las almacenamos en una lista
        face_landmarks_list = []
        for face_landmarks in results.multi_face_landmarks:
            for landmark in face_landmarks.landmark:
                face_landmarks_list.append((landmark.x, landmark.y, landmark.z))

        # Preparamos los datos para enviar al servidor
        data = {
            'type': 'face_mesh',  # Tipo de datos (malla facial)
            'image_path': file,  # Ruta de la imagen procesada
            'face_landmarks': face_landmarks_list  # Lista de coordenadas de landmarks faciales
        }

        # Mostramos los datos que se enviarán al servidor en la consola
        print("Datos a enviar al servidor:", data)

        # Enviamos los datos al servidor solo si no se ha confirmado previamente
        if not confirmed_by_server:
            try:
                response = requests.post(url, json=data)  # Enviar los datos como JSON al servidor
                print("Respuesta del servidor:", response.text)  # Mostrar la respuesta del servidor en la consola
                confirmed_by_server = True  # Actualizar el estado de confirmación
            except requests.exceptions.RequestException as e:
                print("Error al enviar datos:", e)  # Manejar cualquier error al enviar datos al servidor

        # Dibujamos los landmarks faciales en la imagen
        annotated_image = image.copy()
        for face_landmarks in results.multi_face_landmarks:
            # Dibujamos los diferentes componentes de la malla facial
            mp_drawing.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,  # Conexiones de la malla
                landmark_drawing_spec=None,
                connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_tesselation_style())
            mp_drawing.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_CONTOURS,  # Contornos de la cara
                landmark_drawing_spec=None,
                connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_contours_style())
            mp_drawing.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_IRISES,  # Landmarks de los iris
                landmark_drawing_spec=None,
                connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_iris_connections_style())

        # Guardamos la imagen procesada en el disco
        cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)

# Capturamos de video desde la cámara web
with mp_face_mesh.FaceMesh(
        max_num_faces=1,  # Número máximo de caras a detectar
        refine_landmarks=True,  # Refinar los landmarks para incluir iris
        min_detection_confidence=0.5,  # Umbral de confianza mínimo para la detección
        min_tracking_confidence=0.5) as face_mesh:  # Umbral de confianza mínimo para el seguimiento

    # Inicializamos la captura de video desde la cámara web
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, image = cap.read()  # Leer un frame de la cámara
        if not success:
            print("Ignorando frame vacío de la cámara.")
            continue

        # Preparamos la imagen para el procesamiento
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image)  # Procesar el frame con MediaPipe

        # Procesar los landmarks faciales detectados en el frame
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Extraemos las coordenadas de los landmarks y las almacenamos en una lista
                face_landmarks_list = []
                for landmark in face_landmarks.landmark:
                    face_landmarks_list.append((landmark.x, landmark.y, landmark.z))

                # Preparamos los datos para enviar al servidor
                data = {
                    'type': 'face_mesh',  # Tipo de datos (malla facial)
                    'face_landmarks': face_landmarks_list  # Landmarks faciales detectados en el frame
                }

                # Mostramos los datos que se enviarán al servidor en la consola
                print("Datos a enviar al servidor:", data)

                # Enviamos los datos al servidor Flask
                try:
                    response = requests.post(url, json=data)  # Enviar los datos como JSON al servidor
                    print("Respuesta del servidor:", response.text)  # Mostrar la respuesta del servidor en la consola
                    confirmed_by_server = True  # Actualizar el estado de confirmación
                except requests.exceptions.RequestException as e:
                    print("Error al enviar datos:", e)  # Manejar cualquier error al enviar datos al servidor

                # Dibujamos los landmarks faciales en el frame de la cámara
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,  # Conexiones de la malla
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_tesselation_style())
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,  # Contornos de la cara
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_contours_style())
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_IRISES,  # Landmarks de los iris
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_iris_connections_style())

        # Mostramos el frame de la cámara con los landmarks faciales dibujados
        cv2.imshow('MediaPipe Face Mesh', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break  # Salir del bucle: Tecla 'Esc'

    # Liberamos la captura de video y cerramos todas las ventanas abiertas
    cap.release()
    cv2.destroyAllWindows()
