import pygame
import time
from random import randint

pygame.init()

'''criar a janela do jogo'''

back = (200, 255, 255) #cor de fundo azul claro

mw = pygame.display.set_mode((500, 500)) #mw = main window (janela principal)
mw.fill(back) # preenchimento da cor de fundo

clock = pygame.time.Clock()

'''classe retângulo'''
class Area():
    # Construtor da classe
    def __init__(self, x = 0, y = 0, width = 10, height = 10, color = None):
        self.rect = pygame.Rect(x, y, width, height) #retângulo        
        self.fill_color = color
    
    # Método para definir a nova cor
    def color(self, new_color):
        self.fill_color = new_color
    
    # Método para preencher com cor
    def fill(self):
        pygame.draw.rect(mw, self.fill_color, self.rect)
    
    # Método para criar uma linha na parte externa do triângulo
    def outline(self, frame_color, thickness):
        pygame.draw.rect(mw, frame_color, self.rect, thickness)
    
    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)
    

''' classe Label '''
class Label(Area):
    def set_text(self, text, fsize=12, text_color = (0,0,0)):
        self.image = pygame.font.SysFont('verdana',fsize).render(text, True, text_color)

    def draw(self, shift_x = 0, shift_y = 0):
        self.fill()
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

RED = (255, 0, 0) #cor vermelha
GREEN = (0, 255, 51) #cor verde
YELLOW = (255, 255, 0) #cor amarela
DARK_BLUE = (0, 0, 100) #cor azul escuro
BLUE = (80, 80, 255) #cor azul

cards = []
num_cards = 4
x = 70
wait = 0

''' Ciclo para a criação das cartas '''
for i in range(num_cards):
    new_card = Label(x, 170, 70, 100, YELLOW) #cria uma nova carta com a cor amarela
    new_card.outline(BLUE, 10) #cria uma borda com a cor azul
    new_card.set_text('CLICK', 26) #escreve o texto na carta
    cards.append(new_card)
    x = x + 100


while True:
    if wait == 0:
        #transferir a label (rótulo / etiqueta)
        wait = 20 #quantos ticks a label permanece no mesmo lugar
        click = randint(1, num_cards) 
    # for card in cards:
    #     card.draw(10, 30)
        for i in range(num_cards):
            cards[i].color(YELLOW)
            if (i + 1) == click:
                cards[i].draw(10, 40)
            else:
                cards[i].fill()
    else:
        wait = wait - 1 #é o mesmo que wait -= 1 (decremento)
    
    #verificar os clicks a cada tick
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            for i in range(num_cards):
                #verificar qual carta recebeu um click
                if cards[i].collidepoint(x, y):
                    if i + 1 == click:#se a label com a carta for clicada, adicionamos a cor verde
                        cards[i].color(GREEN)
                    else: #caso não seja, colorimos de vermelho e diminuimos um ponto
                        cards[i].color(RED)
                    cards[i].fill()

    pygame.display.update() #atualiza os gráficos da cena
    clock.tick(40) #taxa de atualização de fps
