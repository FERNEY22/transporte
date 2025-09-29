import heapq
from typing import Dict, List, Tuple, Optional

# ================================
# 1. Base de conocimiento (hechos)
# ================================

CONEXIONES = [
    ("A", "B", "L1", 5),
    ("B", "C", "L1", 4),
    ("C", "D", "L1", 6),
    ("A", "E", "L2", 7),
    ("E", "F", "L2", 3),
    ("F", "D", "L2", 5),
    ("B", "E", "L3", 8),
    ("C", "F", "L3", 6),
]

PENALIZACION_TRANSFERENCIA = 3  # minutos por cambio de línea

# ================================
# 2. Funciones del sistema
# ================================

def construir_grafo(conexiones: List[Tuple[str, str, str, int]]) -> Dict[str, List[Tuple[str, str, int]]]:
    grafo = {}
    for origen, destino, linea, tiempo in conexiones:
        if origen not in grafo:
            grafo[origen] = []
        if destino not in grafo:
            grafo[destino] = []
        grafo[origen].append((destino, linea, tiempo))
        grafo[destino].append((origen, linea, tiempo))  # bidireccional
    return grafo

def encontrar_mejor_ruta(grafo: Dict[str, List[Tuple[str, str, int]]],
                        origen: str,
                        destino: str) -> Optional[Tuple[int, List[Tuple[str, str]]]]:
    if origen == destino:
        return 0, [(origen, None)]

    cola = [(0, origen, [(origen, None)], None)]
    visitados = {}

    while cola:
        tiempo_actual, nodo, ruta, ultima_linea = heapq.heappop(cola)

        if nodo in visitados and visitados[nodo] <= tiempo_actual:
            continue
        visitados[nodo] = tiempo_actual

        if nodo == destino:
            ruta_limpia = [(est, lin) for est, lin in ruta]
            return tiempo_actual, ruta_limpia

        for vecino, linea, tiempo_tramo in grafo[nodo]:
            nuevo_tiempo = tiempo_actual + tiempo_tramo
            if ultima_linea is not None and linea != ultima_linea:
                nuevo_tiempo += PENALIZACION_TRANSFERENCIA

            if vecino not in visitados or nuevo_tiempo < visitados.get(vecino, float('inf')):
                nueva_ruta = ruta + [(vecino, linea)]
                heapq.heappush(cola, (nuevo_tiempo, vecino, nueva_ruta, linea))

    return None

def mostrar_estaciones(estaciones: List[str]):
    print("\n Estaciones disponibles:")
    for i, est in enumerate(sorted(estaciones), 1):
        print(f"  {i}. {est}")
    print()

def obtener_estacion_valida(estaciones: List[str], mensaje: str) -> str:
    while True:
        entrada = input(mensaje).strip().upper()
        if entrada in estaciones:
            return entrada
        else:
            print(f" Estación '{entrada}' no válida. Por favor, elige una de la lista.")

def mostrar_ruta(tiempo: int, ruta: List[Tuple[str, str]]):
    print(f"\n Mejor ruta encontrada (tiempo estimado: {tiempo} min):")
    for i, (estacion, linea) in enumerate(ruta):
        if i == 0:
            print(f"  - Iniciar en {estacion}")
        else:
            print(f"  - Tomar línea {linea} hasta {estacion}")
    print()

def menu_principal():
    grafo = construir_grafo(CONEXIONES)
    estaciones = sorted(grafo.keys())

    print(" Bienvenido al Sistema Inteligente de Rutas del Transporte Masivo")
    print("=" * 65)

    while True:
        mostrar_estaciones(estaciones)
        origen = obtener_estacion_valida(estaciones, " Ingresa la estación de ORIGEN: ")
        destino = obtener_estacion_valida(estaciones, " Ingresa la estación de DESTINO: ")

        resultado = encontrar_mejor_ruta(grafo, origen, destino)

        if resultado is None:
            print(f"\n No se encontró una ruta entre {origen} y {destino}.")
        else:
            tiempo, ruta = resultado
            mostrar_ruta(tiempo, ruta)

        # Preguntar si desea otra búsqueda
        while True:
            repetir = input("¿Deseas calcular otra ruta? (s/n): ").strip().lower()
            if repetir in ('s', 'si', 'sí'):
                print("\n" + "="*65)
                break
            elif repetir in ('n', 'no'):
                print("\n ¡Gracias por usar el sistema! Hasta pronto.")
                return
            else:
                print("Por favor, responde 's' para sí o 'n' para no.")

# ================================
# 3. Punto de entrada
# ================================

if __name__ == "__main__":
    menu_principal()