# Importamos la librería NumPy para operaciones matemáticas y manejo de arreglos.
import numpy as np
# Importamos la librería Matplotlib para crear gráficos.
import matplotlib.pyplot as plt

# Definimos dos funciones que representan las restricciones del problema de programación lineal.
def f1(x):
    # La primera restricción es constante e igual a 5.
    return 5 + 0*x

def f2(x):
    # La segunda restricción depende de x y decrece linealmente desde 8.
    return 8 - 2*x

# Generamos un rango de valores para x, desde 0 hasta 5, con 100 puntos en el intervalo.
x_values = np.linspace(0, 5, 100)

# Graficamos las dos restricciones.
plt.plot(x_values, f1(x_values), label=r'$5+0x$')  # Gráfico de la primera restricción.
plt.plot(x_values, f2(x_values), label=r'$8-2x \leq 0$')  # Gráfico de la segunda restricción.

# Rellenamos el área entre las dos funciones, donde la primera es menor o igual que la segunda,
# lo que representa la región factible del problema de programación lineal.
plt.fill_between(x_values, f1(x_values), f2(x_values), where=(f1(x_values) <= f2(x_values)), color='gray', alpha=0.5)

# Etiquetamos los ejes x e y del gráfico.
plt.xlabel('$x$')
plt.ylabel('$y$')

# Añadimos un título y una leyenda al gráfico.
plt.title('Problema de Programación Lineal')
plt.legend()

# Habilitamos la cuadrícula en el gráfico para facilitar la lectura.
plt.grid(True)

# Mostramos el gráfico.
plt.show()
