import pygame
from numerize import numerize 

class Melhoria(object):
    def __init__(self, botao, categoria, descricao, nivel, nivel_maximo, preco):
        self.fonte = r"utils\fonts\Grand9K Pixel.ttf"
        self.botao = botao

        self.categoria = categoria
        self.descricao = descricao
        
        self.preco = preco
        
        self.nivel_maximo = nivel_maximo
        self.nivel = nivel

    def draw_melhorias(self, surface, nome, x, y, width, height, dinheiro_total):
        texto_nome = pygame.font.Font(self.fonte, 18).render(str(nome), True, (240, 240, 240))
        texto_descricao = pygame.font.Font(self.fonte, 12).render(self.descricao, True, (240, 240, 240))
        texto_preco = pygame.font.Font(self.fonte, 16).render(f'${numerize.numerize(self.preco)}', True, (240, 240, 240) if dinheiro_total >= self.preco else (150, 20, 20))
        texto_nivel = pygame.font.Font(self.fonte, 14).render(f'Lvl: {str(self.nivel) if self.nivel < self.nivel_maximo else 'MAX'}', True, (240, 240, 240))

        rect = pygame.Rect(x, y, width, height / 7)
        rect.topleft = (x, y)
        pygame.draw.rect(surface, (120, 80, 20), rect)

        rect.topleft = (x + 5, y + 5)
        surface.blit(texto_nome, rect)

        rect.topleft = (x + 5, y + 35)
        surface.blit(texto_descricao, rect)

        if self.nivel < self.nivel_maximo:
            rect.topleft = (x + 5, y + 60)
            surface.blit(texto_preco, rect)

        if dinheiro_total >= self.preco and self.nivel < self.nivel_maximo:
            self.botao.rect.topright = (x + width - 5, y + 45)
            surface.blit(self.botao.image, self.botao.rect)

            rect.topleft = (x + width / 1.45, y + 60)
            surface.blit(texto_nivel, rect)

        else:
            rect.topleft = (x + width / 1.35, y + 60)
            surface.blit(texto_nivel, rect)
