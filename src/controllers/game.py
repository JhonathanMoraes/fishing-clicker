import pygame
import json
from models.cesta import Cesta
from models.melhoria import Melhoria
from .painel import Painel
from .services.dinheiro import Dinheiro
from .services.texto import Texto
from .services.scene import Scene
from .services.botao import Botao
from .services.progress_bar import Progress_bar
from .window import Window

class Game(Scene):
    def __init__(self):

        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h
        self.margin = 20

        self.data = { 
            'game': {
                'dinheiro': 0,
                'cesta': {'maximo': 5, 'tempo_venda': 50, 'itens': []},
                'melhorias': {'preco': 10},
                'peixe': {'preco': 1}
            },

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


        self.sprites = {
            'peixe': pygame.image.load(r"utils\img\fish.png").convert_alpha(),
            'melhoria': pygame.image.load(r"utils\img\botao_melhoria.png").convert_alpha(),
            'seta_esquerda': pygame.image.load(r"utils\img\botao_seta_esquerda.png").convert_alpha(),
            'seta_direita': pygame.image.load(r"utils\img\botao_seta_direita.png").convert_alpha()
        }

        self.melhorias = {
            'Peixes frescos': Melhoria(self.fonte, Botao((self.screen_width / 2, 60), self.sprites['melhoria'], 1), 'Peixe', 'Duplica valor dos peixes.', 0, 10),
            'Cesta maior': Melhoria(self.fonte, Botao((self.screen_height / 2, 120), self.sprites['melhoria'], 1), 'Barco', 'Aumenta a capacidade da cesta', 0, 10),
        }

        self.progress_bar = {
            'fish': Progress_bar((80, 100), [60, 5], 10),
            'cesta': Progress_bar((10, 100),[50, 10], 30)
        }

        self.cesta = Cesta(self.data['game']['cesta']['maximo'], self.data['game']['cesta']['tempo_venda'], self.data['game']['cesta']['itens'])
        self.fluxo_moedas = []

        self.painel = Painel(self.melhorias, self.screen_width - 300, 0, 300, self.screen_height)
        self.botao_painel = Botao((160, 60), self.sprites['seta_direita'], 1)

        self.fish = Botao((self.screen_width / 2, self.screen_height / 3), self.sprites['peixe'], 2)

        self.melhoria = Botao((160, 60), self.sprites['melhoria'], 1)


    # Renderização dos sprites e formas
    def on_draw(self, surface):
        surface.fill(pygame.Color(50, 150, 210))
        

        if self.painel.exibir:
            self.painel.draw(surface, self.data['game']['dinheiro'])
            self.botao_painel = Botao((700, self.screen_height / 2), self.sprites['seta_direita'], 1)
        else:
            self.botao_painel = Botao((self.screen_width - self.margin, self.screen_height / 2), self.sprites['seta_esquerda'], 1)
        
        self.botao_painel.draw(surface)

        Dinheiro(self.fonte, self.data['game']['dinheiro'], (255, 255, 255), [20, 20]).draw(surface)
        Texto(self.fonte, f'Cesta: {len(self.cesta.itens)}/{self.cesta.maximo}', (255, 255, 255), [20, 110]).draw(surface)
        self.fish.draw(surface)

        if self.data['game']['melhorias']['preco'] <= self.data['game']['dinheiro']:
            self.melhoria.draw(surface)
            Dinheiro(self.fonte, self.data['game']['melhorias']['preco'], (255, 255, 255), [160, 90]).draw(surface)


        if self.progress_bar['fish'].running:
            if self.progress_bar['fish'].draw(surface):
                self.cesta.new_item(self.data['game']['peixe']['preco'])


        if not len(self.cesta.itens) < self.cesta.maximo:
            if self.progress_bar['cesta'].draw(surface):
                texto_timer = Dinheiro(self.fonte, self.data['game']['dinheiro'], (240, 240, 20), [20, 20], self.cesta.total(), 400)
                self.fluxo_moedas.append(texto_timer)
                self.data['game']['dinheiro'] += self.cesta.total()
                self.data['game']['cesta']['itens'] = self.cesta.itens = []
                


        for text in self.fluxo_moedas:
            if text.fluxo >= 0:
                text.draw_ganhos(surface)
            else:
                text.draw_gastos(surface)


    # Atualização do estado dos objetos
    def on_update(self, delta):
        fluxo_moedas = []
        for text in self.fluxo_moedas:
            text.update(delta)
            if text.delay > 0:
                fluxo_moedas.append(text)

        self.fluxo_moedas = fluxo_moedas

    # Event handler - aciona funções a partir de comandos de mouse e teclado
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
            
            elif event.key == pygame.K_TAB:
                self.painel.alternar_exibicao()


        # Mouse click events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.fish.on_event() and self.cesta.espaco_disponivel():
                    if self.progress_bar['fish'].running:
                        self.progress_bar['fish'].progress += 100 / self.progress_bar['fish'].cooldown

                    else:
                        self.progress_bar['fish'].running = True

                
                elif self.melhoria.on_event():
                    if self.data['game']['dinheiro'] >= self.data['game']['melhorias']['preco']:
                        texto_timer = Dinheiro(self.fonte, self.data['game']['dinheiro'], (240, 40, 10), [20, 20], -self.data['game']['melhorias']['preco'], 400)
                        self.fluxo_moedas.append(texto_timer)

                        self.data['game']['dinheiro'] -= self.data['game']['melhorias']['preco']
                        self.data['game']['melhorias']['preco'] = int(self.data['game']['melhorias']['preco'] * 1.5)
                        self.data['game']['peixe']['preco'] *= 2

                elif self.botao_painel.on_event():
                    self.painel.alternar_exibicao()
                
                for melhoria in self.melhorias:
                    if self.melhorias[melhoria].botao.on_event():
                        print(f'clicou, {melhoria}')

        

        # Mouse move events
        elif event.type == pygame.MOUSEMOTION:

            if self.fish.on_event():
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))

            elif self.melhoria.on_event() and self.data['game']['dinheiro'] >= self.data['game']['melhorias']['preco']:
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))

            elif self.botao_painel.on_event():
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
                
            else:
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
            
            for melhoria in self.melhorias:
                    if self.melhorias[melhoria].botao.on_event():
                        pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
