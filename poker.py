class Carta:
    def __init__(self, valor, palo):
        self.valor = valor
        self.palo = palo

def contar_valores(mano):
    conteo = {}
    for carta in mano:
        if carta.valor in conteo:
            conteo[carta.valor] += 1
        else:
            conteo[carta.valor] = 1
    return conteo

def evaluar_mano(mano):
    conteo = contar_valores(mano)
    pares = 0
    trio = False

    for valor, cantidad in conteo.items():
        if cantidad == 2:
            pares += 1
        elif cantidad == 3:
            trio = True

    if trio and pares == 1:
        return "Full house"
    elif trio:
        return "Trío"
    elif pares == 2:
        return "Dos pares"
    elif pares == 1:
        return "Par"
    else:
        return "Mano alta"

def main():
    mano = []
    for i in range(5):  # En este ejemplo, evaluaremos una mano de 5 cartas
        valor = input(f"Introduce el valor de la carta {i+1} (2-10, J, Q, K, A): ")
        palo = input(f"Introduce el palo de la carta {i+1} (Corazones, Diamantes, Tréboles, Picas): ")
        mano.append(Carta(valor, palo))

    consejo = evaluar_mano(mano)
    print(f"Evaluación de la mano: {consejo}")

if __name__ == "__main__":
    main()
