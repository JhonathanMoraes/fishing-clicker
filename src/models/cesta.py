import pygame

class Cesta(object):
    def __init__(self, maximo, tempo_venda, sprite, position, itens=[]):
        self.itens = itens
        self.maximo = maximo
        self.tempo_venda = tempo_venda

        self.sprite = sprite
        self.rect = self.sprite.get_rect()
        self.rect.topleft = position

    def draw(self, surface):
        surface.blit(self.sprite, self.rect)

    def new_item(self, item):
        self.itens.append(item)
    
    def total(self):
        return sum(self.itens)

    def espaco_disponivel(self):
        if len(self.itens) < self.maximo:
            return True
        
        return False