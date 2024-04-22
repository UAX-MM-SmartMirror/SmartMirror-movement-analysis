import threading
from Python.AnalisisMovimientoServidor.Servidor import lanzar_servidor
from Python.Script_Servidor.ContadorBiceps import ContadorBiceps
from Python.Script_Servidor.ContadorFlexiones import ContadorFlexiones
from Python.Script_Servidor.ContadorSentadillas import ContadorSentadillas
from Python.AnalisisMovimientoServidor.VariablesComun import indicador_proceso
from Python.AnalisisMovimientoServidor.VariablesComun import tipo_ejercicio


def server_up():
    monitor = Monitor_Input()
    print("Iniciando hilo principal...")
    try:
        main_program_thread = threading.Thread(target=monitor.run)
        main_program_thread.start()
        print("Hilo principal iniciado.")
    except Exception as e:
        print("Error al iniciar el hilo principal:", e)
        return

    try:
        server_process = threading.Thread(target=lanzar_servidor, daemon=True)
        server_process.start()
        print("Servidor iniciado.")
    except Exception as e:
        print("Error al iniciar el servidor:", e)
        return

    # Espera a que el hilo main_program_thread termine su ejecución
    main_program_thread.join()

    # Espera a que el proceso del servidor termine su ejecución
    server_process.join()


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
            tipo = tipo_ejercicio.get()
            if tipo == 'biceps':
                if flexiones_thread and flexiones_thread.is_alive():
                    self.contador_flexiones.stop()
                    flexiones_thread.join()

                if sentadillas_thread and sentadillas_thread.is_alive():
                    self.contador_sentadillas.stop()
                    sentadillas_thread.join()

                # if face_mesh_thread and face_mesh_thread.is_alive():
                # detector_rostro_mesh.stop()
                # face_mesh_thread.join()

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

                # if face_mesh_thread and face_mesh_thread.is_alive():
                # detector_rostro_mesh.stop()
                # face_mesh_thread.join()

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

                # if face_mesh_thread and face_mesh_thread.is_alive():
                # detector_rostro_mesh.stop()
                # face_mesh_thread.join()'''

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

                # if face_mesh_thread and face_mesh_thread.is_alive():
                # detector_rostro_mesh.stop()
                # face_mesh_thread.join()'''

                print("Todos los contadores han sido detenidos.")
                break  # Salir del bucle y finalizar el script


if __name__ == "__main__":
    server_up()
