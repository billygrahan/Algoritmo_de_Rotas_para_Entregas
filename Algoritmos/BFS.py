import heapq
import math
import os
import random
import time
import sys

# Busca em Largura Modificada (BFS)
# Explora TODOS os caminhos possíveis até a fila esvaziar
# Sempre atualiza quando encontra um caminho com MENOR CUSTO TOTAL

def bfs(graph_distance, origem, destino):
    """
    BFS que explora TODOS os caminhos até a fila esvaziar.
    Sempre que encontra o destino, verifica se o custo é menor
    que o melhor caminho encontrado anteriormente.
    """
    distancias = {}
    predecessores = {}
    
    quantidade_nos_expandidos_bfs = 0
    quantidade_filhos_bfs = 0
    
    # Inicialização: todas as distâncias começam como infinito
    for vertice in graph_distance.keys():
        distancias[vertice] = float('inf')
        predecessores[vertice] = None
    
    # A distância da origem para ela mesma é 0
    distancias[origem] = 0
    
    # Fila: armazena (distância_acumulada, vértice_atual)
    fila_vertices = [(0, origem)]
    
    while fila_vertices:
        # Remove o primeiro da fila
        distancia_atual, vertice_atual = fila_vertices.pop(0)
        
        quantidade_nos_expandidos_bfs += 1
        
        # NÃO PARA AQUI - continua explorando mesmo se for o destino
        # Se a distância atual já é maior que a melhor conhecida, pula
        # if distancia_atual > distancias[vertice_atual]:
        #     continue
        
        numero_filhos_do_vertice_bfs = 0
        
        # Explora todos os vizinhos
        for vizinho, peso_aresta in graph_distance[vertice_atual].items():
            # Calcula a nova distância até o vizinho
            nova_distancia = distancia_atual + peso_aresta
            
            # ✅ ATUALIZA se encontrou um caminho MELHOR (menor custo)
            if nova_distancia < distancias[vizinho]:
                distancias[vizinho] = nova_distancia
                predecessores[vizinho] = vertice_atual
                
                # Adiciona o vizinho na fila para explorar seus vizinhos
                fila_vertices.append((nova_distancia, vizinho))
                numero_filhos_do_vertice_bfs += 1
        
        quantidade_filhos_bfs += numero_filhos_do_vertice_bfs
    
    rota = []
    caminho_atual = destino
    
    # Reconstrói o caminho do destino até a origem
    while caminho_atual is not None:
        rota.append(caminho_atual)
        caminho_atual = predecessores[caminho_atual]
    
    rota.reverse()
    
    # A distância total já está calculada em distancias[destino]
    distancia_total = distancias[destino]
    
    return rota, distancia_total, quantidade_nos_expandidos_bfs, quantidade_filhos_bfs
