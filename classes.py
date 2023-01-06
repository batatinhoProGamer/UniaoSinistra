import pygame, pygame.mixer
from pygame.locals import *
from save_and_load import *


pygame.init()

class Botão(pygame.sprite.Sprite):
    def __init__(self, imagem, lugar):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("sprites/resto/" + imagem + ".png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = lugar[0]
        self.rect.y = lugar[1]
        self.fade = 0
        self.image.set_alpha(self.fade)

    def fade_in(self, valor=1):
        self.fade += valor
        self.image.set_alpha(self.fade)

    def fade_out(self, valor=1):
        self.fade -= valor
        self.image.set_alpha(self.fade)


class Eery(pygame.sprite.Sprite):
    def __init__(self, mapa):
        pygame.sprite.Sprite.__init__(self)
        eery_save = carregar("sprites/eery/eery_saves")

        self.sprites = []
        imagens = []
        posições = ["costas", "direita", "frente", "esquerda"]
        for c in range(0, 4):
            imagens.append(pygame.image.load("sprites/eery/" + posições[c] + "_parada.png").convert_alpha())
            imagens.append(pygame.image.load("sprites/eery/" + posições[c] + "_correndo1.png").convert_alpha())
            imagens.append(pygame.image.load("sprites/eery/" + posições[c] + "_correndo2.png").convert_alpha())
            self.sprites.append(imagens)
            imagens = []

        self.movimento = 0
        self.chegada = [0, 0]
        self.animacao = 0
        self.direção = eery_save["direcao"]
        self.image = self.sprites[self.direção][self.animacao]
        self.posição = eery_save["posicao"]
        self.olhar = eery_save["olhar"]
        self.andando = False
        self.numero_de_fala = eery_save["numero de fala"]

        self.dialogos = carregar("sprites/eery/dialogos")[mapa]
        self.inventario = eery_save["inventario"]

    def mudar_olhar(self, direção):
        self.direção = direção
        self.image = self.sprites[self.direção][int(self.animacao)]

        if direção == 0:
            self.olhar = self.posição.copy()
            self.olhar[1] -= 1

        elif direção == 1:
            self.olhar = self.posição.copy()
            self.olhar[0] += 1
        
        elif direção == 2:
            self.olhar = self.posição.copy()
            self.olhar[1] += 1
        
        else:
            self.olhar = self.posição.copy()
            self.olhar[0] -= 1

    def update(self, segurando_botao, rate=0.075):
        self.animacao += rate

        if self.animacao > 2:
            self.animacao = 0

        self.image = self.sprites[self.direção][int(self.animacao) + 1]
        if self.movimento == 0 and not segurando_botao:
            self.image = self.sprites[self.direção][0]

    def salvar(self):
        saving_eery = {
            "posicao": self.posição,
            "olhar": self.olhar,
            "direcao": self.direção,
            "inventario": self.inventario,
            "numero de fala": self.numero_de_fala
        }
        salvar(saving_eery, "sprites/eery/eery_saves")

    def andar(self, direcao_andar, tabela, posições_objetos=[]):
        self.mudar_olhar(direcao_andar)
        if direcao_andar == 0:
            self.olhar = self.posição.copy()
            self.olhar[1] -= 1

            andar = True
            if len(posições_objetos) > 0:
                for c in range(0, len(posições_objetos)):
                    if posições_objetos[c].posição == self.olhar:
                        andar = False
                        break

            if andar and tabela[self.olhar[1]][self.olhar[0]] == " ":
                self.andando = True
                self.chegada = self.posição.copy()
                self.chegada[1] -= 1
                self.olhar = self.posição.copy()
                self.olhar[1] -= 2
        
        elif direcao_andar == 1:
            self.olhar = self.posição.copy()
            self.olhar[0] += 1
            
            andar = True
            if len(posições_objetos) > 0:
                for c in range(0, len(posições_objetos)):
                    if posições_objetos[c].posição == self.olhar:
                        andar = False
                        break

            if andar and tabela[self.olhar[1]][self.olhar[0]] == " ":
                self.andando = True
                self.chegada = self.posição.copy()
                self.chegada[0] += 1
                self.olhar = self.posição.copy()
                self.olhar[0] += 2
        
        elif direcao_andar == 2:
            self.olhar = self.posição.copy()
            self.olhar[1] += 1

            andar = True
            if len(posições_objetos) > 0:
                for c in range(0, len(posições_objetos)):
                    if posições_objetos[c].posição == self.olhar:
                        andar = False
                        break

            if andar and tabela[self.olhar[1]][self.olhar[0]] == " ":
                self.andando = True
                self.chegada = self.posição.copy()
                self.chegada[1] += 1
                self.olhar = self.posição.copy()
                self.olhar[1] += 2
        
        else:
            self.olhar = self.posição.copy()
            self.olhar[0] -= 1

            andar = True
            if len(posições_objetos) > 0:
                for c in range(0, len(posições_objetos)):
                    if posições_objetos[c].posição == self.olhar:
                        andar = False
                        break

            if andar and tabela[self.olhar[1]][self.olhar[0]] == " ":
                self.andando = True
                self.chegada = self.posição.copy()
                self.chegada[0] -= 1
                self.olhar = self.posição.copy()
                self.olhar[0] -= 2

    def carregar(self, janela, canto_mapa=[], largura=0, altura=0):
        if canto_mapa != []:
            if self.direção == 0:
                janela.blit(self.image, (canto_mapa[0] + self.posição[0] * 64 + 4, canto_mapa[1] + self.posição[1] * 64 - self.movimento))
            elif self.direção == 1:
                janela.blit(self.image, (canto_mapa[0] + self.posição[0] * 64 + 4 + self.movimento, canto_mapa[1] + self.posição[1] * 64))
            elif self.direção == 2:
                janela.blit(self.image, (canto_mapa[0] + self.posição[0] * 64 + 4, canto_mapa[1] + self.posição[1] * 64 + self.movimento))
            else:
                janela.blit(self.image, (canto_mapa[0] + self.posição[0] * 64 + 4 - self.movimento, canto_mapa[1] + self.posição[1] * 64))
        else:
            if self.direção == 0:
                janela.blit(self.image, ((largura - 96) // 2, (altura - 128) // 2 - self.movimento))
            elif self.direção == 1:
                janela.blit(self.image, ((largura - 96) // 2 + self.movimento, (altura - 128) // 2))
            elif self.direção == 2:
                janela.blit(self.image, ((largura - 96) // 2, (altura - 128) // 2 + self.movimento))
            else:
                janela.blit(self.image, ((largura - 96) // 2 - self.movimento, (altura - 128) // 2))
        

class Batatinho(pygame.sprite.Sprite):
    def __init__(self, mapa, offsetx=0, offsety=0):
        pygame.sprite.Sprite.__init__(self)
        batatinho_saves = carregar("sprites/batatinho/batatinho_saves")

        self.mapa = mapa
        self.offsetx = offsetx
        self.offsety = offsety
        self.nome = "batatinho"
        self.sprites = []
        imagens = []
        posições = ["costas", "direita", "frente", "esquerda"]
        for c in range(0, 4):
            imagens.append(pygame.image.load("sprites/batatinho/" + posições[c] + "_parado.png").convert_alpha())
            imagens.append(pygame.image.load("sprites/batatinho/" + posições[c] + "_correndo1.png").convert_alpha())
            imagens.append(pygame.image.load("sprites/batatinho/" + posições[c] + "_correndo2.png").convert_alpha())
            self.sprites.append(imagens)
            imagens = []

        self.portal = pygame.image.load("sprites/batatinho/portal.png").convert_alpha()
        self.portal_pos = []

        self.numero_de_fala = batatinho_saves["numero de fala"]
        self.movimento = 0
        self.chegada = [0, 0]
        self.animacao = 0
        self.direção = batatinho_saves["direcao"]
        self.image = self.sprites[self.direção][self.animacao]
        self.posição = batatinho_saves["posicao"]
        self.olhar = batatinho_saves["olhar"]
        self.andando = False
        self.dialogo_interação = carregar("sprites/batatinho/dialogos")["interacao"][mapa]

        self.dialogos = carregar("sprites/batatinho/dialogos")[mapa]

    def colocar_portal(self):
        self.portal_pos = self.olhar.copy()

    def mudar_olhar(self, direção):
        self.direção = direção
        self.image = self.sprites[self.direção][int(self.animacao)]

        if direção == 0:
            self.olhar = self.posição.copy()
            self.olhar[1] -= 1

        elif direção == 1:
            self.olhar = self.posição.copy()
            self.olhar[0] += 1
        
        elif direção == 2:
            self.olhar = self.posição.copy()
            self.olhar[1] += 1
        
        else:
            self.olhar = self.posição.copy()
            self.olhar[0] -= 1

    def update(self):
        self.animacao += 0.1

        if self.animacao > 2:
            self.animacao = 0

        self.image = self.sprites[self.direção][int(self.animacao) + 1]
        if self.movimento == 0 and not self.andando:
            self.image = self.sprites[self.direção][0]

    def carregar(self, janela, canto_mapa):
        if self.portal_pos != [] and self.mapa == "orfanato":
            janela.blit(self.portal, (canto_mapa[0] + self.portal_pos[0] * 64 + 4 - 32, canto_mapa[1] + self.portal_pos[1] * 64 - self.movimento + self.offsety))

        if self.direção == 0:
            janela.blit(self.image, (canto_mapa[0] + self.posição[0] * 64 + 4 + self.offsetx, canto_mapa[1] + self.posição[1] * 64 - self.movimento + self.offsety))
        elif self.direção == 1:
            janela.blit(self.image, (canto_mapa[0] + self.posição[0] * 64 + 4 + self.movimento + self.offsetx, canto_mapa[1] + self.posição[1] * 64 + self.offsety))
        elif self.direção == 2:
            janela.blit(self.image, (canto_mapa[0] + self.posição[0] * 64 + 4 + self.offsetx, canto_mapa[1] + self.posição[1] * 64 + self.movimento + self.offsety))
        else:
            janela.blit(self.image, (canto_mapa[0] + self.posição[0] * 64 + 4 - self.movimento + self.offsetx, canto_mapa[1] + self.posição[1] * 64 + self.offsety))

    def salvar(self):
        saving_batatinho = {
            "posicao": self.posição,
            "olhar": self.olhar,
            "direcao": self.direção,
            "numero de fala": self.numero_de_fala
        }
        salvar(saving_batatinho, "sprites/batatinho/batatinho_saves")

    def interação(self):
        pass

    def andar(self, direcao_andar):
        self.mudar_olhar(direcao_andar)
        if direcao_andar == 0:
            self.olhar = self.posição.copy()
            self.olhar[1] -= 1

            self.andando = True
            self.chegada = self.posição.copy()
            self.chegada[1] -= 1
        
        elif direcao_andar == 1:
            self.olhar = self.posição.copy()
            self.olhar[0] += 1

            self.andando = True
            self.chegada = self.posição.copy()
            self.chegada[0] += 1
        
        elif direcao_andar == 2:
            self.olhar = self.posição.copy()
            self.olhar[1] += 1

            self.andando = True
            self.chegada = self.posição.copy()
            self.chegada[1] += 1
        
        else:
            self.olhar = self.posição.copy()
            self.olhar[0] -= 1

            self.andando = True
            self.chegada = self.posição.copy()
            self.chegada[0] -= 1

    
class Gif(pygame.sprite.Sprite):
    def __init__(self, imagens, posição, brilho=False, item="", descrição="", tabela_pos=0, offsetx = 0, offsety = 0):
        pygame.sprite.Sprite.__init__(self)

        self.imagens = []
        for c in range(0, len(imagens)):
            self.imagens.append(pygame.image.load("sprites/" + imagens[c] + ".png").convert_alpha())
        
        self.offsetx = offsetx
        self.offsety = offsety

        self.contador = 0
        self.image = self.imagens[0]
        self.posição = posição
        if brilho:
            self.caminho = item
            self.descrição = descrição
            self.tabela_pos = tabela_pos

    def update(self, janela, canto_mapa):
        self.contador += 0.075
        if self.contador // 1 >= len(self.imagens):
            self.contador = 0
        
        self.image = self.imagens[int(self.contador)]
        
        janela.blit(self.image, (canto_mapa[0] + self.posição[0] * 64 + self.offsetx, canto_mapa[1] + self.posição[1] * 64 + self.offsety))


class Mapa(pygame.sprite.Sprite):
    def __init__(self, multipla=False, imagem="", imagens=[], posicao=[0, 0]):
        pygame.sprite.Sprite.__init__(self)
        self.multipla = multipla
        self.posicao = posicao

        if multipla:
            self.imagem = []
            for imagem in imagens:
                self.imagem.append(pygame.image.load(imagem).convert_alpha())
        else:
            self.imagem = pygame.image.load(imagem).convert_alpha()
    
    def atualizar(self, janela, numero=0):
        if self.multipla:
            janela.blit(self.imagem[numero], (self.posicao[0], self.posicao[1]))
        else:
            janela.blit(self.imagem, (self.posicao[0], self.posicao[1]))


class Personagem(pygame.sprite.Sprite):
    def __init__(self, caminho_pasta, nome, offsetx = 0, offsety = 0):
        pygame.sprite.Sprite.__init__(self)
        self.nome = nome
        self.conteudo = carregar(caminho_pasta + "/" + nome + "/saves")
        self.caminho = caminho_pasta + "/" + nome + "/"
        self.image = pygame.image.load(caminho_pasta + "/" + nome + "/" + nome + ".png").convert_alpha()
        self.offsetx = offsetx
        self.offsety = offsety
        self.dialogo_interação = self.conteudo["interacao"]
        self.posição = self.conteudo["posicao"]
        self.primeira_interacao = self.conteudo["primeira_interacao"]

    def update(self, janela, canto_mapa):
        janela.blit(self.image, (canto_mapa[0] + self.posição[0] * 64 + self.offsetx, canto_mapa[1] + self.posição[1] * 64 + self.offsety))

    def salvar(self):
        if self.nome == "teteca":
            conteudo = {"posicao": self.posição, 
                        "interacao": self.dialogo_interação, 
                        "posicao_fala": self.conteudo["posicao_fala"],
                        "primeira_interacao": self.conteudo["primeira_interacao"], 
                        "dentro_do_quarto": self.conteudo["dentro_do_quarto"]}
        else:
            conteudo = {"posicao": self.posição,
                            "interacao": self.dialogo_interação,
                        "posicao_fala": self.conteudo["posicao_fala"],
                        "primeira_interacao": self.primeira_interacao
                        }
        salvar(conteudo, self.caminho + "saves")