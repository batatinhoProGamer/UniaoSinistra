import pygame, pygame.mixer
from pygame.locals import *
from sys import exit
from classes import *
from config import *

pygame.init()
def menu(janela, largura_tela, altura_tela, relogio, fps):
    click = False
    imagem_de_fundo = pygame.image.load("sprites/resto/fundo_menu.png").convert_alpha()
    imagem_de_fundo = pygame.transform.scale(imagem_de_fundo, (largura_tela, altura_tela))
    fade_fundo = 0
    imagem_de_fundo.set_alpha(fade_fundo)

    logo_uniao = Botão("logo", [largura_tela // 2 - 200, 50])

    botao_jogar = Botão("botao_jogar", [largura_tela // 2 - 120, altura_tela // 2 - 150])
    botao_config = Botão("botao_config", [largura_tela // 2 - 137, altura_tela // 2 - 20])
    botao_sair = Botão("botao_sair", [largura_tela // 2 - 105, altura_tela // 2 + 110])

    pygame.mixer.music.load("audios/musicas/menu.mp3")
    pygame.mixer.music.set_volume(carregar("volume"))
    pygame.mixer.music.play(-1)
    while True:
        relogio.tick(fps)
        janela.fill((0, 0, 0))
        cursor_mouse = pygame.mouse.get_pos()

        janela.blit(imagem_de_fundo, (0, 0))

        janela.blit(logo_uniao.image, logo_uniao.rect)

        janela.blit(botao_jogar.image, botao_jogar.rect)
        janela.blit(botao_config.image, botao_config.rect)
        janela.blit(botao_sair.image, botao_sair.rect)

        imagem_de_fundo.set_alpha(fade_fundo)
        if fade_fundo < 255:
            fade_fundo += 1

        if fade_fundo > 100:
            logo_uniao.fade_in(2)

        if botao_jogar.fade < 255 and logo_uniao.fade > 200:
            botao_jogar.fade_in(3)
            botao_config.fade_in(3)
            botao_sair.fade_in(3)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            
            if event.type == MOUSEBUTTONDOWN:
                click = True

        if click and botao_jogar.fade == 255:
            if botao_jogar.rect.collidepoint(cursor_mouse):
                break

            elif botao_config.rect.collidepoint(cursor_mouse):
                config(janela, largura_tela, altura_tela, relogio, fps)

            elif botao_sair.rect.collidepoint(cursor_mouse):
                pygame.quit()
                exit()
            
        click = False
        pygame.display.update()
