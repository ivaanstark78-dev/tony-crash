class Analizador:
    def __init__(self):
        pass

    def calcular_valor(self, cuota, probabilidad):
        # Fórmula de Valor Esperado (EV)
        ev = (probabilidad * cuota) - 1
        return ev * 100

    def calcular_stake(self, cuota, probabilidad):
        # Criterio de Kelly (Stake recomendado como % de banca)
        if cuota <= 1: return 0
        kelly = ((cuota * probabilidad) - 1) / (cuota - 1)
        return max(0, kelly * 100)