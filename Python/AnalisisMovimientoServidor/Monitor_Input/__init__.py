import threading
#import pyautogui

from Python.AnalisisMovimientoServidor.VariablesComun import indicador_proceso
from Python.Script_Servidor.ContadorBiceps import ContadorBiceps
from Python.Script_Servidor.ContadorFlexiones import ContadorFlexiones
from Python.AnalisisMovimientoServidor.Servidor import lanzar_servidor
from Python.Script_Servidor.ContadorSentadillas import ContadorSentadillas



def monitor_input():
    contador_biceps = ContadorBiceps(indicador_proceso)
    contador_flexiones = ContadorFlexiones(indicador_proceso)
    contador_sentadillas = ContadorSentadillas(indicador_proceso)
    #detector_rostro_mesh = FaceMeshDetector(indicador_proceso)

    biceps_thread = None
    flexiones_thread = None
    sentadillas_thread = None
    #face_mesh_thread = None

    while True:
        tipo = input("Ingrese el tipo de ejercicio ['biceps', 'flexiones', 'sentadillas', 'stop']: ").lower()
        if tipo == 'biceps':
            if flexiones_thread and flexiones_thread.is_alive():
                contador_flexiones.stop()
                flexiones_thread.join()

            if sentadillas_thread and sentadillas_thread.is_alive():
                contador_sentadillas.stop()
                sentadillas_thread.join()

            #if face_mesh_thread and face_mesh_thread.is_alive():
                #detector_rostro_mesh.stop()
                #face_mesh_thread.join()

            if not biceps_thread or not biceps_thread.is_alive():
                biceps_thread = threading.Thread(target=contador_biceps.run, daemon=True)
                biceps_thread.start()

        elif tipo == 'flexiones':
            if biceps_thread and biceps_thread.is_alive():
                contador_biceps.stop()
                biceps_thread.join()

            if sentadillas_thread and sentadillas_thread.is_alive():
                contador_sentadillas.stop()
                sentadillas_thread.join()

            #if face_mesh_thread and face_mesh_thread.is_alive():
                #detector_rostro_mesh.stop()
                #face_mesh_thread.join()

            if not flexiones_thread or not flexiones_thread.is_alive():
                flexiones_thread = threading.Thread(target=contador_flexiones.run, daemon=True)
                flexiones_thread.start()

        elif tipo == 'sentadillas':
            if biceps_thread and biceps_thread.is_alive():
                contador_biceps.stop()
                biceps_thread.join()

            if flexiones_thread and flexiones_thread.is_alive():
                contador_flexiones.stop()
                flexiones_thread.join()

            #if face_mesh_thread and face_mesh_thread.is_alive():
                #detector_rostro_mesh.stop()
                #face_mesh_thread.join()'''

            if not sentadillas_thread or not sentadillas_thread.is_alive():
                sentadillas_thread = threading.Thread(target=contador_sentadillas.run, daemon=True)
                sentadillas_thread.start()

        elif tipo == 'stop':
            if biceps_thread and biceps_thread.is_alive():
                contador_biceps.stop()
                biceps_thread.join()

            if flexiones_thread and flexiones_thread.is_alive():
                contador_flexiones.stop()
                flexiones_thread.join()

            if sentadillas_thread and sentadillas_thread.is_alive():
                contador_sentadillas.stop()
                sentadillas_thread.join()

            #if face_mesh_thread and face_mesh_thread.is_alive():
                #detector_rostro_mesh.stop()
                #face_mesh_thread.join()'''

            print("Todos los contadores han sido detenidos.")
            break  # Salir del bucle y finalizar el script
        else:
            print("Entrada no reconocida. Ingrese 'biceps' o 'flexiones'.")

def server_up():
    server_thread = threading.Thread(target=lanzar_servidor, daemon=True)
    server_thread.start()

    # Simula la pulsación de la tecla 'Enter'
    #pyautogui.press('enter')


if __name__ == "__main__":
    server_up()
    monitor_input()


