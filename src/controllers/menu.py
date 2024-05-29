import pygame
from .services.texto import Texto
from .services.scene import Scene
from .services.botao import Botao
from .window import Window
from .game import Game

class Menu(Scene):
    def __init__(self):
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h

        self.sprites = {
            'jogar': pygame.image.load(r'utils\img\botao_jogar.png').convert_alpha(),
            'sair': pygame.image.load(r'utils\img\botao_sair.png').convert_alpha()
        }

        self.jogar = Botao((self.screen_width / 2, self.screen_height / 2.5), self.sprites['jogar'], 3)
        self.sair = Botao((self.screen_width / 2, self.screen_height / 1.5), self.sprites['sair'], 3)

    # Renderização dos sprites e formas
    def on_draw(self, surface):
        surface.fill(pygame.Color(50, 150, 210))

        self.jogar.draw(surface)
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
                if self.jogar.on_event():
                    Window.scene = Game()

                elif self.sair.on_event():
                    Window.running = False


        elif event.type == pygame.MOUSEMOTION:
            if self.jogar.on_event():
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
            elif self.sair.on_event():
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
            else:
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))