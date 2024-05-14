import pygame

class Texto(object):
    def __init__(self, fonte, texto, cor, position, fluxo=0, delay=3000):
        self.fonte = fonte
        self.texto = texto
        self.cor = cor
        self.image = self.fonte.render(str(self.texto), 1, cor)
        self.position = position
        self.rect = self.image.get_rect(topleft=self.position)
        self.fluxo = fluxo
        self.delay = delay

    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def draw_ganhos(self, surface):
        if self.delay > 0:
            self.image = self.fonte.render(f'+${self.fluxo}', 1, self.cor)
            self.image.set_alpha(self.delay)
            self.position[1] -= 1 if self.position[1] >= 1 else 0
            self.rect = self.image.get_rect(topleft=[self.position[0], self.position[1] + 25])
            surface.blit(self.image, self.rect)

    def draw_gastos(self, surface):
        if self.delay > 0:
            self.image = self.fonte.render(f'-${abs(self.fluxo)}', 1, self.cor)
            self.image.set_alpha(self.delay)
            self.position[1] += 1
            self.rect = self.image.get_rect(topleft=self.position)
            surface.blit(self.image, self.rect)

    def shake(self, surface):
        if self.delay > 0:
            self.image = self.fonte.render(f'-${abs(self.fluxo)}', 1, (240, 20, 10))
            self.rect = self.image.get_rect(topleft=self.position)
            surface.blit(self.image, self.rect)
            
    def update(self, delta):
        self.delay -= delta