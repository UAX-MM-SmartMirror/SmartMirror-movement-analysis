# Servidor de Monitoreo de Ejercicios

Este proyecto implementa un servidor para recibir, validar y almacenar datos relacionados con ejercicios enviados desde aplicaciones cliente. Soporta varios tipos de ejercicios y maneja diferentes tipos de entradas de datos relacionados con movimientos corporales.

## Características

- **Validación de Datos:** Asegura que todos los datos entrantes coincidan con los formatos esperados y contengan los campos requeridos según el tipo de ejercicio.
- **Compartición de Recursos de Origen Cruzado (CORS):** Configurado para aceptar solicitudes de cualquier origen.
- **Monitoreo de Ejercicios:** Soporta ejercicios como sentadillas, curls de bíceps y flexiones, y puede manejar dinámicamente datos entrantes basados en el tipo de ejercicio.
- **Procesamiento Concurrente:** Utiliza hilos para gestionar procesos de monitoreo de ejercicios sin bloquear las operaciones principales del servidor.

## Ejecución

Para ejecutar este servidor, necesitarás Python 3.x y Flask.

