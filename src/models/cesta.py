import pygame

class Cesta(object):
    def __init__(self, maximo, tempo_venda, sprite, position, itens=[]):
        self.itens = itens
        self.maximo = maximo
        self.tempo_venda = tempo_venda

        self.position = position
        self.sprite = sprite
        self.rect = sprite.get_rect(midleft= self.position)

    def draw(self, surface):
        image = pygame.transform.scale(self.sprite, (100, 100))
        self.rect = image.get_rect(midleft= self.position)
        surface.blit(image, self.rect)

    def new_item(self, item):
        self.itens.append(item)
    
    def total(self):
        return sum(self.itens)

    def espaco_disponivel(self):
        if len(self.itens) < self.maximo:
            return True
        
        return False

    def on_hover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        
        return False