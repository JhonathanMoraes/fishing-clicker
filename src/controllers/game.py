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

        self.data = { 
            'game': {
                'dinheiro': 0,
                'cesta': {'maximo': 5, 'tempo_venda': 50, 'itens': []},
                'melhorias': {
                    'Duplicar valor dos peixes': {
                        'categoria': 'Pescaria', 
                        'descricao': 'Duplicar valor dos peixes.',
                        'nivel': 0,
                        'nivel_maximo': 10,
                        'preco': 10
                        },
                    'Cesta maior': {
                        'categoria': 'Barco', 
                        'descricao': '+1 de capacidade na cesta.',
                        'nivel': 0,
                        'nivel_maximo': 5,
                        'preco': 10
                        }
                },
                'progress_bar': {
                    'tempo de pesca': {'tempo': 20},
                    'tempo de venda': {'tempo': 30}
                },

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
            'pescador': pygame.image.load(r"utils\img\pescador.png").convert_alpha(),
            'melhoria': pygame.image.load(r"utils\img\botao_melhoria.png").convert_alpha(),
            'seta_esquerda': pygame.image.load(r"utils\img\botao_seta_esquerda.png").convert_alpha(),
            'seta_direita': pygame.image.load(r"utils\img\botao_seta_direita.png").convert_alpha(),
            'botao_grande': pygame.image.load(r"utils\img\botao_grande.png").convert_alpha(),
            'cesta_vazia': pygame.image.load(r"utils\img\cesta_vazia.png").convert_alpha(),
            'cesta_cheia': pygame.image.load(r"utils\img\cesta_cheia.png").convert_alpha(),
            'barco': pygame.image.load(r'utils\img\barco.png').convert_alpha(),
            'vara_pesca': pygame.image.load(r'utils\img\vara_pesca.png').convert_alpha()
        }

        self.melhorias = {
            'Duplicar valor dos peixes': Melhoria(
                    Botao((0, 0), self.sprites['melhoria'], 1), 
                    self.data['game']['melhorias']['Duplicar valor dos peixes']['categoria'],
                    self.data['game']['melhorias']['Duplicar valor dos peixes']['descricao'], 
                    self.data['game']['melhorias']['Duplicar valor dos peixes']['nivel'], 
                    self.data['game']['melhorias']['Duplicar valor dos peixes']['nivel_maximo'], 
                    self.data['game']['melhorias']['Duplicar valor dos peixes']['preco']
                ),
            'Cesta maior': Melhoria(
                Botao((0, 0), self.sprites['melhoria'], 1), 
                self.data['game']['melhorias']['Cesta maior']['categoria'], 
                self.data['game']['melhorias']['Cesta maior']['descricao'], 
                self.data['game']['melhorias']['Cesta maior']['nivel'], 
                self.data['game']['melhorias']['Cesta maior']['nivel_maximo'], 
                self.data['game']['melhorias']['Cesta maior']['preco']
                )
        }

        self.progress_bar = {
            'tempo de pesca': Progress_bar((self.screen_width / 2 - 30, self.screen_height / 1.7), [60, 5], self.data['game']['progress_bar']['tempo de pesca']['tempo']),
            'tempo de venda': Progress_bar((20, 150),[50, 10], self.data['game']['progress_bar']['tempo de venda']['tempo'])
        }

        self.cesta = Cesta(self.data['game']['cesta']['maximo'], self.data['game']['cesta']['tempo_venda'], self.sprites['cesta_cheia'], (10, 90),self.data['game']['cesta']['itens'])
        self.fluxo_moedas = []

        self.painel = Painel(self.melhorias, self.screen_width - 300, 0, 300, self.screen_height)
        self.tab_painel = 'Pescaria'
        self.botao_tab_pesca_painel = Botao((self.screen_width - 220, self.screen_height / 1.05), self.sprites['botao_grande'], 1)
        self.botao_tab_barco_painel = Botao((self.screen_width - 80, self.screen_height / 1.05), self.sprites['botao_grande'], 1)
        self.expand_painel = Botao((700, 30), self.sprites['seta_direita'], 1)

        self.pescador = Botao((self.screen_width / 2, self.screen_height / 1.5), self.sprites['pescador'], 2)


    # Renderização dos sprites e formas
    def on_draw(self, surface):
        surface.fill(pygame.Color(50, 150, 210))
        pygame.draw.rect(surface, (20, 130, 190), (0, self.screen_height / 1.5, self.screen_width, self.screen_height))


        if self.painel.exibir:
            self.painel.draw(surface, self.tab_painel, self.data['game']['dinheiro'])

            self.botao_tab_pesca_painel.draw(surface)
            Botao((self.screen_width - 220, self.screen_height / 1.05), self.sprites['vara_pesca'], 1).draw(surface)

            self.botao_tab_barco_painel.draw(surface)
            Botao((self.screen_width - 80, self.screen_height / 1.05), self.sprites['barco'], 1).draw(surface)

            self.expand_painel = Botao((700, 30), self.sprites['seta_direita'], 1)
        else:
            self.expand_painel = Botao((self.screen_width - 20, 30), self.sprites['seta_esquerda'], 1)
        
        self.expand_painel.draw(surface)



        Dinheiro(self.fonte, self.data['game']['dinheiro'], (255, 255, 255), [20, 20]).draw(surface)
        Texto(self.fonte, f'Cesta: {len(self.cesta.itens)}/{self.cesta.maximo}' if len(self.cesta.itens) < self.cesta.maximo else 'Cheio!', (255, 255, 255), [50, 110]).draw(surface)
        if len(self.cesta.itens) < self.cesta.maximo:
            self.cesta.sprite = self.sprites['cesta_vazia']
        else:
            self.cesta.sprite = self.sprites['cesta_cheia']

        self.cesta.draw(surface)


        if self.progress_bar['tempo de pesca'].running:
            self.pescador.shake(surface)
            
            if self.progress_bar['tempo de pesca'].draw(surface):
                self.cesta.new_item(self.data['game']['peixe']['preco'])

        else:
            self.pescador.draw(surface)


        if not len(self.cesta.itens) < self.cesta.maximo:
            Texto(self.fonte, 'Vendendo...', (255, 255, 255), [30, 170]).draw(surface)
            if self.progress_bar['tempo de venda'].draw(surface):
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
        
        self.pescador.update(delta)

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
                if self.pescador.on_event() and self.cesta.espaco_disponivel():
                    if self.progress_bar['tempo de pesca'].running:
                        self.progress_bar['tempo de pesca'].progress += 100 / self.progress_bar['tempo de pesca'].tempo
                    else:
                        self.progress_bar['tempo de pesca'].running = True

                elif self.expand_painel.on_event():
                    self.painel.alternar_exibicao()

                if self.painel.exibir:
                    if self.botao_tab_pesca_painel.on_event():
                        self.tab_painel = 'Pescaria'
                
                    if self.botao_tab_barco_painel.on_event():
                        self.tab_painel = 'Barco'
                
                for melhoria in self.melhorias:
                    if self.melhorias[melhoria].botao.on_event() and self.melhorias[melhoria].preco <= self.data['game']['dinheiro']:
                        if self.melhorias[melhoria].categoria == self.tab_painel:
                            if self.melhorias[melhoria].nivel < self.melhorias[melhoria].nivel_maximo:
                                texto_timer = Dinheiro(self.fonte, self.data['game']['dinheiro'], (240, 40, 10), [20, 20], -self.melhorias[melhoria].preco, 400)
                                self.fluxo_moedas.append(texto_timer)

                                self.data['game']['dinheiro'] -= self.melhorias[melhoria].preco
                                self.melhorias[melhoria].nivel += 1


                                if melhoria == 'Duplicar valor dos peixes':
                                    self.data['game']['peixe']['preco'] *= 2
                                    self.melhorias[melhoria].preco *= 3
                                
                                if melhoria == 'Cesta maior':
                                    self.cesta.maximo += 1
                                    self.melhorias[melhoria].preco = int(self.melhorias[melhoria].preco * 1.5)


        # Mouse move events
        elif event.type == pygame.MOUSEMOTION:

            if self.pescador.on_event():
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
                
            elif self.expand_painel.on_event():
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))

            elif self.botao_tab_pesca_painel.on_event() and self.painel.exibir:
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))

            elif self.botao_tab_barco_painel.on_event() and self.painel.exibir:
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))

            else:
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
            
            for melhoria in self.melhorias:
                if self.melhorias[melhoria].categoria == self.tab_painel:
                    if self.melhorias[melhoria].botao.on_event() and self.melhorias[melhoria].preco <= self.data['game']['dinheiro']:
                        if self.melhorias[melhoria].nivel < self.melhorias[melhoria].nivel_maximo:
                            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
