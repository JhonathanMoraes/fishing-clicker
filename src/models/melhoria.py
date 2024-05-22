import pygame
from numerize import numerize 

class Melhoria(object):
    def __init__(self, fonte, botao, categoria, descricao, nivel, preco):
        self.fonte = fonte
        self.botao = botao

        #self.icone = icone
        self.categoria = categoria
        self.descricao = descricao

        self.nivel = nivel
        self.preco = preco


    def draw_melhorias(self, surface, x, y, width, height, dinheiro_total):
        rect = pygame.Rect(x, y, width, height / 7)
        rect.topleft = (x, y)
        pygame.draw.rect(surface, (120, 80, 20), rect)

        rect.topleft = (x + 5, y)
        surface.blit(self.fonte.render(self.categoria, 1, (240, 240, 240)), rect)
        rect.topleft = (x + 5, y + 20)
        surface.blit(self.fonte.render(self.descricao, 1, (240, 240, 240)), rect)
        rect.topleft = (x + 5, y + 50)
        surface.blit(self.fonte.render(f'${numerize.numerize(self.preco)}', 1, (240, 240, 240)), rect)
        rect.topleft = (x + width - 20, y)
        surface.blit(self.fonte.render(str(self.nivel), 1, (240, 240, 240)), rect)

        if dinheiro_total >= self.preco:
            self.botao.rect.topright = (x + width - 5, y + 45)
            surface.blit(self.botao.image, self.botao.rect)
