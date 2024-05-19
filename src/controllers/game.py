import pygame
import json
from models.cesta import Cesta
from .services.texto import Texto
from .services.scene import Scene
from .services.botao import Botao
from .services.progress_bar import Progress_bar
from .window import Window

class Game(Scene):
    def __init__(self):
        self.data = { 
            'dinheiro': 0, 
            'cesta': {'maximo': 5, 'tempo_venda': 50, 'itens': []},
            'melhoria': {'preco': 10},
            'peixe': {'preco': 1}
        }
  
        try: 
            with open('game-data.txt') as load_file: 
                self.data = json.load(load_file) 

        except: 
            with open('game-data.txt', 'w') as store_file: 
                json.dump(self.data, store_file)

        try:
            self.fonte = pygame.font.Font(r"utils\fonts\Grand9K Pixel.ttf", 18)

        except:
            self.fonte = pygame.font.Font(None, 18)

        self.cesta = Cesta(self.data['cesta']['maximo'], self.data['cesta']['tempo_venda'], self.data['cesta']['itens'])
        self.progress_bar = {
            'fish': Progress_bar((80, 100), [60, 5], 10),
            'cesta': Progress_bar((10, 100),[50, 10], 30)
        }
        self.fluxo_moedas = []

        fish_sprite = pygame.image.load(r"utils\img\fish.png").convert_alpha()
        self.fish = Botao((80, 40), fish_sprite, 2)

        melhoria_sprite = pygame.image.load(r"utils\img\melhoria.png").convert_alpha()
        self.melhoria = Botao((160, 60), melhoria_sprite, 1)



    def on_draw(self, surface):
        surface.fill(pygame.Color(50, 150, 210))
        
        Texto(self.fonte, f'${self.data['dinheiro']}', (255, 255, 255), [20, 20]).draw(surface)
        Texto(self.fonte, f'Espaço na cesta: {len(self.cesta.itens)}/{self.cesta.maximo}', (255, 255, 255), [20, 110]).draw(surface)
        self.fish.draw(surface)



        if self.data['melhoria']['preco'] <= self.data['dinheiro']:
            self.melhoria.draw(surface)
            Texto(self.fonte, f'Melhorar: ${self.data['melhoria']['preco']}', (255, 255, 255), [160, 90]).draw(surface)



        if self.progress_bar['fish'].running:
            if self.progress_bar['fish'].draw(surface):
                self.cesta.new_item(self.data['peixe']['preco'])
                
        if not len(self.cesta.itens) < self.cesta.maximo:
            if self.progress_bar['cesta'].draw(surface):
                texto_timer = Texto(self.fonte, self.data['dinheiro'], (240, 240, 20), [20, 20], self.cesta.total(), 400)
                self.fluxo_moedas.append(texto_timer)
                self.data['dinheiro'] += self.cesta.total()
                self.cesta.itens = []


        for text in self.fluxo_moedas:
            if text.fluxo >= 0:
                text.draw_ganhos(surface)
            else:
                text.draw_gastos(surface)



    def on_update(self, delta):
        fluxo_moedas = []
        for text in self.fluxo_moedas:
            text.update(delta)
            if text.delay > 0:
                fluxo_moedas.append(text)

        self.fluxo_moedas = fluxo_moedas


    def on_event(self, event):
        if event.type == pygame.QUIT:
            with open('game-data.txt', 'w') as store_data:
                json.dump(self.data, store_data)
            Window.running = False

        # Keyboard click events
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                with open('game-data.txt', 'w') as store_data:
                    json.dump(self.data, store_data)

                Window.running = False


        # Mouse click events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.fish.on_event() and self.cesta.espaco_disponivel():
                    if self.progress_bar['fish'].running:
                        self.progress_bar['fish'].progress += 100 / self.progress_bar['fish'].cooldown

                    else:
                        self.progress_bar['fish'].running = True

                
                elif self.melhoria.on_event():
                    if self.data['dinheiro'] >= self.data['melhoria']['preco']:
                        texto_timer = Texto(self.fonte, self.data['dinheiro'], (240, 40, 10), [20, 20], -self.data['melhoria']['preco'], 400)
                        self.fluxo_moedas.append(texto_timer)

                        self.data['dinheiro'] -= self.data['melhoria']['preco']
                        self.data['melhoria']['preco'] = int(self.data['melhoria']['preco'] * 1.5)
                        self.data['peixe']['preco'] *= 2
        

        # Mouse move events
        elif event.type == pygame.MOUSEMOTION:
            if self.fish.on_event():
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))

            elif self.melhoria.on_event() and self.data['dinheiro'] >= self.data['melhoria']['preco']:
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))

            else:
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))