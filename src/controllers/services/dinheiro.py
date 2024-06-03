import pygame
from numerize import numerize 

class Dinheiro:
    def __init__(self, fonte, dinheiro, cor, position, fluxo=0, delay=3000):
        self.fonte = fonte
        self.dinheiro = numerize.numerize(dinheiro, 2)
        self.cor = cor
        self.image = self.fonte.render(f'${self.dinheiro}', 1, cor)
        self.position = position
        self.rect = self.image.get_rect(midleft=self.position)
        self.fluxo = fluxo
        self.delay = delay

    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def draw_ganhos(self, surface):
        if self.delay > 0:
            text_fluxo = numerize.numerize(self.fluxo, 2)
            self.image = self.fonte.render(f'+${text_fluxo}', 1, self.cor)
            self.image.set_alpha(self.delay)
            self.position[1] -= 1 if self.position[1] >= 1 else 0
            self.rect = self.image.get_rect(topleft=[self.position[0], self.position[1] + 15])
            surface.blit(self.image, self.rect)

    def draw_gastos(self, surface):
        if self.delay > 0:
            text_fluxo = numerize.numerize(abs(self.fluxo), 2)
            self.image = self.fonte.render(f'-${text_fluxo}', 1, self.cor)
            self.image.set_alpha(self.delay)
            self.position[1] += 1
            self.rect = self.image.get_rect(topleft=self.position)
            surface.blit(self.image, self.rect)
            
    def update(self, delta):
        self.delay -= delta