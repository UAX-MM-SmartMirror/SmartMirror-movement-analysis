# Importar las librerías necesarias.
import cv2  # Para el manejo y procesamiento de imágenes.
import numpy as np  # Para operaciones matemáticas y manejo de arrays.
import pyautogui  # Para realizar capturas de pantalla y automatización de la GUI.

# Bucle infinito para capturar y mostrar continuamente la porción de pantalla seleccionada.
while True:
    # Usar PyAutoGUI para capturar una región específica de la pantalla.
    # La región está definida por las coordenadas de inicio (10, 10) y el tamaño (200, 5000).
    screenshot = pyautogui.screenshot(region=(10, 10, 200, 5000))

    # Convertir la captura de pantalla, que PyAutoGUI devuelve como un objeto Image de PIL, a un array de NumPy.
    screenshot = np.array(screenshot)

    # Convertir la imagen de RGB (el formato de color de PIL) a BGR, que es el formato de color utilizado por OpenCV.
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    # Mostrar la imagen capturada en una ventana llamada "screenshot".
    cv2.imshow("screenshot", screenshot)

    # Esperar una tecla. Si se presiona Esc (tecla 27), salir del bucle.
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Cerrar todas las ventanas de OpenCV al terminar.
cv2.destroyAllWindows()
