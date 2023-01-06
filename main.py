import pygame, pygame.mixer
from pygame.locals import *
from menu import *
from jogo import *
from funções import *

pygame.init()

info = pygame.display.Info()
largura_tela = info.current_w
altura_tela = info.current_h
janela = pygame.display.set_mode((largura_tela, altura_tela))
relogio = pygame.time.Clock()
fps = 60
pygame.mixer.init()

while True:
    menu(janela, largura_tela, altura_tela, relogio, fps)
    pygame.mixer.music.stop()
    janela.fill((0, 0, 0))

    fase_atual = carregar()["mapa"]
    if fase_atual == "inicio":
        inicio(janela, largura_tela, altura_tela, relogio, fps)

    fase_atual = carregar()["mapa"]
    if fase_atual == "orfanato":
        orfanato(janela, largura_tela, altura_tela, relogio, fps)

    if fase_atual == "uniao1":
        conversa(janela, largura_tela, altura_tela, fps, relogio, "Fim da primeira parte :)", "")
    pygame.mixer.music.stop()


