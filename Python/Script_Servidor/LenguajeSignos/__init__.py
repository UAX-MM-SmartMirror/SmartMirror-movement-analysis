import cv2
import mediapipe as mp
import requests
import time


class ReconocimientoGestosMano:
    def __init__(self):
        self.mp_dibujo = mp.solutions.drawing_utils
        self.mp_manos = mp.solutions.hands
        self.cap = cv2.VideoCapture(0)

    def ejecutar(self):
        ultimo_envio = time.time()  # Inicializa el tiempo del último envío al tiempo actual
        periodo_envio = 1  # Intervalo de tiempo para enviar datos, en segundos

        with self.mp_manos.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5) as manos:
            while True:
                exito, imagen = self.cap.read()
                if not exito:
                    continue

                imagen = cv2.flip(imagen, 1)
                imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
                resultados = manos.process(imagen_rgb)

                coordenadas_dedos = None

                if resultados.multi_hand_landmarks:
                    for marcas_mano in resultados.multi_hand_landmarks:
                        self.mp_dibujo.draw_landmarks(imagen, marcas_mano, self.mp_manos.HAND_CONNECTIONS)
                        coordenadas_dedos = self.extraer_coordenadas_dedos(marcas_mano)
                        break  # Solo toma las coordenadas de la primera mano detectada

                # Verifica si ha pasado suficiente tiempo desde el último envío
                if time.time() - ultimo_envio > periodo_envio:
                    if coordenadas_dedos:  # Verifica si hay coordenadas para enviar
                        letra = self.detectar_letra(coordenadas_dedos) if coordenadas_dedos else None
                        self.enviar_datos(coordenadas_dedos, letra)  # Envía datos solo si hay coordenadas
                    ultimo_envio = time.time()  # Actualiza el tiempo del último envío

                cv2.imshow("Imagen", imagen)
                if cv2.waitKey(1) & 0xFF == 27:
                    break

        self.cap.release()
        cv2.destroyAllWindows()

    def extraer_coordenadas_dedos(self, marcas_mano):
        # Asegurarse de que mp.solutions.hands.HandLandmark se itera correctamente.
        coordenadas = {}
        for dedo in mp.solutions.hands.HandLandmark:
            if 'TIP' in dedo.name:
                # Accediendo al índice del landmark del dedo.
                idx = dedo.value
                coordenada_dedo = marcas_mano.landmark[idx]  # Usar el índice para acceder al landmark.
                coordenadas[f"{dedo.name}_tip"] = {"x": coordenada_dedo.x, "y": coordenada_dedo.y,
                                                   "z": coordenada_dedo.z}

        print(f"Coordenadas de los dedos enviadas: {coordenadas}")  # Imprimir las coordenadas.
        return coordenadas

    # Esta funcion detecta la letra que se esta formando con los dedos de la mano,
    # pero hace falta realizar pruebas para verificar que la deteccion de las letras sea correcta
    def detectar_letra(self, coordenadas_dedos):
        # Simplificación; deberías expandir esta lógica para detectar más letras
        if 'INDEX_FINGER_TIP' in coordenadas_dedos and 'THUMB_TIP' in coordenadas_dedos:
            punta_indice = coordenadas_dedos['INDEX_FINGER_TIP']
            punta_pulgar = coordenadas_dedos['THUMB_TIP']
            punta_medio = coordenadas_dedos['MIDDLE_FINGER_TIP']
            punta_anular = coordenadas_dedos['RING_FINGER_TIP']
            punta_menique = coordenadas_dedos['PINKY_FINGER_TIP']

            # A: Índice más alto que los demás dedos
            if punta_indice['y'] < punta_medio['y'] < punta_anular['y'] < punta_menique['y']:
                return 'A'
            # B: Pulgar extendido hacia afuera, dedos no tan separados en el eje x
            elif abs(punta_pulgar['x'] - punta_indice['x']) > 0.1 and abs(punta_pulgar['x'] - punta_medio['x']) > 0.1:
                return 'B'
            # C: Buscando una curva abierta formada por el pulgar y los dedos
            elif punta_pulgar['x'] < punta_indice['x'] and punta_pulgar['x'] < punta_medio['x'] and punta_pulgar['y'] > \
                    punta_indice['y'] and punta_pulgar['y'] > punta_medio['y']:
                return 'C'
            # D: Pulgar e índice formando un círculo, el resto extendidos.
            elif punta_pulgar['y'] < punta_indice['y'] and punta_medio['y'] < punta_anular['y'] < punta_menique['y']:
                return 'D'
            # E: Todos los dedos juntos con una ligera curva.
            elif punta_pulgar['x'] < punta_indice['x'] < punta_medio['x'] < punta_anular['x'] < punta_menique['x']:
                return 'E'
            # F: Índice y pulgar formando un círculo, el resto extendido.
            elif punta_pulgar['y'] > punta_indice['y'] and punta_medio['y'] > punta_anular['y'] > punta_menique[
                'y']:
                return 'F'
            # G: Índice extendido, pulgar extendido formando un ángulo recto con índice.
            elif punta_pulgar['x'] > punta_indice['x'] and abs(punta_pulgar['y'] - punta_indice['y']) < 0.1:
                return 'G'
            # H: Índice y medio extendidos juntos, otros dedos doblados.
            elif punta_indice['y'] < punta_medio['y'] and punta_anular['y'] > punta_medio['y']:
                return 'H'
            # I: Menique extendido solo.
            elif punta_menique['y'] < punta_anular['y'] and punta_medio['y'] > punta_indice['y']:
                return 'I'
                # "J": Posición donde el menique esté más bajo en comparación con su posición habitual, sugiriendo un movimiento hacia abajo.
                # (Detección no precisa de "J")
            elif punta_menique['y'] > 0.5:
                return 'J'
            # K: Índice y medio forman una V, pulgar extendido.
            elif punta_indice['x'] < punta_medio['x'] and punta_pulgar['y'] < punta_indice['y']:
                return 'K'
            # L: Índice extendido hacia arriba, pulgar extendido hacia afuera.
            elif punta_indice['y'] < punta_medio['y'] and punta_pulgar['x'] < punta_indice['x']:
                return 'L'
            # M: Si el pulgar está en contacto o muy cerca de los dedos índice y medio (no es muy preciso).
            elif punta_pulgar['x'] > punta_indice['x'] and punta_pulgar['x'] < punta_medio['x']:
                return 'M'
            # N: De manera similar a 'M', pero el pulgar podría estar solo cerca del índice, no del medio.
            elif punta_pulgar['x'] > punta_indice['x'] and punta_pulgar['x'] > punta_medio['x']:
                return 'N'
            # O: Todos los dedos formando un círculo cerrado.
            elif punta_pulgar['x'] > punta_indice['x'] and punta_pulgar['y'] < punta_indice['y']:
                return 'O'
            # P: Pulgar está más alto que los otros dedos (puede dar fallos en la detección)
            elif punta_pulgar['y'] < punta_indice['y'] and punta_pulgar['y'] < punta_medio['y']:
                return 'P'
            # Q: Pulgar está más bajo que los otros dedos (puede dar fallos en la detección).
            elif punta_pulgar['y'] > punta_indice['y'] and punta_pulgar['y'] > punta_medio['y']:
                return 'Q'
            # R: Índice y medio cruzados, otros dedos retraídos.
            elif punta_indice['x'] > punta_medio['x'] and punta_menique['y'] > punta_anular['y']:
                return 'R'
            # S: Puño cerrado con pulgar cruzando sobre los dedos.
            elif punta_pulgar['x'] < punta_indice['x'] and punta_pulgar['y'] > punta_medio['y']:
                return 'S'
            # T: Pulgar metido entre índice y medio.
            elif punta_pulgar['y'] > punta_indice['y'] and punta_pulgar['x'] < punta_medio['x']:
                return 'T'
            # U: Índice y medio extendidos juntos, otros dedos doblados.
            elif punta_indice['y'] < punta_medio['y'] and punta_anular['y'] > punta_medio['y']:
                return 'U'
            # V: Índice y medio forman una V.
            elif punta_indice['x'] < punta_medio['x'] and punta_anular['y'] > punta_medio['y']:
                return 'V'
            # W: Índice, medio y anular extendidos formando una W.
            elif punta_indice['x'] < punta_medio['x'] < punta_anular['x']:
                return 'W'
            # X: Índice doblado hacia el pulgar.
            elif punta_indice['y'] > punta_pulgar['y'] and punta_medio['y'] > punta_indice['y']:
                return 'X'
            # Y: Pulgar e índice formando una forma de 'Y', otros dedos doblados.
            elif punta_pulgar['x'] < punta_indice['x'] and punta_medio['y'] > punta_indice['y']:
                return 'Y'
            # "Z": Posición del índice siendo notablemente más bajo que su posición inicial o esperada, sugiriendo un movimiento descendente.
            # No es preciso.
            elif punta_indice['y'] > 0.5:
                return 'Z'

        return None

    def mostrar_letra(self, imagen, letra):
        cv2.putText(imagen, letra, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    def enviar_datos(self, coordenadas_dedos, letra):
        datos = {
            "type": "hand_signs",
            "letter": letra,
            "finger_coordinates": coordenadas_dedos
        }
        print(f"Enviando datos al servidor: {datos}")  # Confirma los datos que se envían
        try:
            respuesta = requests.post("http://localhost:5000/upload", json=datos)
            print(
                f"Respuesta del servidor: {respuesta.status_code}, {respuesta.json()}")  # Respuesta del servidor
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")


if __name__ == "__main__":
    reconocedor = ReconocimientoGestosMano()
    reconocedor.ejecutar()