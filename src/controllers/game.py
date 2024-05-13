import os
import pygame
import itertools
from models.moeda import Moeda
from .services.scene import Scene
from .services.botao import Botao
from .window import Window

class Game(Scene):
    def __init__(self):
        try:
            self.fonte = pygame.font.Font("src/utils/fonts/Grand9K Pixel.ttf", 18)

        except:
            self.fonte = pygame.font.Font(None, 18)

        self.fluxo_moedas = []
        self.dinheiro = 300

        self.preco_peixe = 1
        self.preco_melhoria = 10

        fish_sprite = pygame.image.load('src/utils/img/fish.png').convert_alpha()
        self.fish = Botao((80, 40), fish_sprite, 2)

        melhoria_sprite = pygame.image.load('src/utils/img/melhoria.png').convert_alpha()
        self.melhoria = Botao((160, 40), melhoria_sprite, 1)

    def on_draw(self, surface):
        surface.fill(pygame.Color(50, 150, 210))
        
        Moeda(self.fonte, f'${self.dinheiro}', (255, 255, 255), [20, 20]).draw(surface)
        Moeda(self.fonte, f'Melhoria: ${self.preco_melhoria}', (255, 255, 255), [160, 90]).draw(surface)
        
        self.fish.draw(surface)
        self.melhoria.draw(surface)

        for text in self.fluxo_moedas:
            if text.fluxo >= 0:
                text.draw_ganhos(surface)
            else:
                text.draw_gastos(surface)

    def on_update(self, delta):
        fluxo_moedas = []
        for text in self.fluxo_moedas:
            text.update(delta)
            if text.delay > 0:
                fluxo_moedas.append(text)

        self.fluxo_moedas = fluxo_moedas

    def on_event(self, event):
        if event.type == pygame.QUIT:
            Window.running = False

        # Keyboard click events
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Window.running = False

        # Mouse click events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.fish.on_event():
                    texto_timer = Moeda(self.fonte, self.dinheiro, (240, 240, 20), [20, 20], self.preco_peixe, 400)
                    self.fluxo_moedas.append(texto_timer)

                    self.dinheiro += self.preco_peixe
                
                elif self.melhoria.on_event():
                    if self.dinheiro >= self.preco_melhoria:
                        texto_timer = Moeda(self.fonte, self.dinheiro, (240, 40, 10), [20, 20], -self.preco_melhoria, 400)
                        self.fluxo_moedas.append(texto_timer)

                        self.dinheiro -= self.preco_melhoria
                        self.preco_melhoria += self.preco_peixe
                        self.preco_peixe *= 2
        
        # Mouse move events
        elif event.type == pygame.MOUSEMOTION:
            if self.fish.on_event():
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))

            elif self.melhoria.on_event() and self.dinheiro >= self.preco_melhoria:
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))

            else:
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))