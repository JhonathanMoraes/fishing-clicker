import pygame

class Progress_bar:
    def __init__(self, pos, tamanho, tempo, running=False, progress=0):
        self.pos = pos
        self.tamanho = tamanho
        self.tempo = tempo
        self.running = running
        self.progress = progress

    def draw(self, surface, koi=False):
        if self.progress < 100:
            pygame.draw.rect(surface, (0, 0, 0), self.pos + tuple(self.tamanho))
            ratio = self.progress / 100
            
            if koi and self.progress > 1:
                pygame.draw.rect(surface, (240, 240, 20), self.pos + tuple([int(self.tamanho[0] * ratio), self.tamanho[1]]))
                self.progress -= 0.5
            elif not koi:
                pygame.draw.rect(surface, (10, 240, 20), self.pos + tuple([int(self.tamanho[0] * ratio), self.tamanho[1]]))
                self.progress += 10 / self.tempo

        elif self.progress >= 100:
            self.running = False
            self.progress = 0
            return True
        
        return False

