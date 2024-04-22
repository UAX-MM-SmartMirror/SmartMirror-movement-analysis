import threading
from queue import Queue
from Python.AnalisisMovimientoServidor.Servidor import lanzar_servidor
from Python.Script_Servidor.ContadorBiceps import ContadorBiceps
from Python.Script_Servidor.ContadorFlexiones import ContadorFlexiones
from Python.Script_Servidor.ContadorSentadillas import ContadorSentadillas
from Python.AnalisisMovimientoServidor.VariablesComun import indicador_proceso
from Python.AnalisisMovimientoServidor.VariablesComun import tipo_ejercicio
from flask import Flask, jsonify, request
from datetime import datetime

class Monitor_Input:
    def __init__(self):
        self.contador_biceps = ContadorBiceps(indicador_proceso)
        self.contador_flexiones = ContadorFlexiones(indicador_proceso)
        self.contador_sentadillas = ContadorSentadillas(indicador_proceso)

    def run(self):
        biceps_thread = None
        flexiones_thread = None
        sentadillas_thread = None

        while True:
            tipo = input ("Ingrese el tipo de ejercicio ['biceps'-'flexiones'-'sentadillas'-'stop']: ")
            if tipo == 'biceps':
                if flexiones_thread and flexiones_thread.is_alive():
                    self.contador_flexiones.stop()
                    flexiones_thread.join()

                if sentadillas_thread and sentadillas_thread.is_alive():
                    self.contador_sentadillas.stop()
                    sentadillas_thread.join()

                #if face_mesh_thread and face_mesh_thread.is_alive():
                    #detector_rostro_mesh.stop()
                    #face_mesh_thread.join()

                if not biceps_thread or not biceps_thread.is_alive():
                    biceps_thread = threading.Thread(target=self.contador_biceps.run, daemon=True)
                    biceps_thread.start()

            elif tipo == 'flexiones':
                if biceps_thread and biceps_thread.is_alive():
                    self.contador_biceps.stop()
                    biceps_thread.join()

                if sentadillas_thread and sentadillas_thread.is_alive():
                    self.contador_sentadillas.stop()
                    sentadillas_thread.join()

                #if face_mesh_thread and face_mesh_thread.is_alive():
                    #detector_rostro_mesh.stop()
                    #face_mesh_thread.join()

                if not flexiones_thread or not flexiones_thread.is_alive():
                    flexiones_thread = threading.Thread(target=self.contador_flexiones.run, daemon=True)
                    flexiones_thread.start()

            elif tipo == 'sentadillas':
                if biceps_thread and biceps_thread.is_alive():
                    self.contador_biceps.stop()
                    biceps_thread.join()

                if flexiones_thread and flexiones_thread.is_alive():
                    self.contador_flexiones.stop()
                    flexiones_thread.join()

                #if face_mesh_thread and face_mesh_thread.is_alive():
                    #detector_rostro_mesh.stop()
                    #face_mesh_thread.join()'''

                if not sentadillas_thread or not sentadillas_thread.is_alive():
                    sentadillas_thread = threading.Thread(target=self.contador_sentadillas.run, daemon=True)
                    sentadillas_thread.start()

            elif tipo == 'stop':
                if biceps_thread and biceps_thread.is_alive():
                    self.contador_biceps.stop()
                    biceps_thread.join()

                if flexiones_thread and flexiones_thread.is_alive():
                    self.contador_flexiones.stop()
                    flexiones_thread.join()

                if sentadillas_thread and sentadillas_thread.is_alive():
                    self.contador_sentadillas.stop()
                    sentadillas_thread.join()

                #if face_mesh_thread and face_mesh_thread.is_alive():
                    #detector_rostro_mesh.stop()
                    #face_mesh_thread.join()'''

                print("Todos los contadores han sido detenidos.")
                break  # Salir del bucle y finalizar el script
def server_up():
    server_thread = threading.Thread(target=lanzar_servidor, daemon=True)
    server_thread.start()

    # Simula la pulsación de la tecla 'Enter'
    #pyautogui.press('enter')
    #def select_exercise(self):
        #data = request.json
        #exercise_type = data.get('type')
        #if exercise_type in ['biceps', 'flexiones', 'sentadillas']:
            #tipo_ejercicio['type'] = exercise_type
            #return jsonify({"message": f"Ejercicio {exercise_type} seleccionado"}), 200
        #else:
            #return jsonify({"error": "Tipo de ejercicio no válido"}), 400

if __name__ == "__main__":
    monitor = Monitor_Input()
    server_up()
    monitor_thread = threading.Thread(target=monitor.run)
    monitor_thread.start()

