import pygame

class Progress_bar(object):
    def __init__(self, pos, tamanho, tempo, running=False, progress=0):
        self.pos = pos
        self.tamanho = tamanho
        self.tempo = tempo
        self.running = running
        self.progress = progress

    def draw(self, surface):
        if self.progress < 100:
            pygame.draw.rect(surface, (0, 0, 0), self.pos + tuple(self.tamanho))
            ratio = self.progress / 100
            pygame.draw.rect(surface, (10, 240, 20), self.pos + tuple([int(self.tamanho[0] * ratio), self.tamanho[1]]))
            self.progress += 10 / self.tempo

        elif self.progress >= 100:
            self.running = False
            self.progress = 0
            return True
        
        return False