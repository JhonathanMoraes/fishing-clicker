import pygame
import json
from numerize import numerize
from models.cesta import Cesta
from models.melhoria import Melhoria
from .final import Final
from .painel import Painel
from .background import Background
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
                    'Peixes raros': {
                        'categoria': 'Pesca', 
                        'descricao': 'Aumenta o valor dos peixes em 50%.',
                        'nivel': 0,
                        'nivel_maximo': 20,
                        'preco': 50
                        },
                    'Iscas vivas': {
                        'categoria': 'Pesca', 
                        'descricao': 'Reduz o tempo de pesca em 5.',
                        'nivel': 0,
                        'nivel_maximo': 12,
                        'preco': 20
                        },

                    'Cesta maior': {
                        'categoria': 'Barco', 
                        'descricao': '+1 de capacidade da cesta.',
                        'nivel': 0,
                        'nivel_maximo': 5,
                        'preco': 40
                        },
                    'Barco mais rápido': {
                        'categoria': 'Barco', 
                        'descricao': 'Reduz o tempo de venda em 10.',
                        'nivel': 0,
                        'nivel_maximo': 5,
                        'preco': 40
                        },
                    'Investimentos': {
                        'categoria': 'Barco', 
                        'descricao': 'Renda passiva de 1% do valor investido.',
                        'nivel': 0,
                        'nivel_maximo': 10,
                        'preco': 100
                    }
                },
                'progress_bar': {
                    'tempo de pesca': {'tempo': 70},
                    'tempo de venda': {'tempo': 100},
                    'tempo de renda passiva': {'tempo': 10}
                },

                'peixe': {'preco': 10},
                'renda passiva': 0
            },

        }

        try: 
            with open('game-data.txt') as load_file: 
                self.data = json.load(load_file) 

        except: 
            with open('game-data.txt', 'w') as store_file: 
                json.dump(self.data, store_file)

        self.fonte = pygame.font.Font(r"utils\fonts\Grand9K Pixel.ttf", 18)

        self.sprites = {
            'pescador': pygame.image.load(r"utils\img\pescador.png").convert_alpha(),
            'melhoria': pygame.image.load(r"utils\img\botao_melhoria.png").convert_alpha(),
            'seta_esquerda': pygame.image.load(r"utils\img\botao_seta_esquerda.png").convert_alpha(),
            'seta_direita': pygame.image.load(r"utils\img\botao_seta_direita.png").convert_alpha(),
            'botao_pesca': pygame.image.load(r"utils\img\botao_pesca.png").convert_alpha(),
            'botao_barco': pygame.image.load(r"utils\img\botao_barco.png").convert_alpha(),
            'cesta_vazia': pygame.image.load(r"utils\img\cesta_vazia.png").convert_alpha(),
            'cesta_cheia': pygame.image.load(r"utils\img\cesta_cheia.png").convert_alpha(),
            'koi': pygame.image.load(r"utils\img\koi.png").convert_alpha()
        }

        self.melhorias = {
            'Peixes raros': Melhoria(
                Botao((0, 0), self.sprites['melhoria'], 1), 
                self.data['game']['melhorias']['Peixes raros']['categoria'],
                self.data['game']['melhorias']['Peixes raros']['descricao'], 
                self.data['game']['melhorias']['Peixes raros']['nivel'], 
                self.data['game']['melhorias']['Peixes raros']['nivel_maximo'], 
                self.data['game']['melhorias']['Peixes raros']['preco']
                ),
            'Iscas vivas': Melhoria(
                Botao((0, 0), self.sprites['melhoria'], 1), 
                self.data['game']['melhorias']['Iscas vivas']['categoria'],
                self.data['game']['melhorias']['Iscas vivas']['descricao'], 
                self.data['game']['melhorias']['Iscas vivas']['nivel'], 
                self.data['game']['melhorias']['Iscas vivas']['nivel_maximo'], 
                self.data['game']['melhorias']['Iscas vivas']['preco']
                ),

            'Cesta maior': Melhoria(
                Botao((0, 0), self.sprites['melhoria'], 1), 
                self.data['game']['melhorias']['Cesta maior']['categoria'], 
                self.data['game']['melhorias']['Cesta maior']['descricao'], 
                self.data['game']['melhorias']['Cesta maior']['nivel'], 
                self.data['game']['melhorias']['Cesta maior']['nivel_maximo'], 
                self.data['game']['melhorias']['Cesta maior']['preco']
                ),
            'Barco mais rápido': Melhoria(
                Botao((0, 0), self.sprites['melhoria'], 1), 
                self.data['game']['melhorias']['Barco mais rápido']['categoria'], 
                self.data['game']['melhorias']['Barco mais rápido']['descricao'], 
                self.data['game']['melhorias']['Barco mais rápido']['nivel'], 
                self.data['game']['melhorias']['Barco mais rápido']['nivel_maximo'], 
                self.data['game']['melhorias']['Barco mais rápido']['preco']
                ),
            'Investimentos': Melhoria(
                Botao((0, 0), self.sprites['melhoria'], 1), 
                self.data['game']['melhorias']['Investimentos']['categoria'], 
                self.data['game']['melhorias']['Investimentos']['descricao'], 
                self.data['game']['melhorias']['Investimentos']['nivel'], 
                self.data['game']['melhorias']['Investimentos']['nivel_maximo'], 
                self.data['game']['melhorias']['Investimentos']['preco']
                )
        }

        self.progress_bar = {
            'tempo de pesca': Progress_bar((self.screen_width / 2.23, self.screen_height / 1.8), [120, 10], self.data['game']['progress_bar']['tempo de pesca']['tempo']),
            'tempo de venda': Progress_bar((self.screen_width / 2.23, self.screen_height / 2),[110, 20], self.data['game']['progress_bar']['tempo de venda']['tempo']),
            'tempo de renda passiva': Progress_bar((20, self.screen_height / 6 + 20),[100, 5], self.data['game']['progress_bar']['tempo de renda passiva']['tempo'])
        }

        self.background = Background()

        self.cesta = Cesta(
            self.data['game']['cesta']['maximo'], 
            self.data['game']['cesta']['tempo_venda'], 
            self.sprites['cesta_vazia'], 
            (10, self.screen_height / 1.12),
            self.data['game']['cesta']['itens']
            )
        self.expand_cesta = False

        self.fluxo_moedas = []

        self.painel = Painel(self.melhorias, self.screen_width - 300, 0, 300, self.screen_height)
        self.tab_painel = 'Pesca'
        self.botao_tab_pesca_painel = Botao((self.screen_width - 220, self.screen_height / 1.05), self.sprites['botao_pesca'], 1)
        self.botao_tab_barco_painel = Botao((self.screen_width - 80, self.screen_height / 1.05), self.sprites['botao_barco'], 1)
        self.expand_painel = Botao((700, 30), self.sprites['seta_direita'], 1)

        self.pescador = Botao((self.screen_width / 2, self.screen_height / 1.5), self.sprites['pescador'], 3)

        self.koi = False


    # Renderização dos sprites e formas
    def on_draw(self, surface):
        surface.fill(pygame.Color(50, 150, 210))
        self.background.draw(surface)


        if self.painel.exibir:
            self.painel.draw(surface, self.tab_painel, self.data['game']['dinheiro'])

            self.botao_tab_pesca_painel.draw(surface)
            self.botao_tab_barco_painel.draw(surface)

            self.expand_painel = Botao((700, 30), self.sprites['seta_direita'], 1)
        else:
            self.expand_painel = Botao((self.screen_width - 20, 30), self.sprites['seta_esquerda'], 1)
        
        self.expand_painel.draw(surface)


        pygame.draw.rect(surface, (90, 50, 10), pygame.Rect(0, 3, 200, 40))
        Dinheiro(self.fonte, self.data['game']['dinheiro'], (240, 240, 220), [20, 20]).draw(surface)


        if self.progress_bar['tempo de pesca'].running:
            self.pescador.shake(surface)
            
            if self.progress_bar['tempo de pesca'].draw(surface, self.koi):
                if self.koi:
                    Window.scene = Final()
                    self.koi = False
                else:
                    self.cesta.new_item(self.data['game']['peixe']['preco'])

        else:
            self.pescador.draw(surface)


        if not len(self.cesta.itens) < self.cesta.maximo:
            self.cesta.sprite = self.sprites['cesta_cheia']
            Texto(self.fonte, 'Vendendo...', (255, 255, 255), [self.screen_width / 2.23, self.screen_height / 2.15]).draw(surface)
            if self.progress_bar['tempo de venda'].draw(surface):
                texto_timer = Dinheiro(self.fonte, self.data['game']['dinheiro'], (240, 240, 20), [20, 20], self.cesta.total(), 400)
                self.fluxo_moedas.append(texto_timer)

                self.data['game']['dinheiro'] += self.cesta.total()
                self.data['game']['cesta']['itens'] = self.cesta.itens = []
        else:
            self.cesta.sprite = self.sprites['cesta_vazia']
            
        self.cesta.draw(surface)
        if self.expand_cesta:
            Texto(self.fonte, f'Peixes: {len(self.cesta.itens)}/{self.cesta.maximo}', (255, 255, 255), [self.screen_width / 9, self.screen_height / 1.07]).draw(surface)


        if self.data['game']['renda passiva'] > 0:
            pygame.draw.rect(surface, (90, 50, 10), pygame.Rect(0, self.screen_height / 7.5, 300, 60))
            Texto(self.fonte, f'Renda passiva: +${numerize.numerize(self.data['game']['renda passiva'], 2)}', (255, 255, 255), [20, self.screen_height / 6]).draw(surface)
            if self.progress_bar['tempo de renda passiva'].draw(surface):
                texto_timer = Dinheiro(self.fonte, self.data['game']['dinheiro'], (240, 240, 20), [20, 20], self.data['game']['renda passiva'], 400)
                self.fluxo_moedas.append(texto_timer)

                self.data['game']['dinheiro'] += self.data['game']['renda passiva']
                self.progress_bar['tempo de renda passiva'].running = True
            

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
                        self.tab_painel = 'Pesca'
                
                    if self.botao_tab_barco_painel.on_event():
                        self.tab_painel = 'Barco'
                        
                
                for melhoria in self.melhorias:
                    if self.melhorias[melhoria].botao.on_event() and self.melhorias[melhoria].preco <= self.data['game']['dinheiro']:
                        if self.melhorias[melhoria].categoria == self.tab_painel:
                            if self.melhorias[melhoria].nivel < self.melhorias[melhoria].nivel_maximo:
                                texto_timer = Dinheiro(self.fonte, self.data['game']['dinheiro'], (240, 40, 10), [20, 20], -self.melhorias[melhoria].preco, 400)
                                self.fluxo_moedas.append(texto_timer)

                                self.data['game']['dinheiro'] -= self.melhorias[melhoria].preco


                                if melhoria == 'Peixes raros':
                                    self.data['game']['peixe']['preco'] = int(self.data['game']['peixe']['preco'] * 1.5)

                                    self.data['game']['melhorias']['Peixes raros']['nivel'] += 1
                                    self.data['game']['melhorias']['Peixes raros']['preco'] = int(self.data['game']['melhorias']['Peixes raros']['preco'] * 1.4)

                                elif melhoria == 'Iscas vivas':
                                    self.data['game']['progress_bar']['tempo de pesca']['tempo'] -= 5
                                    self.progress_bar['tempo de pesca'].tempo = self.data['game']['progress_bar']['tempo de pesca']['tempo']

                                    self.data['game']['melhorias']['Iscas vivas']['nivel'] += 1
                                    self.data['game']['melhorias']['Iscas vivas']['preco'] += 300
                                
                                
                                elif melhoria == 'Cesta maior':
                                    self.data['game']['cesta']['maximo'] += 1
                                    self.cesta.maximo = self.data['game']['cesta']['maximo']

                                    self.data['game']['melhorias']['Cesta maior']['nivel'] += 1
                                    self.data['game']['melhorias']['Cesta maior']['preco'] = int(self.data['game']['melhorias']['Cesta maior']['preco'] * 1.5)

                                elif melhoria == 'Barco mais rápido':
                                    self.data['game']['progress_bar']['tempo de venda']['tempo'] -= 10
                                    self.progress_bar['tempo de venda'].tempo = self.data['game']['progress_bar']['tempo de venda']['tempo']

                                    self.data['game']['melhorias']['Barco mais rápido']['nivel'] += 1
                                    self.data['game']['melhorias']['Barco mais rápido']['preco'] += 300
                                
                                elif melhoria == 'Investimentos':
                                    self.data['game']['renda passiva'] += int(self.data['game']['melhorias']['Investimentos']['preco'] * 0.01)

                                    self.data['game']['melhorias']['Investimentos']['nivel'] += 1
                                    self.data['game']['melhorias']['Investimentos']['preco'] *= 2

                                self.melhorias[melhoria].nivel = self.data['game']['melhorias'][melhoria]['nivel']
                                self.melhorias[melhoria].preco = self.data['game']['melhorias'][melhoria]['preco']


                                nivel_atual = sum([self.data['game']['melhorias'][melhoria]['nivel'] for melhoria in self.data['game']['melhorias']])
                                nivel_maximo = sum([self.data['game']['melhorias'][melhoria]['nivel_maximo'] for melhoria in self.data['game']['melhorias']])

                                if nivel_atual >= nivel_maximo:
                                    self.koi = True


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
            
            if self.cesta.on_hover():
                self.expand_cesta = True
            else:
                self.expand_cesta = False
            
            for melhoria in self.melhorias:
                if self.melhorias[melhoria].categoria == self.tab_painel:
                    if self.melhorias[melhoria].botao.on_event() and self.melhorias[melhoria].preco <= self.data['game']['dinheiro']:
                        if self.melhorias[melhoria].nivel < self.melhorias[melhoria].nivel_maximo:
                            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
