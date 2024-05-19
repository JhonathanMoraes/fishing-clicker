import pygame

class Cesta(object):
    def __init__(self, maximo, tempo_venda, itens=[]):
        self.itens = itens
        self.maximo = maximo
        self.tempo_venda = tempo_venda

    def new_item(self, item):
        self.itens.append(item)
    
    def total(self):
        return sum(self.itens)

    def espaco_disponivel(self):
        if len(self.itens) < self.maximo:
            return True
        
        return False