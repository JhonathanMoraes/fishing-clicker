from models.peixe import Peixe
from controllers.window import Window
from controllers.game import Game
import json
import pygame

try: 
    with open('game-config.txt') as load_config: 
        config = json.load(load_config) 

except: 
    with open('game-config.txt', 'w') as load_config:
        config = {
            'screen': {
                'width': 1024,
                'height' : 600,
                'display': 0
            },

            'game': {
                'titulo': 'Fishing Clicker'
            }
        }
        json.dump(config, load_config)

def main():
    pygame.init()
    Window.create(config['game']['titulo'], config['screen']['width'], config['screen']['height'], config['screen']['display'])
    Window.scene = Game()
    Window.mainloop()

main()