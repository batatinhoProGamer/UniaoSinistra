import pygame, pygame.mixer
from pygame.locals import *
from menu import *
from jogo import *
from classes import *
from save_and_load import *
from sys import exit

def conversa(janela, largura_tela, altura_tela, fps, relogio, texto, personagem):
    quantidade_de_letras = len(texto)
    mostrar_letras = -1
    fonte = pygame.font.Font("fonte.ttf", 40)
    fonte_char = pygame.font.Font("fonte.ttf", 45)
    posição_x = 40
    posição_y = altura_tela - 200
    char = fonte_char.render(personagem, True, (255, 255, 255))
    atumalaca = 0
    lado_esquerdo = pygame.image.load("sprites/resto/conversa1.png").convert_alpha()
    meio = pygame.image.load("sprites/resto/conversa2.png").convert_alpha()
    lado_direito = pygame.image.load("sprites/resto/conversa3.png").convert_alpha()

    lado_esquerdo = pygame.transform.scale(lado_esquerdo, (288, 288))
    meio = pygame.transform.scale(meio, (largura_tela - 576, 288))
    lado_direito = pygame.transform.scale(lado_direito, (288, 288))
    
    janela.blit(lado_esquerdo, (0, altura_tela - 288))
    janela.blit(meio, (288, altura_tela - 288))
    janela.blit(lado_direito, (largura_tela - 288, altura_tela - 288))

    audio = pygame.mixer.Sound("audios/efeitos/fala.wav")
    audio.set_volume(carregar("volume"))
    audio.play(-1)
    texto_separado = texto.split()
    posicao_texto_separado = 0
    linhas = 0
    palavras_na_linha = 0
    fazendo_palavra = True

    run = True
    while run:
        relogio.tick(fps)

        if atumalaca == 0 and mostrar_letras < quantidade_de_letras - 1:
            if posição_x + len(texto_separado[posicao_texto_separado]) * 25 + 15 >= largura_tela and not fazendo_palavra:
                posição_x = 40
                posição_y += 45
                linhas += palavras_na_linha
                palavras_na_linha = 0
            
            mostrar_letras += 1
            letra = fonte.render(texto[mostrar_letras], True, (255, 255, 255))
            atumalaca = 1
            janela.blit(letra, (posição_x, posição_y))
            if texto[mostrar_letras] == " ":
                fazendo_palavra = False
                posição_x += 10
                posicao_texto_separado += 1
                palavras_na_linha += 1
            else:
                posição_x += 25
                fazendo_palavra = True
                
        else:
            atumalaca = 0

        if mostrar_letras == quantidade_de_letras -1:
            audio.stop()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            
            if event.type == MOUSEBUTTONDOWN:
                audio.stop()
                run = False

        janela.blit(char, ((largura_tela - char.get_width()) // 2, altura_tela - 250))

        pygame.display.update()


def inventario(janela, largura, altura, fps, relogio, eery):

    selecionado = [1, 0]

    imagem_inventario = pygame.image.load("sprites/resto/inventario.png").convert_alpha()
    quadrado_selecao = pygame.image.load("sprites/resto/selecao_item.png").convert_alpha()

    posicao_x = (largura - 925) // 2
    posicao_y = (altura - 588) // 2

    craft = ["", ""]
    resultado_craft = ""
    item_craft1 = False
    item_craft2 = False
    item_craft_final = False

    descricao_itens = {
        "sprites/itens/papel_queimado.png": "São as informações do gowon queimadas.",
        "sprites/itens/caneta_ruan.png": "É só uma caneta meio derretida...",
        "sprites/itens/chave_ruan.png": "Chave da casa do Ruan.",
        "sprites/itens/isqueiro.png": "Isqueiro do nicas... ele fuma?",
        "sprites/itens/livro.png": "Livro de anotações do Ruan. Aqui deve ter algo sobre o seu paradeiro.",
        "sprites/itens/oculos.png": "Um óculos que você não usa mais.",
        "sprites/itens/papel.png": "São as informações do gowon... melhor achar um jeito de destruí-las.",
        "sprites/itens/pp.png": "Então esse é o PP que tanto dizem?",
        "sprites/itens/remedio_teteca.png": "Viagra..."
    }

    resultados = {
        "sprites/itens/papel_queimado.png": ["sprites/itens/papel.png", "sprites/itens/isqueiro.png"]
    }

    fundo_descricao = pygame.image.load("sprites/resto/conversa.png").convert_alpha()

    som = pygame.mixer.Sound("audios/efeitos/inventario_som.wav")
    som.set_volume(carregar("volume"))
    run = True
    while run:
        relogio.tick(fps)
        janela.fill((0, 0, 0))
        janela.blit(imagem_inventario, ((largura - 925) // 2, (altura - 588) // 2))

        for event in pygame.event.get():
            if event.type == QUIT:
                eery.salvar()
                pygame.quit()
                exit()
            
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if item_craft1:
                        for num, itens in enumerate(eery.inventario):
                            if itens == "":
                                eery.inventario[num] = craft[0]
                                break
                    if item_craft2:
                        for num, itens in enumerate(eery.inventario):
                            if itens == "":
                                eery.inventario[num] = craft[1]
                                break
                        craft[0]
                    run = False
                    eery.salvar()
                    som.play()

                elif event.key in [K_a, K_LEFT] and selecionado not in [[0, 0], [1, 0]]:
                    selecionado[1] -= 1
                    som.play()
                    
                elif event.key in [K_w, K_UP] and selecionado[0] == 1:
                    selecionado = [0, 0]
                    som.play()

                elif event.key in [K_d, K_RIGHT] and selecionado not in [[0, 2], [1, 8]]:
                    selecionado[1] += 1
                    som.play()

                elif event.key in [K_s, K_DOWN] and selecionado[0] == 0:
                    selecionado = [1, 0]
                    som.play()

                elif event.key in [K_SPACE, K_KP_ENTER]:
                    som.play()
                    if selecionado[0] == 1:
                        if eery.inventario[selecionado[1]] != "":
                            if not item_craft1:
                                item_craft1 = True
                                craft[0] = eery.inventario[selecionado[1]]
                                eery.inventario[selecionado[1]] = ""
                            elif not item_craft2:
                                item_craft2 = True
                                craft[1] = eery.inventario[selecionado[1]]
                                eery.inventario[selecionado[1]] = ""
                        
                    else:
                        if selecionado[1] == 0 and item_craft1:
                            for num, item in enumerate(eery.inventario):
                                if item == "":
                                    eery.inventario[num] = craft[0]
                                    craft[0] = ""
                                    item_craft1 = False
                                    break
                        
                        elif selecionado[1] == 1 and item_craft2:
                            for num, item in enumerate(eery.inventario):
                                if item == "":
                                    eery.inventario[num] = craft[1]
                                    item_craft2 = False
                                    craft[1] = ""
                                    break
                        
                        elif selecionado[1] == 2 and item_craft_final:
                            item_craft1 = False
                            item_craft2 = False
                            item_craft_final = False
                            craft = ["", ""]
                            for num, item in enumerate(eery.inventario):
                                if item == "":
                                    eery.inventario[num] = resultado_craft
                                    resultado_craft = ""
                                    break
        
        for key, resultado in resultados.items():
            if craft[1] in resultado and craft[0] in resultado:
                item_craft_final = True
                resultado_craft = key

        if craft[0] != "":
            janela.blit(pygame.image.load(craft[0]).convert_alpha(), (481 + posicao_x, 200 + posicao_y))
        if craft[1] != "":
            janela.blit(pygame.image.load(craft[1]).convert_alpha(), (581 + posicao_x, 200 + posicao_y))
        if resultado_craft != "":
            janela.blit(pygame.image.load(resultado_craft).convert_alpha(), (765 + posicao_x, 200 + posicao_y))

        for num, item in enumerate(eery.inventario):
            if item != "":
                janela.blit(pygame.image.load(item).convert_alpha(), (59 + num * 89 + posicao_x + (num + 1) // 3, 439 + posicao_y))

        if selecionado[0] == 0:
            if selecionado[1] == 0:
                janela.blit(quadrado_selecao, (481 + posicao_x, 200 + posicao_y))
            elif selecionado[1] == 1:
                janela.blit(quadrado_selecao, (581 + posicao_x, 200 + posicao_y))
            elif selecionado[1] == 2:
                janela.blit(quadrado_selecao, (765 + posicao_x, 200 + posicao_y))
        else:
            janela.blit(quadrado_selecao, (59 + selecionado[1] * 89 + posicao_x + (selecionado[1] + 1) // 3, 439 + posicao_y))
            if eery.inventario[selecionado[1]] != "":
                fonte = pygame.font.Font("fonte.ttf", 25)
                texto = fonte.render(descricao_itens[eery.inventario[selecionado[1]]], True, (255, 255, 255))
                janela.blit(pygame.transform.scale(fundo_descricao, (texto.get_width() + 80, (texto.get_width() + 80) * 0.21)), (59 + selecionado[1] * 89 + posicao_x + (selecionado[1] + 1) // 3, 439 + posicao_y + 120))
                janela.blit(texto, (59 + selecionado[1] * 89 + posicao_x + (selecionado[1] + 1) // 3 + 40, 439 + posicao_y + 120 + texto.get_width() * 0.21 // 2))

        pygame.display.update()