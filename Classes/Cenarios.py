import os
import random
from PIL import Image
from os import listdir, path
from os.path import isfile, join
from pathlib import Path
import pygame.mixer

from PPlay import sprite
from PPlay.gameimage import *
from Classes.Itens import *
from PPlay.sound import *
from Classes.Colisoes import *
from Classes.Personagens import *
from math import sqrt


class Cenario0:
    def __init__(self):
        self.fundo = GameImage("Imagens/" + InformacoesBase.resolucao + "Cenario-0.png")
        self.som_cenario = "Sons/Musica_0.mp3"
        self.volume_som_cenario = 0.3
        self.som_passos = "Sons/piso_marmore.wav"
        self.volume_passos = 0.3
        F_R = InformacoesBase.fator_redimensionamento
        self.F_R = F_R
        # Configuração das colisões
        self.area_colisoes = [[0 / F_R, 780 / F_R, 339 / F_R, 1080 / F_R], [463 / F_R, 862 / F_R, 829 / F_R, 1080 / F_R]
            , [1141 / F_R, 362 / F_R, 1466 / F_R, 567 / F_R], [829 / F_R, 781 / F_R, 1182 / F_R, 1080 / F_R],
                              [1182 / F_R, 919 / F_R, 1288 / F_R, 1004 / F_R],
                              [1203 / F_R, 571 / F_R, 1403 / F_R, 635 / F_R],
                              [1559 / F_R, 579 / F_R, 1678 / F_R, 661 / F_R],
                              [1563 / F_R, 710 / F_R, 1920 / F_R, 803 / F_R],
                              [1687 / F_R, 300 / F_R, 1920 / F_R, 597 / F_R],
                              [654 / F_R, 459 / F_R, 761 / F_R, 490 / F_R]]

        self.limite = 213.45 / F_R

        # Configuração dos inimigos
        self.inimigos = []
        self.area_inimigos = []
        self.area_chefao = []
        self.ordas_inimigos = 0
        self.numero_inimigos = 0
        self.chefao_criado = False
        self.cria_inimigos()

        # Configuração dos itens
        arma = Pistola()
        item_vida = ItemVida()
        item_vida2 = ItemVida()
        item_vida.imagem.x = 395 / self.F_R
        item_vida.imagem.y = 837 / self.F_R
        item_vida2.imagem.x = 658 / self.F_R
        item_vida2.imagem.y = 839 / self.F_R

        self.itens = [arma, item_vida, item_vida2]

        # Configurações dos Aliados
        esposa_e_filha = Aliados("Imagens/" + InformacoesBase.resolucao + "esposa_e_filha.png", "Esposa e Filha")
        esposa_e_filha.sprite.x = 651 / F_R
        esposa_e_filha.sprite.y = 260 / F_R
        self.aliados = [esposa_e_filha]

        # Auxilio para resetar as colisões
        self.inicializando = True

    def colisoes_cenario(self, personagem):
        atras = False
        sprite_jogador = personagem.sprite
        if sprite_jogador.y > self.limite:
            for i in range(len(self.area_colisoes)):
                if self.area_colisoes[i][1] > sprite_jogador.y + sprite_jogador.height:
                    atras = True
                colisao = colisao_retangulo(sprite_jogador, self.area_colisoes[i], atras)
                if colisao is not True:
                    personagem.colisao_antiga[i] = colisao
                elif colisao is True:
                    indice = personagem.colisao_antiga[i].index(False)
                    if indice == 0:
                        sprite_jogador.x = self.area_colisoes[i][indice] - sprite_jogador.width
                    elif indice == 1:
                        sprite_jogador.y = self.area_colisoes[i][indice] - sprite_jogador.height
                    elif indice == 2:
                        sprite_jogador.x = self.area_colisoes[i][indice]
                    else:
                        if atras:
                            sprite_jogador.y = self.area_colisoes[i][indice] - sprite_jogador.height + 20
                        else:
                            sprite_jogador.y = self.area_colisoes[i][indice]
        else:
            sprite_jogador.y = self.limite

    def proxima_fase(self, jogador, inimigos):
        sprite_jogador = jogador.sprite
        if sprite_jogador.x + sprite_jogador.width > 1668 / self.F_R \
                and 640 / self.F_R < sprite_jogador.y + sprite_jogador.height < 720 / self.F_R:
            sprite_jogador.x = 230 / self.F_R
            sprite_jogador.y = (647 / self.F_R) - sprite_jogador.height
            self.inicializando = True
            InformacoesBase.trocando_cenario = True
            return "cenario_1"
        return "cenario_0"

    def adiciona_lista_de_colisoes_anteriores(self, personagem):
        personagem.colisao_antiga = [[] for _ in range(len(self.area_colisoes))]

    def cria_chefao(self):
        if not self.chefao_criado:
            inimigo = Chefao()
            self.adiciona_lista_de_colisoes_anteriores(inimigo)
            inimigo.sprite.x = random.randint(self.area_chefao[0], self.area_chefao[2] - inimigo.sprite.width)
            inimigo.sprite.y = random.randint(self.area_chefao[1], self.area_chefao[3] - inimigo.sprite.height)
            self.inimigos.append(inimigo)

    def cria_inimigos(self):
        for i in range(self.numero_inimigos):
            inimigo = Inimigos()
            self.adiciona_lista_de_colisoes_anteriores(inimigo)
            inimigo.sprite.x = random.randint(self.area_inimigos[0], self.area_inimigos[2] - inimigo.sprite.width)
            inimigo.sprite.y = random.randint(self.area_inimigos[1], self.area_inimigos[3] - inimigo.sprite.height)
            self.inimigos.append(inimigo)


class Cenario1(Cenario0):
    def __init__(self):
        super().__init__()
        self.fundo = GameImage("Imagens/" + InformacoesBase.resolucao + "Cenario_2.png")
        self.som_cenario = "Sons/Musica_1.ogg"
        self.volume_som_cenario = 0.1
        self.som_passos = "Sons/piso_neve.ogg"
        self.volume_passos = 0.2
        F_R = self.F_R
        # Configuração de colisões
        self.area_colisoes = [[470 / F_R, 859 / F_R, 909 / F_R, 1080 / F_R],
                              [360 / F_R, 43 / F_R, 605 / F_R, 416 / F_R], [907 / F_R, 3 / F_R, 1486 / F_R, 458 / F_R],
                              [1109 / F_R, 890 / F_R, 1278 / F_R, 1069 / F_R],
                              [1542 / F_R, 155 / F_R, 1652 / F_R, 423 / F_R],
                              [1603 / F_R, 854 / F_R, 1912 / F_R, 1074 / F_R],
                              [4 / F_R, 5 / F_R, 1910 / F_R, 376 / F_R],
                              [0 / F_R, 563 / F_R, 138 / F_R, 742 / F_R]]
        self.limite = 0 / F_R

        # Configurações dos inimigos
        self.inimigos = []
        self.area_inimigos = [620 // F_R, 483 // F_R, 1527 // F_R, 850 // F_R]
        self.area_chefao = [236 // F_R, 472 // F_R, 950 // F_R, 857 // F_R]
        self.ordas_inimigos = 3
        self.numero_inimigos = 3
        # Configurações dos Aliados
        self.aliados = []

        # Configurações dos itens
        self.itens = []

    def proxima_fase(self, jogador, lista_inimigos):
        sprite_jogador = jogador.sprite
        if sprite_jogador.x + sprite_jogador.width > (1891 / self.F_R) \
                and (547 / self.F_R) < sprite_jogador.y + sprite_jogador.height < (688 / self.F_R) \
                and self.ordas_inimigos == 0 and len(lista_inimigos) == 0:
            sprite_jogador.x = 146
            sprite_jogador.y = 575 - sprite_jogador.height
            InformacoesBase.trocando_cenario = True
            return "cenario_2"
        elif sprite_jogador.x < (168 / self.F_R) and (558 / self.F_R) < sprite_jogador.y + sprite_jogador.height < \
                (739 / self.F_R) and (jogador.inventario.verifica_item("FlorMedicinal") is not False) \
                and len(lista_inimigos) == 0:
            sprite_jogador.x = 1520 / self.F_R
            sprite_jogador.y = (705 / self.F_R) - sprite_jogador.height
            InformacoesBase.trocando_cenario = True
            return "cenario_0"
        return "cenario_1"


class Cenario2(Cenario0):
    def __init__(self):
        super().__init__()
        self.fundo = GameImage("Imagens/" + InformacoesBase.resolucao + "Cenario_3.png")
        self.som_cenario = "Sons/Musica_1.ogg"
        self.volume_som_cenario = 0.1
        self.som_passos = "Sons/piso_neve.ogg"
        self.volume_passos = 0.2
        F_R = self.F_R
        # Configurações de Colisões
        self.area_colisoes = [[459 / F_R, 848 / F_R, 819 / F_R, 1076 / F_R],
                              [1001 / F_R, 806 / F_R, 1365 / F_R, 1074 / F_R],
                              [251 / F_R, 278 / F_R, 383 / F_R, 368 / F_R],
                              [503 / F_R, 281 / F_R, 632 / F_R, 371 / F_R],
                              [858 / F_R, 143 / F_R, 1113 / F_R, 414 / F_R],
                              [1485, 887, 1916, 1074], [5 / F_R, 3 / F_R, 1913 / F_R, 330 / F_R]]
        self.limite = 0 / F_R

        # Configuração dos inimigos
        self.inimigos = []
        self.area_inimigos = [845 // F_R, 421 // F_R, 1919 // F_R, 803 // F_R]
        self.ordas_inimigos = 3
        self.numero_inimigos = 4

        # Configurações dos Aliados
        self.aliados = []

        # Configuração dos itens
        flor_medicinal = FlorMedicinal()
        self.itens = [flor_medicinal]

    def proxima_fase(self, jogador, lista_inimigos):
        sprite_jogador = jogador.sprite
        if sprite_jogador.x < (30 / self.F_R) and (488 / self.F_R) < sprite_jogador.y + sprite_jogador.height < \
                (658 / self.F_R):
            possui_flor = jogador.inventario.verifica_item("FlorMedicinal")
            if (possui_flor and len(lista_inimigos) == 0 and self.ordas_inimigos == 0) or not possui_flor:
                sprite_jogador.x = 1760 / self.F_R
                sprite_jogador.y = (644 / self.F_R) - sprite_jogador.height
                InformacoesBase.trocando_cenario = True
                return "cenario_1"
        return "cenario_2"


class Menu:
    def __init__(self, imagem, menu_retorno):
        # definir o fundo
        self.fundo = GameImage(imagem)
        self.F_R = InformacoesBase.fator_redimensionamento
        self.pasta_apagar = "Imagens\\ImagensRedimensionadas\\"
        self.menu_retorno = menu_retorno
        self.opcoes_menu = None
        self.imagem_atras = False
        self.cor_rect = (125, 125, 125)
        # Sons
        self.som_selecao = pygame.mixer.Sound("Sons/selecao_menu.wav")
        self.som_escolha_feita = pygame.mixer.Sound("Sons/som_escolha_feita.wav")
        self.tocar_som1 = True
        self.tocar_som2 = True

    def tela(self, janela):
        opcao_selecionada = False
        tela = pygame.display.set_mode((janela.width, janela.height))
        pode_selecionar = False
        while not opcao_selecionada:
            desenha_1 = False
            desenha_2 = False
            mouse = Mouse()
            botao_mouse = mouse.is_button_pressed(1)
            if not botao_mouse:
                pode_selecionar = True
            janela.set_background_color("BLACK")
            pos_mouse = mouse.get_position()
            if (480 / self.F_R) < pos_mouse[0] < (960 / self.F_R) and (665 / self.F_R) < pos_mouse[1] < (
                    814 / self.F_R):
                desenha_1 = True
                if botao_mouse and pode_selecionar:
                    self.som_escolha_feita.play()
                    return self.menu_retorno
            elif (960 / self.F_R) < pos_mouse[0] < (1440 / self.F_R) and (665 / self.F_R) < pos_mouse[1] < \
                    (814 / self.F_R):
                desenha_2 = True
                if botao_mouse and pode_selecionar:
                    self.som_escolha_feita.play()
                    pasta_imagens = listdir(self.pasta_apagar)
                    for imagens in pasta_imagens:
                        os.remove(self.pasta_apagar + imagens)
                    pygame.time.wait(1500)
                    janela.close()

            if self.imagem_atras:
                self.fundo.draw()
                if desenha_1:
                    pygame.draw.rect(tela, self.cor_rect,
                                     (480 / self.F_R, 665 / self.F_R, 480 / self.F_R, 149 / self.F_R),
                                     int(5 / self.F_R))
                    if self.tocar_som1:
                        self.som_selecao.play()
                        self.tocar_som1 = False

                else:
                    self.tocar_som1 = True

                if desenha_2:
                    pygame.draw.rect(tela, self.cor_rect,
                                     (960 / self.F_R, 665 / self.F_R, 480 / self.F_R, 149 / self.F_R),
                                     int(5 / self.F_R))
                    if self.tocar_som2:
                        self.som_selecao.play()
                        self.tocar_som2 = False
                else:
                    self.tocar_som2 = True

            else:
                if desenha_1:
                    pygame.draw.rect(tela, self.cor_rect,
                                     (480 / self.F_R, 665 / self.F_R, 480 / self.F_R, 149 / self.F_R),
                                     int(5 / self.F_R))
                    if self.tocar_som1:
                        self.som_selecao.play()
                        self.tocar_som1 = False

                else:
                    self.tocar_som1 = True

                if desenha_2:
                    pygame.draw.rect(tela, self.cor_rect,
                                     (960 / self.F_R, 665 / self.F_R, 480 / self.F_R, 149 / self.F_R),
                                     int(5 / self.F_R))
                    if self.tocar_som2:
                        self.som_selecao.play()
                        self.tocar_som2 = False
                else:
                    self.tocar_som2 = True

                self.fundo.draw()

            if self.opcoes_menu is not None:
                self.opcoes_menu.draw()
            janela.update()


class MenuPrincipal(Menu):
    def __init__(self, imagem, menu_retorno):
        super().__init__(imagem, menu_retorno)
        self.opcoes_menu = GameImage("Imagens/" + InformacoesBase.resolucao + "menu_principal_letras.png")
        self.imagem_atras = True
        self.cor_rect = (79, 208, 230)


class TelaPrologo:
    def __init__(self, dir_imagem):
        # definir o fundo
        self.fundo = GameImage(dir_imagem)

    def tela(self, janela):
        sair = False
        frase_proxima_mensagem = GameImage("Imagens/" + InformacoesBase.resolucao + "proxima_mensagem.png")
        while Keyboard().key_pressed("SPACE"):
            janela.update()
        while not (Keyboard().key_pressed("SPACE") and not sair):
            janela.set_background_color("BLACK")
            self.fundo.draw()
            frase_proxima_mensagem.draw()
            janela.update()


class TelaResolucao:
    def __init__(self, ):
        self.fundo = GameImage("Imagens/" + InformacoesBase.resolucao + "Tela_de_resolucao.png")
        self.F_R = InformacoesBase.fator_redimensionamento
        self.diretorio_arquivos = "Imagens\\1080P\\"
        self.diretorio_salvar = "Imagens\\ImagensRedimensionadas\\"
        # Sons
        self.som_selecao = pygame.mixer.Sound("Sons/selecao_menu.wav")
        self.som_escolha_feita = pygame.mixer.Sound("Sons/som_escolha_feita.wav")
        self.tocar_som1 = True
        self.tocar_som2 = True
        self.tocar_som3 = True
        self.tocar_som4 = True

    def tela(self, janela):
        opcao_selecionada = False
        tela = pygame.display.set_mode((janela.width, janela.height))
        pode_selecionar = False
        while not opcao_selecionada:
            mouse = Mouse()
            botao_mouse = mouse.is_button_pressed(1)
            if not botao_mouse:
                pode_selecionar = True
            janela.set_background_color("BLACK")
            cor1 = (0, 0, 0)
            cor2 = (0, 0, 0)
            cor3 = (0, 0, 0)
            cor4 = (0, 0, 0)
            pos_mouse = mouse.get_position()
            if (480 / self.F_R) < pos_mouse[0] < (960 / self.F_R) and (515 / self.F_R) < pos_mouse[1] < \
                    (665 / self.F_R):
                cor1 = (125, 125, 125)

                if self.tocar_som1:
                    self.som_selecao.play()
                    self.tocar_som1 = False

                if botao_mouse and pode_selecionar:
                    self.som_escolha_feita.play()
                    InformacoesBase.janela = Window(1280, 720)
                    InformacoesBase.resolucao = "ImagensRedimensionadas/"
                    self.cria_imagens_resolucao()
                    opcao_selecionada = True

            else:
                self.tocar_som1 = True

            if (480 / self.F_R) < pos_mouse[0] < (960 / self.F_R) and (665 / self.F_R) < pos_mouse[1] < \
                    (814 / self.F_R):
                cor3 = (125, 125, 125)

                if self.tocar_som2:
                    self.som_selecao.play()
                    self.tocar_som2 = False

                if botao_mouse and pode_selecionar:
                    self.som_escolha_feita.play()
                    InformacoesBase.janela = Window(1600, 900)
                    InformacoesBase.resolucao = "ImagensRedimensionadas/"
                    self.cria_imagens_resolucao()
                    opcao_selecionada = True

            else:
                self.tocar_som2 = True

            if (960 / self.F_R) < pos_mouse[0] < (1440 / self.F_R) and (515 / self.F_R) < pos_mouse[1] < \
                    (665 / self.F_R):
                cor2 = (125, 125, 125)

                if self.tocar_som3:
                    self.som_selecao.play()
                    self.tocar_som3 = False

                if botao_mouse and pode_selecionar:
                    self.som_escolha_feita.play()
                    InformacoesBase.janela = Window(1366, 768)
                    InformacoesBase.resolucao = "ImagensRedimensionadas/"
                    self.cria_imagens_resolucao()
                    opcao_selecionada = True

            else:
                self.tocar_som3 = True

            if (960 / self.F_R) < pos_mouse[0] < (1440 / self.F_R) and (665 / self.F_R) < pos_mouse[1] < \
                    (814 / self.F_R):
                cor4 = (125, 125, 125)

                if self.tocar_som4:
                    self.som_selecao.play()
                    self.tocar_som4 = False

                if botao_mouse and pode_selecionar:
                    self.som_escolha_feita.play()
                    InformacoesBase.janela = Window(1920, 1080)
                    InformacoesBase.resolucao = "1080P/"
                    opcao_selecionada = True
            else:
                self.tocar_som4 = True

            pygame.draw.rect(tela, cor1, ((480 / self.F_R), (515 / self.F_R), 480 / self.F_R, 149 / self.F_R))
            pygame.draw.rect(tela, cor2, ((960 / self.F_R), (515 / self.F_R), (480 / self.F_R), (149 / self.F_R)))
            pygame.draw.rect(tela, cor3, ((480 / self.F_R), (665 / self.F_R), 480 / self.F_R, 149 / self.F_R))
            pygame.draw.rect(tela, cor4, ((960 / self.F_R), (665 / self.F_R), (480 / self.F_R), (149 / self.F_R)))
            self.fundo.draw()
            janela.update()
        return "menu_principal"

    def cria_imagens_resolucao(self):
        resolucao = (InformacoesBase.janela.width, InformacoesBase.janela.height)
        resolucao_base = InformacoesBase.resolucao_base
        fator_redimensionamento = (resolucao_base[0] / resolucao[0], resolucao_base[1] / resolucao[1])

        arquivos = [f for f in listdir(self.diretorio_arquivos) if isfile(join(self.diretorio_arquivos, f))]

        for arquivo in arquivos:
            if arquivo.__contains__(".png"):
                imagem_padrao = Image.open(self.diretorio_arquivos + arquivo)

                tamanho_imagem_padrao = imagem_padrao.size
                imagem_redimensionada = imagem_padrao.resize(
                    (int(tamanho_imagem_padrao[0] / fator_redimensionamento[0]),
                     int(tamanho_imagem_padrao[1] / fator_redimensionamento[1])))
                imagem_redimensionada.save(self.diretorio_salvar + arquivo)
