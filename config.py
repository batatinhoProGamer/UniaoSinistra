import pygame, pygame.mixer
from pygame.locals import *
from sys import exit
from classes import *
from save_and_load import *

def config(janela, largura_tela, altura_tela, relogio, fps):
    try:
        volume = carregar("volume")
    except:
        volume = 1
        salvar(1, "volume")

    click = False
    run = True
    imagem_som = pygame.image.load("sprites/resto/som.png").convert_alpha()

    imagem_de_fundo = pygame.image.load("sprites/resto/fundo_menu.png").convert_alpha()
    imagem_de_fundo = pygame.transform.scale(imagem_de_fundo, (largura_tela, altura_tela))

    logo_uniao = Botão("logo", [largura_tela // 2 - 200, 50])

    posição_bolinha = volume * 500
    while run:
        relogio.tick(fps)
        janela.fill((0, 0, 0))
        posição_mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            
            if event.type == MOUSEBUTTONDOWN:
                click = True
            
            if event.type == KEYDOWN:
                run = False

        janela.blit(imagem_de_fundo, (0, 0))
        janela.blit(logo_uniao.image, logo_uniao.rect)
        janela.blit(imagem_som, (largura_tela // 2 - 200, altura_tela // 2 - 42))
        
        pygame.draw.line(janela, (20, 20, 20), (largura_tela // 2 - 16, altura_tela // 2 + 250), (largura_tela // 2 - 16, altura_tela // 2 + 250 - posição_bolinha), 20)
        bolinha = pygame.draw.circle(janela, (0, 0, 0), (largura_tela // 2 - 15, altura_tela // 2 + 250 - posição_bolinha), 30)

        if pygame.mouse.get_pressed()[0] and bolinha.collidepoint(posição_mouse) and altura_tela // 2 + 250 >= posição_mouse[1] >= altura_tela // 2 - 250:
            posição_bolinha = altura_tela // 2 + 250 - posição_mouse[1]
            volume = posição_bolinha / 500
            salvar(volume, "volume")
            pygame.mixer.music.set_volume(volume)

        pygame.display.update()