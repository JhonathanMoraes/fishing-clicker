import os
import pygame
from .background import Background
from .services.texto import Texto
from .services.scene import Scene
from .services.botao import Botao
from .window import Window

class Final(Scene):
    def __init__(self):
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h

        self.fonte = pygame.font.Font(r"utils\fonts\Grand9K Pixel.ttf", 18)

        os.remove('game-data.txt')

        self.sprites = {
            'koi': pygame.image.load(r'utils\img\koi.png').convert_alpha(),
            'sair': pygame.image.load(r'utils\img\botao_sair.png').convert_alpha()
        }

        self.koi_image = pygame.transform.scale(self.sprites['koi'], (80, 80))
        self.koi_rect = self.koi_image.get_rect(center= (self.screen_width / 2, self.screen_height / 2.6))

        self.sair = Botao((self.screen_width / 2, self.screen_height / 1.2), self.sprites['sair'], 1.5)

    # Renderização dos sprites e formas
    def on_draw(self, surface):
        Background().draw(surface)

        container_rect = pygame.Rect(self.screen_width / 2, self.screen_height / 2, 400, 250)
        container_rect.center = (self.screen_width / 2, self.screen_height / 2)
        pygame.draw.rect(surface, (90, 50, 10), container_rect)
        
        surface.blit(self.koi_image, self.koi_rect)

        Texto(self.fonte, 'Parabéns! Você pescou o peixe Koi.', (255, 255, 255), [self.screen_width / 2.9, self.screen_height / 2.1]).draw(surface)
        Texto(self.fonte, 'Obrigado por jogar!', (255, 255, 255), [self.screen_width / 2.45, self.screen_height / 1.6]).draw(surface)

        self.sair.draw(surface)


    # Event handler - aciona funções a partir de comandos de mouse e teclado
    def on_event(self, event):
        if event.type == pygame.QUIT:
            Window.running = False

        # Keyboard click events
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Window.running = False


        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.sair.on_event():
                    Window.running = False


        elif event.type == pygame.MOUSEMOTION:
            if self.sair.on_event():
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
            else:
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))