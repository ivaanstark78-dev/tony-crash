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

    def seleccionar_mejor_opcion(self, lista_mercados):
        # Filtramos cuotas menores a 1.50 para evitar riesgos excesivos
        validas = [m for m in lista_mercados if m['cuota'] >= 1.50]
        
        if not validas:
            return None, "❌ No encontré opciones con suficiente valor (todas las cuotas son menores a 1.50)."
        
        # Seleccionamos la de mayor cuota
        mejor = max(validas, key=lambda x: x['cuota'])
        return mejor, f"He analizado {len(lista_mercados)} opciones."