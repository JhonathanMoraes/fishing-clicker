from models.peixe import Peixe
from controllers.window import Window
from controllers.game import Game
import pygame

def main():
    pygame.init()
    Window.create("Fishing Clicker", 1600, 900)
    Window.scene = Game()
    Window.mainloop()

main()