import pygame

class Botao(object):
    def __init__(self, position, image , escala):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * escala), int(height * escala)))
        self.rect = self.image.get_rect()
        self.rect.topleft = position

    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def on_event(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        
        return False
