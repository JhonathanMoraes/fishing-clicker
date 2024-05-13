import pygame
import random

class Peixe(object):
    def __init__(self, nome, tamanho, velocidade, valor):
        self.nome = nome
        self.tamanho = tamanho
        self.velocidade = velocidade
        #self.raridade = raridade -> implementar futuramente
        self.valor = valor