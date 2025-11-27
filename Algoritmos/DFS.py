import heapq
import math
import os
import random
import time
import sys


def dfs(graph_distance, origem, destino):
    sys.setrecursionlimit(1000000000)
    
    # Variáveis para rastrear o melhor caminho encontrado
    melhor_distancia = float('inf')
    melhor_caminho = []
    
    quantidade_nos_expandidos = 0
    quantidade_caminhos_explorados = 0
    
    def dfs_visit(vertice_atual, caminho_atual, distancia_atual, visitados):
        nonlocal melhor_distancia, melhor_caminho, quantidade_nos_expandidos, quantidade_caminhos_explorados
        
        quantidade_nos_expandidos += 1
        
        if vertice_atual == destino:
            quantidade_caminhos_explorados += 1
            if distancia_atual < melhor_distancia:
                melhor_distancia = distancia_atual
                melhor_caminho = caminho_atual.copy()
            return
        
        for vizinho, peso_aresta in graph_distance[vertice_atual].items():
            if vizinho not in visitados:
                nova_distancia = distancia_atual + peso_aresta
                
                novo_caminho = caminho_atual + [vizinho]
                novos_visitados = visitados | {vizinho}

                dfs_visit(vizinho, novo_caminho, nova_distancia, novos_visitados)
    
    caminho_inicial = [origem]
    visitados_inicial = {origem}
    
    dfs_visit(origem, caminho_inicial, 0, visitados_inicial)
    
    quantidade_filhos = 0
    for vertice in graph_distance.keys():
        quantidade_filhos += len(graph_distance[vertice])
    
    # Retorna o melhor caminho encontrado
    return melhor_caminho, melhor_distancia, quantidade_nos_expandidos, quantidade_caminhos_explorados
