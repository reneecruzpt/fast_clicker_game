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
LIGHT_GREEN = (200, 255, 200) #cor utilizada no ecrã de vitória
LIGHT_RED = (250, 128, 114) #cor utilizada no ecrã de tempo esgotado

cards = []
num_cards = 4
x = 70

start_time = time.time() # Marca o início do jogo, serve para controlar o tempo
cur_time = start_time # Tempo de referência para atualizar o cronômetro

#Elementos na interface (3 - Etapas: Criar o objeto, escrever o texto e desenhar o objeto)
time_text = Label(0, 0, 50, 50, back) #Texto estático "Time"
time_text.set_text('Tempo:', 40, DARK_BLUE) #Escreve no objeto criado anteriormente
time_text.draw(20, 20) #Desenha o objeto com o texto

timer = Label(50, 55, 50, 40, back) # Contador do tempo em segundos
timer.set_text('0', 40, DARK_BLUE) #define o texto para timer
timer.draw(20, 20) #desenha

score_text = Label(300, 0, 50, 50, back) #texto estático 'Count:'
score_text.set_text('Count:', 40, DARK_BLUE)
score_text.draw(20,20)

score = Label(430, 55, 50, 40, back) # Contador do tempo em segundos
score.set_text('0', 40, DARK_BLUE) #define o texto para timer
score.draw(20, 20) #desenha

''' Ciclo para a criação das cartas '''
for i in range(num_cards):
    new_card = Label(x, 170, 70, 100, YELLOW) #cria uma nova carta com a cor amarela
    new_card.outline(BLUE, 10) #cria uma borda com a cor azul
    new_card.set_text('CLICK', 26) #escreve o texto na carta
    cards.append(new_card)
    x = x + 100


points = 0 #contador de pontos
wait = 0
while True:
    if wait == 0:
        #transferir a label (rótulo / etiqueta)
        wait = 20 #quantos ticks a label permanece no mesmo lugar
        click = randint(1, num_cards) 
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
                        points += 1 #soma um ponto por acerto
                    else: #caso não seja, colorimos de vermelho e diminuimos um ponto
                        cards[i].color(RED)
                        points -= 1 #diminui um ponto por erro
                    cards[i].fill()
                    score.set_text(str(points), 40, DARK_BLUE)
                    score.draw(0, 0)

    new_time = time.time() #atualiza com o tempo corrente
    
    if new_time - start_time >= 11: #Fim do jogo após 11 segundos
        win = Label(0, 0, 500, 500, LIGHT_RED)
        win.set_text("Time's up!!!", 60, DARK_BLUE)
        win.draw(110, 180)
        pygame.display.update() #atualiza os gráficos da cena
        time.sleep(5)
        break
    
    if int(new_time) - int(cur_time) == 1: # Atualizar o contador a cada segundo
        timer.set_text(str(int(new_time - start_time)), 40, DARK_BLUE)
        timer.draw(0, 0) #etapa 3 desenhar 
        cur_time = new_time
        
    if points >= 5: #condição de vitória
        win = Label(0, 0, 500, 500, LIGHT_GREEN)
        win.set_text("You won!!!", 60, DARK_BLUE)
        win.draw(140, 180)
        
        result_time = Label(90, 230, 250, 250, LIGHT_GREEN)
        result_time.set_text("Completion time:" + str(int(new_time - start_time)) + 'sec', 40, DARK_BLUE)
        result_time.draw(0,0)
        break

    
    pygame.display.update() #atualiza os gráficos da cena
    clock.tick(40) #taxa de atualização de fps
    
pygame.display.update()