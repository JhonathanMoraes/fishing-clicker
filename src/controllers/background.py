import pygame
import random

class Background(pygame.sprite.Sprite):
    def __init__(self):
        self.lago = pygame.image.load(r"utils\img\laguinho.png").convert_alpha()
        self.lago = pygame.transform.scale(self.lago, (1024, 500))
        self.lago_rect = self.lago.get_rect()
        self.lago_rect.midleft = (0, 350)

        self.montanha = pygame.image.load(r"utils\img\montanha.png").convert_alpha()
        self.montanha = pygame.transform.scale(self.montanha, (1024, 450))
        self.montanha_rect = self.lago.get_rect()
        self.montanha_rect.midleft = (0, 200)

    def draw(self, surface):
        surface.blit(self.lago, self.lago_rect)
        surface.blit(self.montanha, self.montanha_rect)