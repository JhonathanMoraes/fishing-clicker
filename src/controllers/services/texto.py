import pygame

class Texto:
    def __init__(self, fonte, texto, cor, position):
        self.fonte = fonte
        self.texto = texto
        self.cor = cor
        self.image = self.fonte.render(str(self.texto), 1, cor)
        self.position = position
        self.rect = self.image.get_rect(midleft=self.position)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
