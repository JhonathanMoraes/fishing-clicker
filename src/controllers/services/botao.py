import pygame

class Botao(pygame.sprite.Sprite):
    def __init__(self, position, image, escala):
        width = image.get_width()
        height = image.get_height()
        self.position = position
        self.image = pygame.transform.scale(image, (int(width * escala), int(height * escala)))
        self.rect = self.image.get_rect(center = self.position)

        self.angulo = 0
        self.direction = True

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def move(self, x, y):
        self.rect.move_ip(x, y)

    def shake(self, surface):
        if self.angulo > 5 or self.angulo < -5:
            self.direction = not self.direction
        
        if self.direction:
            self.angulo += 0.2
        else:
            self.angulo -= 0.2

        image = pygame.transform.rotate(self.image, self.angulo)
        surface.blit(image, self.rect)
    
    def on_event(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        
        return False

