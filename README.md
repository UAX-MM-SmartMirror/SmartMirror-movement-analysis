# 1. SmartMirror Movement Analysis Server

Este servidor Flask se utiliza para recibir datos de movimiento desde un cliente y almacenarlos para su posterior análisis. El cliente puede enviar datos de diferentes tipos, como la posición corporal, el conteo de sentadillas, los signos de mano, etc. El servidor valida los datos recibidos y los almacena en una lista, junto con un registro de tiempo.

## Algoritmo y Funcionamiento

El servidor consta de las siguientes partes principales:

### 1. Validación de Datos

Antes de almacenar los datos recibidos, el servidor valida su estructura y contenido para garantizar que cumplan con el formato esperado y contengan la información necesaria. Se utilizan diccionarios de claves esperadas para cada tipo de dato para verificar que se proporcionen todos los campos necesarios para cada tipo de dato. Además, se realizan comprobaciones específicas según el tipo de dato para asegurarse de que los valores sean del tipo correcto.

### 2. Rutas de API

El servidor tiene dos rutas de API principales:

* **'/upload' (POST)**: Esta ruta se utiliza para que el cliente envíe datos al servidor. Los datos se reciben en formato JSON y se validan antes de almacenarse en la lista de datos. Si los datos son válidos, se agrega un sello de tiempo y se almacenan junto con el tipo de dato.
* **'/data' (GET)**: Esta ruta se utiliza para recuperar datos almacenados del servidor. El cliente puede filtrar los datos por tipo y rango de tiempo especificados en los parámetros de la consulta. Los datos filtrados se devuelven al cliente en formato JSON.

### 3. Almacenamiento de Datos

Los datos recibidos y validados se almacenan en una lista llamada `data_store`. Cada entrada en esta lista contiene el tipo de dato, los datos específicos y un sello de tiempo que indica cuándo se recibió el dato.

## Ejecución del Servidor

Para ejecutar el servidor, simplemente ejecute el script Python y el servidor se iniciará en el puerto 5000 en modo de depuración.


# 2. Scripts Del Servidor
