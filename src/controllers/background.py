import pygame
import random

class Background(pygame.sprite.Sprite):
    def __init__(self):
        self.lago = pygame.image.load(r"utils\img\laguinho.png").convert_alpha()
        self.lago = pygame.transform.scale(self.lago, (1024, 500))
        self.lago_rect = self.lago.get_rect()
        self.lago_rect.midleft = (0, 350)

        self.nuvem = pygame.image.load(r"utils\img\nuvem.png").convert_alpha()
        self.nuvem = pygame.transform.scale(self.nuvem, (300, 300))
        self.nuvem.set_alpha(150)
        self.nuvem_rect = self.nuvem.get_rect()
        self.nuvem_rect.center = (200, 150)

    def draw(self, surface):
        surface.blit(self.lago, self.lago_rect)
        surface.blit(self.nuvem, self.nuvem_rect)

        if self.nuvem_rect.centerx < 1200:
            self.nuvem_rect.centerx += 1
        else:
            rand_escala = random.randrange(100, 350)
            self.nuvem = pygame.transform.scale(self.nuvem, (rand_escala, rand_escala))
            self.nuvem = pygame.transform.flip(self.nuvem, random.choice([True, False]), random.choice([True, False]))
            self.nuvem_rect.midleft = (-300, random.randrange(100, 200))