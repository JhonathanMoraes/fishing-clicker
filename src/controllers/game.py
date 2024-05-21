import pygame
import json
from models.cesta import Cesta
from .painel import Painel
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
            'dinheiro': 0,
            'cesta': {'maximo': 5, 'tempo_venda': 50, 'itens': []},
            'melhorias': {'preco': 10},
            'peixe': {'preco': 1}
        }
  
        self.sprites = {
            'peixe': pygame.image.load(r"utils\img\fish.png").convert_alpha(),
            'melhorias': pygame.image.load(r"utils\img\botao_melhoria.png").convert_alpha(),
            'seta_esquerda': pygame.image.load(r"utils\img\botao_seta_esquerda.png").convert_alpha(),
            'seta_direita': pygame.image.load(r"utils\img\botao_seta_direita.png").convert_alpha()
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


        self.progress_bar = {
            'fish': Progress_bar((80, 100), [60, 5], 10),
            'cesta': Progress_bar((10, 100),[50, 10], 30)
        }

        self.cesta = Cesta(self.data['cesta']['maximo'], self.data['cesta']['tempo_venda'], self.data['cesta']['itens'])
        self.fluxo_moedas = []

        self.painel = Painel(self.screen_width, 0, 300, self.screen_height)
        self.botao_painel = Botao((160, 60), self.sprites['seta_direita'], 1)

        self.fish = Botao((self.screen_width / 2, self.screen_height / 3), self.sprites['peixe'], 2)

        self.melhorias = Botao((160, 60), self.sprites['melhorias'], 1)


    # Renderização dos sprites e formas
    def on_draw(self, surface):
        surface.fill(pygame.Color(50, 150, 210))
        
        if self.painel.exibir:
            self.painel.draw(surface)
            self.botao_painel = Botao((700, self.screen_height / 2), self.sprites['seta_direita'], 1)
        else:
            self.botao_painel = Botao((950, self.screen_height / 2), self.sprites['seta_esquerda'], 1)
        
        
        self.botao_painel.draw(surface)

        Texto(self.fonte, f'${self.data['dinheiro']}', (255, 255, 255), [20, 20]).draw(surface)
        Texto(self.fonte, f'Cesta: {len(self.cesta.itens)}/{self.cesta.maximo}', (255, 255, 255), [20, 110]).draw(surface)
        self.fish.draw(surface)

        if self.data['melhorias']['preco'] <= self.data['dinheiro']:
            self.melhorias.draw(surface)
            Texto(self.fonte, f'Melhorar: ${self.data['melhorias']['preco']}', (255, 255, 255), [160, 90]).draw(surface)


        if self.progress_bar['fish'].running:
            if self.progress_bar['fish'].draw(surface):
                self.cesta.new_item(self.data['peixe']['preco'])


        if not len(self.cesta.itens) < self.cesta.maximo:
            if self.progress_bar['cesta'].draw(surface):
                texto_timer = Texto(self.fonte, self.data['dinheiro'], (240, 240, 20), [20, 20], self.cesta.total(), 400)
                self.fluxo_moedas.append(texto_timer)
                self.data['dinheiro'] += self.cesta.total()
                self.data['cesta']['itens'] = self.cesta.itens = []
                


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

                
                elif self.melhorias.on_event():
                    if self.data['dinheiro'] >= self.data['melhorias']['preco']:
                        texto_timer = Texto(self.fonte, self.data['dinheiro'], (240, 40, 10), [20, 20], -self.data['melhorias']['preco'], 400)
                        self.fluxo_moedas.append(texto_timer)

                        self.data['dinheiro'] -= self.data['melhorias']['preco']
                        self.data['melhorias']['preco'] = int(self.data['melhorias']['preco'] * 1.5)
                        self.data['peixe']['preco'] *= 2

                elif self.botao_painel.on_event():
                    self.painel.alternar_exibicao()

        

        # Mouse move events
        elif event.type == pygame.MOUSEMOTION:
            if self.fish.on_event():
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))

            elif self.melhorias.on_event() and self.data['dinheiro'] >= self.data['melhorias']['preco']:
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))

            elif self.botao_painel.on_event():
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
                
            else:
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))