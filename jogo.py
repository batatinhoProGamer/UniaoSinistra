import pygame, pygame.mixer
from pygame.locals import *
from sys import exit
from classes import *
from config import *
from menu import *
from funções import *
from random import randint

def inicio(janela, largura_tela, altura_tela, relogio, fps):
    falas = ["Ás vezes eu sinto como se essa não fosse eu.", "Como se eu tivesse vivido outra vida antes dessa.", "Isso me dá um desconforto, mesmo sem saber o motivo.", "Eu gostaria de perguntar para ele o porque de eu me sentir assim."]
    for fala in falas:
        relogio.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        conversa(janela, largura_tela, altura_tela, fps, relogio, fala, "Eery")
        
        pygame.display.update()

    
    voltar = False
    num = 0
    branco = pygame.image.load("sprites/resto/branco.png").convert_alpha()
    branco = pygame.transform.scale(branco, (largura_tela, altura_tela))
    branco.set_alpha(0)
    efeito_inicial = pygame.mixer.Sound("audios/efeitos/efeito_inicio.wav")
    efeito_inicial.set_volume(carregar("volume"))
    efeito_inicial.play()
    while True:
        relogio.tick(fps)
        janela.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
        if not voltar:
            num += 1.5
            if num == 255:
                voltar = True
        else:
            num -= 3
            if num == 0:
                break
        
        branco.set_alpha(num)
        janela.blit(branco, (0, 0))

        pygame.display.update()
    janela.fill((0, 0, 0))
    janela.blit(pygame.image.load("sprites/resto/intro.png").convert_alpha(), ((largura_tela - 1000) // 2, (altura_tela - 332) // 2))
    takes = 0

    while takes < 300:
        relogio.tick(fps)
        takes += 1
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
        pygame.display.update()

    numero = 0
    quadrado = pygame.image.load("sprites/resto/nada.png").convert_alpha()
    quadrado = pygame.transform.scale(quadrado, (largura_tela, altura_tela))
    quadrado.set_alpha(0)
    while numero < 255:
        relogio.tick(fps)
        numero += 1
        quadrado.set_alpha(numero)
        janela.blit(quadrado, (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
        pygame.display.update()
    quadrado.set_alpha(0)
    save = carregar()

    # personagens
    eery = Eery("inicio")

    batatinho = Batatinho(save["mapa"])

    # mapa
    imagem_mapa = pygame.image.load("sprites/" + save["imagem"] + ".png").convert_alpha()
    canto_mapa = [(largura_tela - imagem_mapa.get_width()) // 2, (altura_tela - imagem_mapa.get_height()) // 2]

    personagens_posição = [batatinho]

    brilhos = []
    if len(save["inicio"]["brilhos"]) > 0:
        for c in range(0, len(save["inicio"]["brilhos"])):
            textos = []
            for t in range(1, 5):
                textos.append("resto/brilho" + str(t))
            brilhos.append(Gif(textos, save["inicio"]["brilhos"][c], True, save["inicio"]["brilhos texto"][c]["caminho"], save["inicio"]["brilhos texto"][c]["descricao"], len(personagens_posição)))
            personagens_posição.append(brilhos[c])

    objetos_f = save["inicio"]["objetos_f"]
    objetos_f_pos = save["inicio"]["objetos_f_pos"]
        
    tabela_mapa = carregar("tabelas")["inicio"]

    pygame.mixer.music.load("audios/musicas/quarto_eery.mp3")
    pygame.mixer.music.set_volume(carregar("volume"))
    
    run = True
    while run:
        janela.fill((0, 0, 0))
        relogio.tick(fps)

        for event in pygame.event.get():
            if event.type == QUIT:
                eery.salvar()
                batatinho.salvar()
                salvar(save)
                pygame.quit()
                exit()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    eery.salvar()
                    batatinho.salvar()
                    salvar(save)
                    run = False   
                
                elif event.key == K_e:
                    inventario(janela, largura_tela, altura_tela, fps, relogio, eery)
                            
        if not eery.andando and not batatinho.andando:
            if pygame.key.get_pressed()[K_w]:
                eery.andar(0, tabela_mapa, personagens_posição)
            
            elif pygame.key.get_pressed()[K_d]:
                eery.andar(1, tabela_mapa, personagens_posição)
            
            elif pygame.key.get_pressed()[K_s]:
                eery.andar(2, tabela_mapa, personagens_posição)
                
            elif pygame.key.get_pressed()[K_a]:
                eery.andar(3, tabela_mapa, personagens_posição)
                
        if eery.andando:
            eery.movimento += 3
            if eery.movimento == 66:
                eery.andando = False
                eery.movimento = 0
                eery.posição = eery.chegada.copy()
                eery.animacao = 0
            eery.update(pygame.key.get_pressed()[K_w] or pygame.key.get_pressed()[K_a] or pygame.key.get_pressed()[K_s] or pygame.key.get_pressed()[K_d])

        if batatinho.andando:
            batatinho.movimento += 4
            if batatinho.movimento > 64:
                batatinho.andando = False
                batatinho.movimento = 0
                batatinho.posição = batatinho.chegada.copy()
                batatinho.animacao = 0
            batatinho.update()

        
        janela.blit(imagem_mapa, (canto_mapa[0], canto_mapa[1]))

        eery.carregar(janela, canto_mapa)
        batatinho.carregar(janela, canto_mapa)
        if eery.posição[1] > batatinho.posição[1]:
            eery.carregar(janela, canto_mapa)
            

        if len(brilhos) > 0:
            for c in range(0, len(brilhos)):
                brilhos[c].update(janela, canto_mapa)
        
        if batatinho.posição[1] > 2:
            batatinho.andar(0)
            if batatinho.posição[1] == 8:
                eery.mudar_olhar(3)
        
        elif batatinho.posição[0] < 7:
            batatinho.andar(1)
            
        elif batatinho.numero_de_fala == 0:
            while True:
                if len(eery.dialogos) != eery.numero_de_fala:
                    for c in range(0, len(eery.dialogos[eery.numero_de_fala])):
                        conversa(janela, largura_tela, altura_tela, fps, relogio, eery.dialogos[eery.numero_de_fala][c], "Eery")
                    eery.numero_de_fala += 1      

                if len(batatinho.dialogos) != batatinho.numero_de_fala:
                    for c in range(0, len(batatinho.dialogos[batatinho.numero_de_fala])):
                        conversa(janela, largura_tela, altura_tela, fps, relogio, batatinho.dialogos[batatinho.numero_de_fala][c], "batatinho")
                    batatinho.numero_de_fala += 1              

                elif len(batatinho.dialogos) == batatinho.numero_de_fala:
                    break
            
            
        elif batatinho.posição != [7, 1]:
            batatinho.andar(0)
            pygame.mixer.music.play(-1)
        
        elif batatinho.movimento == 0:
            batatinho.mudar_olhar(3)
            batatinho.colocar_portal()
        
        if batatinho.portal_pos != []:
            janela.blit(batatinho.portal, (canto_mapa[0] + batatinho.portal_pos[0] * 64 - 16,canto_mapa[1] + batatinho.portal_pos[1] * 64))
            batatinho.carregar(janela, canto_mapa)
            eery.carregar(janela, canto_mapa)

            if eery.movimento == 0 and eery.posição == batatinho.portal_pos:
                contagem = 0
                quadrado.set_alpha(0)
                som_portal = pygame.mixer.Sound("audios/efeitos/portal.wav")
                som_portal.set_volume(carregar("volume"))
                som_portal.play()
                while True:
                    relogio.tick(fps)
                    contagem += 1
                    if contagem == 255:
                        eery.posição = [42, 9]
                        eery.mudar_olhar(1)
                        eery.salvar()
                        batatinho.posição = [44, 9]
                        batatinho.mudar_olhar(3)
                        batatinho.salvar()
                        save["mapa"] = "orfanato"
                        pygame.mixer.music.fadeout(1000)
                        salvar(save)
                        run = False
                        break
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            eery.posição = [42, 9]
                            eery.mudar_olhar(1)
                            eery.salvar()
                            batatinho.posição = [44, 9]
                            batatinho.mudar_olhar(3)
                            batatinho.salvar()
                            save["mapa"] = "orfanato"
                            salvar(save)
                            pygame.quit()
                            exit()
                    quadrado.set_alpha(contagem)
                    janela.blit(quadrado, (0, 0))
                    
                    pygame.display.update()
            
            if pygame.key.get_pressed()[K_f]:

                if len(brilhos) > 0:
                    for c in range(0, len(brilhos)):
                        if brilhos[c].posição == eery.olhar:
                            conversa(janela, largura_tela, altura_tela, fps, relogio, brilhos[c].descrição, "")
                            for num, item in enumerate(eery.inventario):
                                if item == "":
                                    eery.inventario[num] = brilhos[c].caminho
                                    break
                            del personagens_posição[brilhos[c].tabela_pos]
                            del brilhos[c]
                            break

                for num, posicoes in enumerate(objetos_f_pos):
                    for posicao in posicoes:
                        if eery.olhar == posicao:
                            conversa(janela, largura_tela, altura_tela, fps, relogio, objetos_f[num], "")

                for c in range(0, len(personagens_posição)):
                    if personagens_posição[c].posição == eery.olhar:
                        conversa(janela, largura_tela, altura_tela, fps, relogio, personagens_posição[c].dialogo_interação, personagens_posição[c].nome)

        pygame.display.update()


def orfanato(janela, largura_tela, altura_tela, relogio, fps):
    eery = Eery("orfanato")

    porta_som_abrir = pygame.mixer.Sound("audios/efeitos/porta_abrir.wav")
    porta_som_abrir.set_volume(carregar("volume"))

    batatinho = Batatinho("orfanato", offsety=-128, offsetx=-24)
    personagens = []
    personagens.append(Personagem("sprites/orfanato/personagens", "gowon", -12, -116))
    personagens.append(Personagem("sprites/orfanato/personagens", "nicas", -8, -116))
    personagens.append(Personagem("sprites/orfanato/personagens", "peppy", -12, -128))
    personagens.append(Personagem("sprites/orfanato/personagens", "ric", -6, -114))
    if not carregar("sprites/orfanato/personagens/teteca/saves")["dentro_do_quarto"]:
        personagens.append(Personagem("sprites/orfanato/personagens", "teteca", -6, -114))

    save = carregar()
    objetos_f = save["orfanato"]["objetos_f"]
    objetos_f_pos = save["orfanato"]["objetos_f_pos"]
    contagem = 0

    tabela_mapa = carregar("tabelas")["orfanato"]
    mapa = Mapa(True, imagens=["sprites/orfanato/fundos/mapa_fundo.png", "sprites/orfanato/fundos/mapa_frente.png"], posicao=[0, 0])
    mapa.posicao = [eery.posição[0] * (-64) - 32 + largura_tela // 2, (eery.posição[1] - 1) * (-64) + altura_tela // 2]
    mapa_movimento = 0

    fonte = Gif(["orfanato/fundos/fonte_0", "orfanato/fundos/fonte_1",
                "orfanato/fundos/fonte_2", "orfanato/fundos/fonte_3",
                "orfanato/fundos/fonte_4", "orfanato/fundos/fonte_5"], [30, 25], offsetx=-16, offsety=-112)
    personagens.append(fonte)

    textos = []
    for t in range(1, 5):
        textos.append("resto/brilho" + str(t))

    brilhos = []
    for num, brilho in enumerate(save["orfanato"]["brilhos"]):
        brilhos.append(Gif(textos, brilho, True, save["orfanato"]["brilhos texto"][num]["caminho"], save["orfanato"]["brilhos texto"][num]["descricao"], offsety=-128))
    

    pygame.mixer.music.load("audios/musicas/harumachi_clover.mp3")
    pygame.mixer.music.set_volume(carregar("volume"))
    quadrado = pygame.image.load("sprites/resto/nada.png").convert_alpha()
    quadrado = pygame.transform.scale(quadrado, (largura_tela, altura_tela))
    run = True
    while run:
        janela.fill((0, 0, 0))
        relogio.tick(fps)

        for event in pygame.event.get():
            if event.type == QUIT:
                eery.salvar()
                batatinho.salvar()
                salvar(save)
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    eery.salvar()
                    batatinho.salvar()
                    salvar(save)
                    run = False   

        mapa.atualizar(janela, 0)
        for personagem in personagens:
            if eery.posição[1] >= personagem.posição[1]:
                personagem.update(janela, mapa.posicao)

        if eery.posição[1] >= batatinho.posição[1]:
            batatinho.carregar(janela, mapa.posicao)
            eery.carregar(janela, largura=largura_tela, altura=altura_tela)
        else:
            eery.carregar(janela, largura=largura_tela, altura=altura_tela)
            batatinho.carregar(janela, mapa.posicao)

        for personagem in personagens:
            if eery.posição[1] < personagem.posição[1]:
                personagem.update(janela, mapa.posicao)
            
        mapa.atualizar(janela, 1)

        if carregar("sprites/orfanato/personagens/teteca/saves")["posicao_fala"] == "segunda":
            for num, brilho in enumerate(brilhos):
                if not save["orfanato"]["brilhos texto"][num]["pego"]:
                    brilho.contador += 0.075
                    if brilho.contador // 1 >= len(brilho.imagens):
                        brilho.contador = 0
                
                    brilho.image = brilho.imagens[int(brilho.contador)]
                    
                    brilho.update(janela, mapa.posicao)


        if contagem < 255:
            contagem += 1
            quadrado.set_alpha(255 - contagem)
            janela.blit(quadrado, (0, 0))
            if contagem == 255 and eery.posição == [42, 9]:
                conversa(janela, largura_tela, altura_tela, fps, relogio, "Chegamos.", "Batatinho")
                conversa(janela, largura_tela, altura_tela, fps, relogio, "Para que possamos descobrir o paradeiro do Ruan, precisamos investigar desde o início do servidor, ou seja, no Orfanato.", "Batatinho")
                conversa(janela, largura_tela, altura_tela, fps, relogio, "Como aqui só havia jogadores de Osu!, é provável que tenha algumas gírias sobre o jogo.", "Batatinho")
                conversa(janela, largura_tela, altura_tela, fps, relogio, "Para não prolongar demais vou te ensinar o básico.", "Batatinho")
                conversa(janela, largura_tela, altura_tela, fps, relogio, "Aqui, eles possuem um sistema de pontuação denominado de 'PP', que também é fundamental para dizer qual seu ranking.", "Batatinho")
                conversa(janela, largura_tela, altura_tela, fps, relogio, "Muitos deles só jogam por conta disso e ficam viciados em acumular o máximo possível.", "Batatinho")
                conversa(janela, largura_tela, altura_tela, fps, relogio, "Logo, pode acontecer que eles utilizem isso como sistema de troca entre eles.", "Batatinho")
                conversa(janela, largura_tela, altura_tela, fps, relogio, "Aqueles que não possuem esse vício, apenas curtem o jogo, como o Nicas. É provável que você encontre ele por aqui.", "Batatinho")
                conversa(janela, largura_tela, altura_tela, fps, relogio, "Entendi. Mas como que vou achar pistas sobre onde o Ruan pode estar?", "Eery")
                conversa(janela, largura_tela, altura_tela, fps, relogio, "Existe algumas casas por aqui, cada ADM do Orfanato tinha uma. Dê uma olhada na casa dele, talvez você encontre algo.", "Batatinho")
                conversa(janela, largura_tela, altura_tela, fps, relogio, "Aliás, eu também era ADM nesse servidor, então passe na minha casa para ver se há algo útil. Se ela não estiver aberta, me procure aqui.", "Batatinho")
                conversa(janela, largura_tela, altura_tela, fps, relogio, "Assim que achar algo do paradeiro do Ruan, volte aqui para darmos uma olhada juntos.", "Batatinho")
                conversa(janela, largura_tela, altura_tela, fps, relogio, "Okay então, estou indo.", "Eery")
                pygame.mixer.music.play(-1)
            elif contagem == 255:
                pygame.mixer.music.play(-1)
        else:
            personagens.append(batatinho)
            if not eery.andando and not batatinho.andando:
                if pygame.key.get_pressed()[K_w]:
                    eery.andar(0, tabela_mapa, personagens)
                
                elif pygame.key.get_pressed()[K_d]:
                    eery.andar(1, tabela_mapa, personagens)
                
                elif pygame.key.get_pressed()[K_s]:
                    eery.andar(2, tabela_mapa, personagens)
                    
                elif pygame.key.get_pressed()[K_a]:
                    eery.andar(3, tabela_mapa, personagens)
            del personagens[-1]
                    
            if eery.andando:
                mapa_movimento += 4
                if eery.direção == 0:
                    mapa.posicao[1] += 4
                elif eery.direção == 1:
                    mapa.posicao[0] -= 4
                elif eery.direção == 2:
                    mapa.posicao[1] -= 4
                elif eery.direção == 3:
                    mapa.posicao[0] += 4

                if mapa_movimento == 64:
                    eery.andando = False
                    eery.movimento = 0
                    mapa_movimento = 0
                    eery.posição = eery.chegada.copy()
                    eery.animacao = 0
                eery.update(pygame.key.get_pressed()[K_w] or pygame.key.get_pressed()[K_a] or pygame.key.get_pressed()[K_s] or pygame.key.get_pressed()[K_d], 0.1)

            if pygame.key.get_pressed()[K_e]:
                inventario(janela, largura_tela, altura_tela, fps, relogio, eery)
                eery.salvar()

            if pygame.key.get_pressed()[K_f]:
                if 9 <= eery.olhar[0] <= 14 and 16 <= eery.olhar[1] <= 20:
                    mensagens = ["RIC É UM DEUS!!!", "OLHA PRA CÁ LINDO.", "VOCÊ ESTÁ SOLTEIRO?", "COMO SER IGUAL A VC, ME ENSINAAAA!!!"]
                    conversa(janela, largura_tela, altura_tela, fps, relogio, mensagens[randint(0, len(mensagens) - 1)], "Multidão")

                for personagem in personagens:
                    if personagem.posição != [30, 25]:
                        if personagem.posição == eery.olhar:
                            for num, dialogos in enumerate(personagem.dialogo_interação[personagem.conteudo["posicao_fala"]]):
                                if num % 2 == 0:
                                    for fala_eery in dialogos:
                                        conversa(janela, largura_tela, altura_tela, fps, relogio, fala_eery, "Eery")
                                else:
                                    for fala_char in dialogos:
                                        conversa(janela, largura_tela, altura_tela, fps, relogio, fala_char, personagem.nome)
                            if personagem.conteudo["posicao_fala"] == "primeira":
                                personagem.conteudo["posicao_fala"] = "segunda"
                                personagem.salvar()

                            elif personagem.conteudo["posicao_fala"] == "segunda":
                                if personagem.nome == "gowon":
                                    if "sprites/itens/papel_queimado.png" in eery.inventario:
                                        eery.inventario = list(map(lambda x: x.replace('sprites/itens/papel_queimado.png', ''), eery.inventario))
                                        personagem.conteudo["posicao_fala"] = "terceira"
                                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Sim, achei esse papel aqui com suas informações e logo queimei para ninguém pegar mais.", "Eery")
                                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Obrigado. Você foi de grande ajuda.", "gowon")
                                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Agora vou poder ir para o multi do nicas tranquilo.", "gowon")
                                        personagem.posição = [30, 21]
                                        personagem.salvar()
                                        contagem = 0
                                        quadrado = pygame.image.load("sprites/resto/nada.png").convert_alpha()
                                        quadrado = pygame.transform.scale(quadrado, (largura_tela, altura_tela))
                                        quadrado.set_alpha(0)
                                        voltar = False
                                        while True:
                                            relogio.tick(fps)
                                            if not voltar:
                                                contagem += 3
                                                if contagem == 255:
                                                    voltar = True
                                            else:
                                                contagem -= 3
                                                if contagem == 0:
                                                    break
                                            
                                            quadrado.set_alpha(contagem)
                                            janela.blit(quadrado, (0, 0))

                                            pygame.display.update()
                                            
                                        eery.salvar()
                                    else:
                                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Conseguiu fazer aquilo?", "gowon")
                                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Ainda não.", "Eery")

                                elif personagem.nome == "nicas":
                                    if len(personagens) == 6 and personagens[0].posição != [7, 40] and personagens[3].posição != [11, 14] and personagens[4].posição == [28, 22]:
                                        personagem.conteudo["posicao_fala"] = "terceira"
                                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Muito obrigado! Leve isto como agradecimento por reunir eles aqui.", "nicas")
                                        for num, item in enumerate(eery.inventario):
                                            if item == "":
                                                eery.inventario[num] = "sprites/itens/pp.png"
                                                break
                                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Nicas lhe entrega PP.", "")
                                        personagem.salvar()
                                        eery.salvar()
                                    else:
                                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Conseguiu reunir todos aqui?", "nicas")
                                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Ainda não.", "Eery")
                                
                                elif personagem.nome == "peppy":
                                    if "sprites/itens/pp.png" in eery.inventario:
                                        eery.inventario = list(map(lambda x: x.replace('sprites/itens/pp.png', ''), eery.inventario))
                                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Conseguiu pegar o PP?", "peppy")
                                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Sim, aqui está", "Eery")
                                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Certo.", "peppy")
                                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Aqui está a chave, faça bom proveito dela e volte sempre.", "peppy")
                                        personagem.conteudo["posicao_fala"] = "terceira"
                                        for num, item in enumerate(eery.inventario):
                                            if item == "":
                                                eery.inventario[num] = "sprites/itens/chave_ruan.png"
                                                break
                                        personagem.salvar()
                                        eery.salvar()
                                    
                                    else:
                                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Conseguiu pegar o PP?", "peppy")
                                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Ainda não.", "Eery")
                                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Certo, estarei esperando aqui.", "peppy")
                                
                                elif personagem.nome == "ric":
                                    if personagens[1].conteudo["posicao_fala"] == "segunda":
                                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Bom... O nicas estava querendo ir multi com você lá na praça pública.", "Eery")
                                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Sério?", "ric")
                                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Sim. Ele me pediu para chamar algumas pessoas caso eu encontre elas, e você era uma delas.", "Eery")
                                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Ótimo! Terei uma desculpa para sair daqui também...", "ric")
                                        conversa(janela, largura_tela, altura_tela, fps, relogio, "PESSOAL VOLTEM PARA SUAS CASAS! EU ESTAREI OCUPADO AGORA.", "ric")
                                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Muito obrigado!", "ric")
                                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Denada! Aproveite o multi", "Eery")
                                        num = 0
                                        voltar = False
                                        while True:
                                            relogio.tick(fps)
                                            quadrado.set_alpha(num)
                                            if not voltar:
                                                num += 3

                                            else:
                                                num -= 3
                                                if num == 0:
                                                    break
                                            if num == 255:
                                                voltar = True
                                            janela.blit(quadrado, (0, 0))
                                            pygame.display.update()

                                        personagem.posição = [33, 22]
                                        personagem.conteudo["posicao_fala"] = "terceira"
                                
                                personagem.salvar()
                
                try:
                    if brilhos[0].posição == eery.olhar:
                        if not save["orfanato"]["brilhos texto"][0]["pego"]:
                            conversa(janela, largura_tela, altura_tela, fps, relogio, brilhos[0].descrição, "")
                            for num, item in enumerate(eery.inventario):
                                if item == "":
                                    eery.inventario[num] = brilhos[0].caminho
                                    break
                            del brilhos[0]
                            save["orfanato"]["brilhos texto"][0]["pego"] = True
                            salvar(save)
                            eery.salvar()
                            break
                except:
                    pass
                
                if eery.olhar == batatinho.posição:
                    conversa(janela, largura_tela, altura_tela, fps, relogio, "Encontrou algo que nos ajude a encontrar o ruan?", "batatinho")
                    if "sprites/itens/livro.png" in eery.inventario:
                        eery.inventario = list(map(lambda x: x.replace('sprites/itens/caderno.png', ''), eery.inventario))
                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Consegui. Eu achei esse caderno dele.", "Eery")
                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Boa! Vou dar uma olhada nele para ver o que está escrito.", "batatinho")
                        conversa(janela, largura_tela, altura_tela, fps, relogio, "...", "")
                        conversa(janela, largura_tela, altura_tela, fps, relogio, "...", "")
                        conversa(janela, largura_tela, altura_tela, fps, relogio, "...", "")
                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Eai? Achou algo de interessante?", "Eery")
                        conversa(janela, largura_tela, altura_tela, fps, relogio, "A maioria das coisas que tem aqui são só algumas anotações inúteis.", "batatinho")
                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Mas eu consegui achar algo que vai nos ajudar a encontrar ele.", "batatinho")
                        conversa(janela, largura_tela, altura_tela, fps, relogio, "E o que é?", "Eery")
                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Bem, segundo o que está escrito aqui, parece que ele foi até a época da União Sinistra 1.", "batatinho")
                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Não diz nada sobre o motivo de tudo isso, mas acredito que se acharmos ele, podemos entender melhor.", "batatinho")
                        conversa(janela, largura_tela, altura_tela, fps, relogio, "E caso esteja planejando algo ruim, podemos impedir também.", "batatinho")
                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Nossa! Que ótimo!", "Eery")
                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Então iremos agora para a União sinistra 1?", "Eery")
                        conversa(janela, largura_tela, altura_tela, fps, relogio, "É o jeito... se prepare novamente, pois teremos outra viagem.", "batatinho")
                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Irei colocar o portal aqui para irmos.", "batatinho")
                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Ok.", "Eery")
                        
                        batatinho.olhar = [batatinho.posição[0] - 1, batatinho.posição[1]]
                        if not batatinho.olhar == eery.posição:
                            batatinho.colocar_portal()
                            batatinho.mudar_olhar(2)
                        else:
                            batatinho.mudar_olhar(1)
                            batatinho.colocar_portal()
                    else:
                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Ainda não.", "Eery")

                for num, posicoes in enumerate(objetos_f_pos):
                    for posicao in posicoes:
                        if eery.olhar == posicao:
                            conversa(janela, largura_tela, altura_tela, fps, relogio, objetos_f[num], "")

                if eery.olhar in [[24, 43], [25, 43]]:
                    conversa(janela, largura_tela, altura_tela, fps, relogio, "Lar de Batatinho", "")
                    if len(personagens) == 5 and not carregar("sprites/orfanato/personagens/teteca/saves")["dentro_do_quarto"]:
                        personagens.append(Personagem("sprites/orfanato/personagens", "teteca", -6, -114))
                elif eery.olhar == [29, 43]:
                    conversa(janela, largura_tela, altura_tela, fps, relogio, "Lar de Gowon", "")
                elif eery.olhar == [33, 43]:
                    conversa(janela, largura_tela, altura_tela, fps, relogio, "Lar de Nicas", "")
                elif eery.olhar in [[37, 43], [38, 43]]:
                    conversa(janela, largura_tela, altura_tela, fps, relogio, "Lar de Ruan", "")
                elif eery.olhar in [[42, 43], [43, 43]]:
                    conversa(janela, largura_tela, altura_tela, fps, relogio, "Lar de Catjam", "")
                elif eery.olhar in [[47, 43], [48, 43]]:
                    conversa(janela, largura_tela, altura_tela, fps, relogio, "A placa está em pedaços, está quase ilegível.", "Eery")

                elif eery.olhar == [22, 42]:
                    porta_som_abrir.play()
                    quarto_orfanato(janela, largura_tela, altura_tela, relogio, fps, "batatinho", eery, save)
                elif eery.olhar == [27, 42]:
                    porta_som_abrir.play()
                    quarto_orfanato(janela, largura_tela, altura_tela, relogio, fps, "gowon", eery, save)
                elif eery.olhar == [35, 42]:
                    porta_som_abrir.play()
                    quarto_orfanato(janela, largura_tela, altura_tela, relogio, fps, "nicas", eery, save)
                elif eery.olhar == [40, 42]:
                    if "sprites/itens/chave_ruan.png" in eery.inventario:
                        porta_som_abrir.play()
                        quarto_orfanato(janela, largura_tela, altura_tela, relogio, fps, "ruan", eery, save)
                    else:
                        conversa(janela, largura_tela, altura_tela, fps, relogio, "Está trancada.", "")
                elif eery.olhar == [45, 42]:
                    conversa(janela, largura_tela, altura_tela, fps, relogio, "Está trancada.", "")
                
        if eery.movimento == 0 and eery.posição == batatinho.portal_pos:
            contagem = 0
            som_portal = pygame.mixer.Sound("audios/efeitos/portal.wav")
            som_portal.set_volume(carregar("volume"))
            som_portal.play()
            quadrado = pygame.image.load("sprites/resto/nada.png").convert_alpha()
            quadrado = pygame.transform.scale(quadrado, (largura_tela, altura_tela))
            quadrado.set_alpha(0)
            run = False
            while True:
                relogio.tick(fps)
                contagem += 1
                if contagem == 255:
                    eery.posição = [42, 9]
                    eery.mudar_olhar(1)
                    eery.salvar()
                    batatinho.posição = [44, 9]
                    batatinho.mudar_olhar(3)
                    batatinho.salvar()
                    save["mapa"] = "uniao1"
                    salvar(save)
                    run = False
                    break
                for event in pygame.event.get():
                    if event.type == QUIT:
                        eery.posição = [42, 9]
                        eery.mudar_olhar(1)
                        eery.salvar()
                        batatinho.posição = [44, 9]
                        batatinho.mudar_olhar(3)
                        batatinho.salvar()
                        save["mapa"] = "uniao1"
                        salvar(save)
                        pygame.quit()
                        exit()
                quadrado.set_alpha(contagem)
                janela.blit(quadrado, (0, 0))
                
                pygame.display.update()
        pygame.display.update()


def quarto_orfanato(janela, largura_tela, altura_tela, relogio, fps, quarto, eery, save):
    eery.posição = [7, 9]
    eery.olhar = [7, 8]
    tabela_quarto = carregar("tabelas")["orfanato_quarto"]
    imagem_quarto = pygame.image.load("sprites/orfanato/fundos/quarto.png").convert_alpha()
    canto_quarto = [(largura_tela - imagem_quarto.get_width()) // 2 - 20,(altura_tela - imagem_quarto.get_height()) // 2 - 20]

    personagens_posição = []
    if quarto == "batatinho" and carregar("sprites/orfanato/personagens/teteca/saves")["dentro_do_quarto"]:
        #teteca = Personagem("sprites/orfanato/personagens", "teteca", -6, -114)
        teteca = Personagem("sprites/orfanato/personagens", "teteca", 12, 12)
        personagens_posição.append(teteca)

    brilhos = []
    for c in range(0, len(save["orfanato"]["quartos"][quarto]["brilhos"])):
        textos = []
        for t in range(1, 5):
            textos.append("resto/brilho" + str(t))
        brilhos.append(Gif(textos, save["orfanato"]["quartos"][quarto]["brilhos"][c], True, save["orfanato"]["quartos"][quarto]["brilhos texto"][c]["caminho"], save["orfanato"]["quartos"][quarto]["brilhos texto"][c]["descricao"], len(personagens_posição), 8, -8))

    objetos_f = save["orfanato"]["quartos"][quarto]["objetos_f"]
    objetos_f_pos = save["orfanato"]["quartos"][quarto]["objetos_f_pos"]

    som_porta_fechar = pygame.mixer.Sound("audios/efeitos/porta_fechar.wav")
    som_porta_fechar.set_volume(carregar("volume"))
    run = True
    while run:
        janela.fill((0, 0, 0))
        relogio.tick(fps)


        for event in pygame.event.get():
            if event.type == QUIT:
                if quarto == "batatinho":
                    eery.posição = [22, 43]
                    eery.olhar = [22, 44]
                elif quarto == "gowon":
                    eery.posição = [27, 43]
                    eery.olhar = [27, 44]
                elif quarto == "nicas":
                    eery.posição = [35, 43]
                    eery.olhar = [35, 44]
                elif quarto == "ruan":
                    eery.posição = [40, 43]
                    eery.olhar = [40, 44]
                eery.salvar()
                salvar(save)
                pygame.quit()
                exit()

        janela.blit(imagem_quarto, (canto_quarto[0] + 4, canto_quarto[1]))

        try:
            janela.blit(teteca.image, (canto_quarto[0] + teteca.posição[0] * 32 + teteca.offsetx, canto_quarto[1] + teteca.posição[1] * 32 + teteca.offsety))
        except:
            pass

        if eery.direção == 0:
            janela.blit(eery.image, (canto_quarto[0] + eery.posição[0] * 32 + 4, canto_quarto[1] + eery.posição[1] * 32 - eery.movimento))
        elif eery.direção == 1:
            janela.blit(eery.image, (canto_quarto[0] + eery.posição[0] * 32 + 4 + eery.movimento, canto_quarto[1] + eery.posição[1] * 32))
        elif eery.direção == 2:
            janela.blit(eery.image, (canto_quarto[0] + eery.posição[0] * 32 + 4, canto_quarto[1] + eery.posição[1] * 32 + eery.movimento))
        else:
            janela.blit(eery.image, (canto_quarto[0] + eery.posição[0] * 32 + 4 - eery.movimento, canto_quarto[1] + eery.posição[1] * 32))

        if not eery.andando:
            if pygame.key.get_pressed()[K_w]:
                eery.andar(0, tabela_quarto, personagens_posição)
            
            elif pygame.key.get_pressed()[K_d]:
                eery.andar(1, tabela_quarto, personagens_posição)
            
            elif pygame.key.get_pressed()[K_s]:
                eery.andar(2, tabela_quarto, personagens_posição)
                
            elif pygame.key.get_pressed()[K_a]:
                eery.andar(3, tabela_quarto, personagens_posição)
                
        if eery.andando:
            eery.movimento += 2
            if eery.movimento >= 33:
                eery.andando = False
                eery.movimento = 0
                eery.posição = eery.chegada.copy()
                eery.animacao = 0
            eery.update(pygame.key.get_pressed()[K_w] or pygame.key.get_pressed()[K_a] or pygame.key.get_pressed()[K_s] or pygame.key.get_pressed()[K_d], 0.1)

        for num, brilho in enumerate(brilhos):
            if not save["orfanato"]["quartos"][quarto]["brilhos texto"][num]["pego"]:
                brilho.contador += 0.075
                if brilho.contador // 1 >= len(brilho.imagens):
                    brilho.contador = 0
            
                brilho.image = brilho.imagens[int(brilho.contador)]
                
                janela.blit(brilho.image, (canto_quarto[0] + brilho.posição[0] * 32 + brilho.offsetx, canto_quarto[1] + brilho.posição[1] * 32 + brilho.offsety))

        if quarto == "ruan" and len(brilhos) == 1:
            if not save["orfanato"]["quartos"][quarto]["brilhos texto"][0]["pego"] or save["orfanato"]["quartos"][quarto]["brilhos texto"][1]["pego"]:
                brilhos[0].contador += 0.075
                if brilhos[0].contador // 1 >= len(brilhos[0].imagens):
                    brilhos[0].contador = 0
        
                brilhos[0].image = brilhos[0].imagens[int(brilhos[0].contador)]
                
                janela.blit(brilhos[0].image, (canto_quarto[0] + brilhos[0].posição[0] * 32 + brilhos[0].offsetx, canto_quarto[1] + brilhos[0].posição[1] * 32 + brilhos[0].offsety))

        if pygame.key.get_pressed()[K_e]:
            inventario(janela, largura_tela, altura_tela, fps, relogio, eery)
            eery.salvar()

        if pygame.key.get_pressed()[K_f]:

            if len(brilhos) > 0:
                for c in range(0, len(brilhos)):
                    if brilhos[c].posição == eery.olhar:
                        if save["orfanato"]["quartos"][quarto]["brilhos texto"][c]["pego"] == False:
                            conversa(janela, largura_tela, altura_tela, fps, relogio, brilhos[c].descrição, "")
                            for num, item in enumerate(eery.inventario):
                                if item == "":
                                    eery.inventario[num] = brilhos[c].caminho
                                    break
                            del brilhos[c]
                            save["orfanato"]["quartos"][quarto]["brilhos texto"][c]["pego"] = True
                            salvar(save)
                            eery.salvar()
                            break

            for num, posicoes in enumerate(objetos_f_pos):
                for posicao in posicoes:
                    if eery.olhar == posicao:
                        conversa(janela, largura_tela, altura_tela, fps, relogio, objetos_f[num], "")

            for c in range(0, len(personagens_posição)):
                if personagens_posição[c].posição == eery.olhar:
                    for num, conversando in enumerate(personagens_posição[c].dialogo_interação[personagens_posição[c].conteudo["posicao_fala"]]):
                        for fala in conversando:
                            if num % 2 == 1:
                                conversa(janela, largura_tela, altura_tela, fps, relogio, fala, personagens_posição[c].nome)
                            else:
                                conversa(janela, largura_tela, altura_tela, fps, relogio, fala, "Eery")
                    if personagens_posição[c].conteudo["posicao_fala"] == "primeira":
                        personagens_posição[c].conteudo["posicao_fala"] = "segunda"
                        personagens_posição[c].salvar()
                    elif personagens_posição[c].conteudo["posicao_fala"] == "segunda":
                        if "sprites/itens/remedio_teteca.png" in eery.inventario:
                            conversa(janela, largura_tela, altura_tela, fps, relogio, "Sim! Aqui está Teteca. Espero que você melhore nessa sua situação.", "Eery")
                            conversa(janela, largura_tela, altura_tela, fps, relogio, "Muito obrigado Eery! Agora vou conseguir participar de cabeça erguida no muiltizinho do Nicas!", "Teteca")
                            personagens_posição[c].posição = [28, 22]
                            personagens_posição[c].conteudo["posicao_fala"] = "terceira"
                            personagens_posição[c].conteudo["dentro_do_quarto"] = False
                            personagens_posição[c].salvar()
                            eery.inventario = list(map(lambda x: x.replace('sprites/itens/remedio_teteca.png', ''), eery.inventario))
                            contagem = 0
                            quadrado = pygame.image.load("sprites/resto/nada.png").convert_alpha()
                            quadrado = pygame.transform.scale(quadrado, (largura_tela, altura_tela))
                            quadrado.set_alpha(0)
                            voltar = False
                            while True:
                                relogio.tick(fps)
                                if not voltar:
                                    contagem += 3
                                    if contagem == 255:
                                        voltar = True
                                else:
                                    contagem -= 3
                                    if contagem == 0:
                                        break
                                
                                quadrado.set_alpha(contagem)
                                janela.blit(quadrado, (0, 0))

                                pygame.display.update()
                                
                            del personagens_posição[c]
                            eery.salvar()
                        else:
                            conversa(janela, largura_tela, altura_tela, fps, relogio, "Ainda não... Ainda estou procurando.", "Eery")
                            conversa(janela, largura_tela, altura_tela, fps, relogio, "Ok! Estarei aqui esperando.", "Teteca")

        if eery.posição == [7, 10]:
            if quarto == "batatinho":
                eery.posição = [22, 43]
                eery.olhar = [22, 44]
                som_porta_fechar.play()
            elif quarto == "gowon":
                eery.posição = [27, 43]
                som_porta_fechar.play()
                eery.olhar = [27, 44]
            elif quarto == "nicas":
                som_porta_fechar.play()
                eery.posição = [35, 43]
                eery.olhar = [35, 44]
            elif quarto == "ruan":
                eery.posição = [40, 43]
                som_porta_fechar.play()
                eery.olhar = [40, 44]
            run = False
        
        pygame.display.update()
