import pulp

# Crea el problema de maximización
prob = pulp.LpProblem("Maximizar_Z", pulp.LpMaximize)

# Define las variables como enteras
x1 = pulp.LpVariable("x1", lowBound=0, cat=pulp.LpInteger)  # x1 >= 0 y entero
x2 = pulp.LpVariable("x2", lowBound=0, cat=pulp.LpInteger)  # x2 >= 0 y entero

# Función objetivo
prob += 4 * x1 + 5 * x2, "Z"

# Restricciones
prob += 2 * x1 + x2 <= 8
prob += x2 <= 5

# Resuelve el problema
prob.solve()

# Muestra el estado del problema y los valores óptimos de las variables
print("Estado:", pulp.LpStatus[prob.status])
print(f"x1 = {x1.varValue}")
print(f"x2 = {x2.varValue}")

# Muestra el valor de la función objetivo
print(f"Valor máximo de Z = {pulp.value(prob.objective)}")
