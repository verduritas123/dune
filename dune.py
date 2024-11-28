import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
import timeit

# Mapa del desierto de Arrakis
mapa_arrakis = {
    "Arrakeen": ["Sietch Tabr", "Oasis del Norte", "Campamento Fremen"],
    "Sietch Tabr": ["Arrakeen", "Oasis del Este", "Montaña de la Especia"],
    "Oasis del Norte": ["Arrakeen", "Campamento Fremen"],
    "Campamento Fremen": ["Arrakeen", "Oasis del Norte", "Oasis del Este"],
    "Oasis del Este": ["Sietch Tabr", "Campamento Fremen", "Zona Peligrosa"],
    "Montaña de la Especia": ["Sietch Tabr", "Zona Peligrosa"],
    "Zona Peligrosa": ["Oasis del Este", "Montaña de la Especia"]
}

# 1. Función BFS para encontrar la ruta más corta
def bfs(origen, destino, grafo):
    cola = deque([origen])
    visitados = set([origen])
    padres = {origen: None}

    while cola:
        nodo_actual = cola.popleft()
        
        if nodo_actual == destino:
            ruta = []
            while nodo_actual is not None:
                ruta.insert(0, nodo_actual)
                nodo_actual = padres[nodo_actual]
            return ruta, len(ruta) - 1  # La distancia es el número de nodos - 1
        
        for vecino in grafo[nodo_actual]:
            if vecino not in visitados:
                cola.append(vecino)
                visitados.add(vecino)
                padres[vecino] = nodo_actual
    
    return None, 0  # Si no hay ruta

# 2. Función DFS para verificar la conectividad del grafo
def dfs(grafo, nodo_actual, visitados):
    visitados.add(nodo_actual)
    
    for vecino in grafo[nodo_actual]:
        if vecino not in visitados:
            dfs(grafo, vecino, visitados)

def es_conexo(grafo):
    visitados = set()
    dfs(grafo, next(iter(grafo)), visitados)
    
    if len(visitados) == len(grafo):
        print("El grafo es conexo.")
    else:
        print("El grafo no es conexo.")

#3 Ruta segura
def rutas_seguras_bfs(origen, destino, grafo, nodo_prohibido):
    cola = deque([[origen]])  # Cola de rutas, inicializada con la ruta desde el origen
    rutas_seguras = []  # Lista para almacenar las rutas válidas

    while cola:
        ruta_actual = cola.popleft()  # Extrae la ruta actual de la cola
        nodo_actual = ruta_actual[-1]  # Último nodo de la ruta actual

        if nodo_actual == destino:
            rutas_seguras.append(ruta_actual)  # Si se llega al destino, añade la ruta
            continue

        for vecino in grafo[nodo_actual]:
            if vecino != nodo_prohibido and vecino not in ruta_actual:  # Evita el nodo prohibido y ciclos
                nueva_ruta = list(ruta_actual)  # Crea una copia de la ruta actual
                nueva_ruta.append(vecino)  # Agrega el vecino a la ruta
                cola.append(nueva_ruta)  # Encola la nueva ruta

    return rutas_seguras

# 4. Melange
def buscar_melange_dfs(grafo, nodo_actual, visitados):
    print(f"Visitando: {nodo_actual}")  # Imprime el nodo visitado
    visitados.append(nodo_actual)  # Agrega el nodo actual a la lista de visitados

    for vecino in grafo[nodo_actual]:
        if vecino not in visitados:
            buscar_melange_dfs(grafo, vecino, visitados)  # Llama recursivamente para explorar vecinos

def simulacion_melange(grafo, origen):
    visitados = []  # Lista para rastrear el orden de las visitas
    buscar_melange_dfs(grafo, origen, visitados)
    return visitados

# 5. Función para graficar el grafo
def graficar_grafo(grafo, ruta=None, visitados=None):
    G = nx.Graph()
    
    # Agregar nodos y aristas
    for nodo, vecinos in grafo.items():
        for vecino in vecinos:
            G.add_edge(nodo, vecino)
    
    pos = nx.spring_layout(G)  # Disposición de los nodos en el gráfico
    
    # Dibuja el grafo
    plt.figure(figsize=(8, 6))
    nx.draw_networkx_nodes(G, pos, node_size=3000, node_color='lightblue', alpha=0.7)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    nx.draw_networkx_edges(G, pos, width=2, alpha=0.7, edge_color='black')

    if ruta:
        # Resaltar la ruta encontrada
        ruta_edges = [(ruta[i], ruta[i + 1]) for i in range(len(ruta) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=ruta_edges, width=4, edge_color='red')

    if visitados:
        # Resaltar los nodos visitados
        visitados_edges = [(visitados[i], visitados[i + 1]) for i in range(len(visitados) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=visitados_edges, width=4, edge_color='green')

    plt.title("Mapa de Arrakis y Rutas Encontradas")
    plt.axis('off')
    plt.show()

# 6. Medición de tiempos de ejecución con timeit
def medir_tiempos():
    # Funciones para medir
    def medir_bfs():
        bfs("Arrakeen", "Oasis del Norte", mapa_arrakis)

    def medir_dfs():
        dfs(mapa_arrakis, "Arrakeen", set())

    def medir_rutas_seguras():
        rutas_seguras_bfs("Arrakeen", "Montaña de la Especia", mapa_arrakis, "Zona Peligrosa")

    def medir_simulacion_melange():
        simulacion_melange(mapa_arrakis, "Arrakeen")

    # Medir tiempos usando timeit
    tiempo_bfs = timeit.timeit(medir_bfs, number=100)
    tiempo_dfs = timeit.timeit(medir_dfs, number=100)
    tiempo_rutas_seguras = timeit.timeit(medir_rutas_seguras, number=100)
    tiempo_simulacion_melange = timeit.timeit(medir_simulacion_melange, number=100)

    # Mostrar resultados
    print(f"Tiempo BFS (100 ejecuciones): {tiempo_bfs:.6f} segundos")
    print(f"Tiempo DFS (100 ejecuciones): {tiempo_dfs:.6f} segundos")
    print(f"Tiempo Rutas Seguras BFS (100 ejecuciones): {tiempo_rutas_seguras:.6f} segundos")
    print(f"Tiempo Simulación Melange DFS (100 ejecuciones): {tiempo_simulacion_melange:.6f} segundos")

# Ejecutar las búsquedas
ruta, distancia = bfs("Arrakeen", "Oasis del Norte", mapa_arrakis)
print(f"Ruta más corta desde Arrakeen hasta Oasis del Norte: {ruta} con distancia de {distancia} nodos")

# Verificar la conectividad
es_conexo(mapa_arrakis)

rutas_seguras = rutas_seguras_bfs("Arrakeen", "Montaña de la Especia", mapa_arrakis, "Zona Peligrosa")
print("Rutas seguras hacia la Montaña de la Especia:")
for ruta in rutas_seguras:
    print(" -> ".join(ruta))

# Búsqueda de Melange
print("\nBúsqueda de Melange desde Arrakeen:")
orden_exploracion = simulacion_melange(mapa_arrakis, "Arrakeen")
print("Orden de exploración:", " -> ".join(orden_exploracion))

# Graficar el mapa de Arrakis y la ruta encontrada
graficar_grafo(mapa_arrakis, ruta=ruta)

# Analizar tiempos de ejecución
medir_tiempos()
