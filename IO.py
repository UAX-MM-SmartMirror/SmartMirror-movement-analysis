import numpy as np
import matplotlib.pyplot as plt

# Funciones de restricciones
def f1(x):
    return 5 + 0*x

def f2(x):
    return 8 - 2*x

# Rango de valores para x
x_values = np.linspace(0, 5, 100)

# Gráfico
plt.plot(x_values, f1(x_values), label=r'$5+0x$')
plt.plot(x_values, f2(x_values), label=r'$8-2x \leq 0$')
plt.fill_between(x_values, f1(x_values), f2(x_values), where=(f1(x_values) <= f2(x_values)), color='gray', alpha=0.5)
plt.xlabel('$x$')
plt.ylabel('$y$')
plt.title('Problema de Programación Lineal')
plt.legend()
plt.grid(True)
plt.show()