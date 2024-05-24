import pygame
from .services.texto import Texto

class Painel(object):
    def __init__(self, melhorias, x, y, width, height):
        self.fonte = r"utils\fonts\Grand9K Pixel.ttf"
        self.melhorias = melhorias

        self.x, self.y = x, y
        self.width, self.height = width, height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect.topleft = (self.x, self.y)

        self.exibir = False
        
    def draw(self, surface, categoria, dinheiro_total):
        if self.exibir:
            pygame.draw.rect(surface, (90, 50, 10), self.rect)
            Texto(pygame.font.Font(self.fonte, 26), categoria, (240, 240, 240), (self.x + 10, 25)).draw(surface)

            x, y = self.x, 55
            for melhoria in self.melhorias:
                if self.melhorias[melhoria].categoria == categoria:
                    self.melhorias[melhoria].draw_melhorias(surface, x, y, self.width, self.height, dinheiro_total)
                    y += 100

    def alternar_exibicao(self):
        self.exibir = not self.exibir