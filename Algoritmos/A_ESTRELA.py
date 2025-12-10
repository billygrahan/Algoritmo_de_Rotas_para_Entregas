import heapq
import math
import os
import random
import time
import sys

# Converte para radianos
def converter_para_radianos(valor):
    return valor * math.pi / 180

# Calcula a heuristica haversiana
def heuristica_haversiana(grafo, vertice, destino):
    x1, y1 = grafo[vertice]  # lat1, lon1
    x2, y2 = grafo[destino]  # lat2, lon2
    
    lat1 = converter_para_radianos(x1)
    lat2 = converter_para_radianos(x2)
    lon1 = converter_para_radianos(y1)
    lon2 = converter_para_radianos(y2)
    
    diferenca_latitudes = lat2 - lat1
    diferenca_longitudes = lon2 - lon1
    
    formula1 = math.sin(diferenca_latitudes / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(diferenca_longitudes / 2)**2
    formula2 = 2 * math.asin(math.sqrt(formula1))
    
    raio_terra = 6371

    return raio_terra * formula2

# Calcula a heuristica euclidiana
def heuristica_euclidiana(grafo, vertice, destino):
    x1, y1 = grafo[vertice]
    x2, y2 = grafo[destino]

    return math.sqrt( (x2-x1)**2 + (y2-y1)**2 )

def fator_de_ramificação_a_estrela(grafo):
    filhos = 0
    for no in grafo:
        filhos = filhos + len(grafo[no])
    return filhos/len(grafo)

# calcula as distancia tendo em vista a heuristica
def calcula_distancias(grafo_coordenadas, destino, heuristica):
    distancias_heuristicas = {}
    
    for origem in grafo_coordenadas.keys():
        if origem == destino:
            distancias_heuristicas[origem] = 0
        else:
            distancia_linha_reta = heuristica(grafo_coordenadas, origem, destino)
            distancias_heuristicas[origem] = distancia_linha_reta
    
    return distancias_heuristicas

# Função para reconstruir o caminho a partir dos predecessores
def reconstruir_caminho(onde_veio, atual):
    caminho_total = [atual]
    while atual in onde_veio:
        atual = onde_veio[atual]
        caminho_total.append(atual)
    caminho_total.reverse()
    return caminho_total

def distancia_caminho(caminho, grafo):
    distancia = 0
    for i in range(len(caminho) - 1):
        distancia += grafo[caminho[i]][caminho[i + 1]]
    return distancia

def a_estrela(graph_distance, graph_coordinates, origem, destino, heuristica):
    # calcula somente somente as heurísticas necessárias
    time_start_heuristica = time.time()
    
    cache_heuristicas = {}
    
    def get_heuristica(vertice):
        if vertice not in cache_heuristicas:
            cache_heuristicas[vertice] = heuristica(graph_coordinates, vertice, destino)
        return cache_heuristicas[vertice]
    
    tempo_calculo_heuristica = time.time() - time_start_heuristica

    fila_prioridade = []
    visitados = set() 
    onde_veio = {}

    valor_g = {}
    
    # Inicializa apenas os valores necessários
    for key in graph_distance.keys():
        valor_g[key] = float('inf')
    
    valor_g[origem] = 0
    h_origem = get_heuristica(origem)
    
    heapq.heappush(fila_prioridade, (h_origem, 0, origem))

    while fila_prioridade:
        f_atual, g_atual, atual = heapq.heappop(fila_prioridade)
        
        if atual == destino:
            caminho = reconstruir_caminho(onde_veio, atual)
            tempo_calculo_heuristica += time.time() - time_start_heuristica
            return caminho, distancia_caminho(caminho, graph_distance), len(visitados), fator_de_ramificação_a_estrela(graph_distance), tempo_calculo_heuristica
        
        # Ignora se já visitou este nó com custo melhor
        if atual in visitados:
            continue
            
        visitados.add(atual)

        # Explora vizinhos
        for vizinho in graph_distance[atual]:
            if vizinho in visitados:
                continue
                
            tentativa_valor_g = valor_g[atual] + graph_distance[atual][vizinho]

            if tentativa_valor_g < valor_g[vizinho]:
                onde_veio[vizinho] = atual
                valor_g[vizinho] = tentativa_valor_g
                
                h_vizinho = get_heuristica(vizinho)
                f_vizinho = tentativa_valor_g + h_vizinho
                
                heapq.heappush(fila_prioridade, (f_vizinho, tentativa_valor_g, vizinho))

    return None