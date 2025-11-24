import heapq
import math
import os
import random
import time
import sys
from collections import deque


def bfs(graph_distance, origem, destino):
    
    melhor_distancia = float('inf')
    melhor_caminho = []
    
    quantidade_nos_expandidos_bfs = 0
    quantidade_filhos_bfs = 0
    
    Q = deque()
    caminho_inicial = [origem]
    visitados_inicial = {origem}
    Q.append((origem, 0, caminho_inicial, visitados_inicial))
    
    while Q:
        vertice_atual, distancia_atual, caminho_atual, visitados_caminho = Q.popleft()
        
        quantidade_nos_expandidos_bfs += 1
        
        if vertice_atual == destino:
            if distancia_atual < melhor_distancia:
                melhor_distancia = distancia_atual
                melhor_caminho = caminho_atual.copy()
            continue
        
        numero_filhos_do_vertice_bfs = 0
        
        for vizinho, peso_aresta in graph_distance[vertice_atual].items():
            
            if vizinho not in visitados_caminho:
                
                nova_distancia = distancia_atual + peso_aresta
                
                novo_caminho = caminho_atual + [vizinho]
                novos_visitados = visitados_caminho | {vizinho}
                
                Q.append((vizinho, nova_distancia, novo_caminho, novos_visitados))
                numero_filhos_do_vertice_bfs += 1
        
        quantidade_filhos_bfs += numero_filhos_do_vertice_bfs
    
    return melhor_caminho, melhor_distancia, quantidade_nos_expandidos_bfs, quantidade_filhos_bfs

