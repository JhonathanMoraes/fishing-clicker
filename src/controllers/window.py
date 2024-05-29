import pygame
from .services.scene import Scene

class Window:
    @classmethod
    def create(self, titulo, width, height, display):
        pygame.display.set_caption(titulo)
        self.surface = pygame.display.set_mode((width, height), display)
        pygame.display.set_icon(pygame.image.load(r"utils\img\icons\koi.ico"))
        self.rect = self.surface.get_rect()
        self.clock = pygame.time.Clock()
        self.running = False
        self.delta = 0
        self.fps = 60
        self.scene = Scene()

    @classmethod
    def mainloop(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                self.scene.on_event(event)

            self.scene.on_update(self.delta)
            self.scene.on_draw(self.surface)

            pygame.display.flip()
            self.delta = self.clock.tick(self.fps)