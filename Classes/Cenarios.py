import random

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
        self.fundo = GameImage("Imagens/Cenario-0.png")
        self.som_cenario = "Sons/Musica_0.mp3"
        self.volume_som_cenario = 0.3
        self.som_passos = "Sons/piso_marmore.wav"
        self.volume_passos = 0.3
        # Configuração das colisões
        self.area_colisoes = [[0, 780, 339, 1080], [463, 862, 829, 1080], [1141, 362, 1466, 567],
                              [829, 781, 1182, 1080], [1182, 919, 1288, 1004], [1203, 571, 1403, 635],
                              [1559, 579, 1678, 661], [1563, 710, 1920, 803], [1687, 300, 1920, 597],
                              [654, 200, 761, 490]]
        self.limite = 213.45

        fm = FlorMedicinal()
        fm.imagem.x = 0
        fm.imagem.y = 500
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
        item_vida.imagem.x = 395
        item_vida.imagem.y = 837
        item_vida2.imagem.x = 658
        item_vida2.imagem.y = 839

        self.itens = [arma, item_vida, item_vida2, fm]

        # Configurações dos Aliados
        esposa_e_filha = Aliados("Imagens/esposa_e_filha.png", "Esposa e Filha")
        esposa_e_filha.sprite.x = 651
        esposa_e_filha.sprite.y = 260
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
        if sprite_jogador.x + sprite_jogador.width > 1668 \
                and 640 < sprite_jogador.y + sprite_jogador.height < 720:
            sprite_jogador.x = 230
            sprite_jogador.y = 647 - sprite_jogador.height
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
        self.fundo = GameImage("Imagens/Cenario_2.png")
        self.som_cenario = "Sons/Musica_1.ogg"
        self.volume_som_cenario = 0.1
        self.som_passos = "Sons/piso_neve.ogg"
        self.volume_passos = 0.2
        # Configuração de colisões
        self.area_colisoes = [[470, 859, 909, 1080], [360, 43, 605, 416], [907, 3, 1486, 458],
                              [1109, 890, 1278, 1069], [1542, 155, 1652, 423], [1603, 854, 1912, 1074],
                              [4, 5, 1910, 376], [0, 563, 138, 742]]
        self.limite = 0

        # Configurações dos inimigos
        self.inimigos = []
        self.area_inimigos = [710, 465, 1847, 854]
        self.area_chefao = [236, 472, 950, 857]
        self.ordas_inimigos = 3
        self.numero_inimigos = 3
        # Configurações dos Aliados
        self.aliados = []

        # Configurações dos itens
        self.itens = []

    def proxima_fase(self, jogador, lista_inimigos):
        sprite_jogador = jogador.sprite
        if sprite_jogador.x + sprite_jogador.width > 1891 \
                and 547 < sprite_jogador.y + sprite_jogador.height < 688 and self.ordas_inimigos == 0 \
                and len(lista_inimigos) == 0:
            sprite_jogador.x = 146
            sprite_jogador.y = 575 - sprite_jogador.height
            InformacoesBase.trocando_cenario = True
            return "cenario_2"
        elif sprite_jogador.x < 168 and 558 < sprite_jogador.y + sprite_jogador.height < 739 \
                and (jogador.inventario.verifica_item("FlorMedicinal") is not False) and len(lista_inimigos) == 0:
            sprite_jogador.x = 1520
            sprite_jogador.y = 705 - sprite_jogador.height
            InformacoesBase.trocando_cenario = True
            return "cenario_0"
        return "cenario_1"


class Cenario2(Cenario0):
    def __init__(self):
        super().__init__()
        self.fundo = GameImage("Imagens/Cenario_3.png")
        self.som_cenario = "Sons/Musica_1.ogg"
        self.volume_som_cenario = 0.1
        self.som_passos = "Sons/piso_neve.ogg"
        self.volume_passos = 0.2
        # Configurações de Colisões
        self.area_colisoes = [[459, 848, 819, 1076], [1001, 806, 1365, 1074], [251, 278, 383, 368],
                              [503, 281, 632, 371], [858, 143, 1113, 414], [1485, 887, 1916, 1074],
                              [5, 3, 1913, 330]]
        self.limite = 0

        # Configuração dos inimigos
        self.inimigos = []
        self.area_inimigos = [845, 421, 1919, 803]
        self.ordas_inimigos = 3
        self.numero_inimigos = 4

        # Configurações dos Aliados
        self.aliados = []

        # Configuração dos itens
        flor_medicinal = FlorMedicinal()
        self.itens = [flor_medicinal]

    def proxima_fase(self, jogador, lista_inimigos):
        sprite_jogador = jogador.sprite
        if sprite_jogador.x < 30 and 488 < sprite_jogador.y + sprite_jogador.height < 658:
            possui_flor = jogador.inventario.verifica_item("FlorMedicinal")
            if (possui_flor and len(lista_inimigos) == 0 and self.ordas_inimigos == 0) or not possui_flor:
                sprite_jogador.x = 1760
                sprite_jogador.y = 644 - sprite_jogador.height
                InformacoesBase.trocando_cenario = True
                return "cenario_1"
        return "cenario_2"


class TelaMorte:
    def __init__(self, imagem):
        # definir o fundo
        self.fundo = GameImage(imagem)

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
            pos_mouse = mouse.get_position()
            if 480 < pos_mouse[0] < 960 and 665 < pos_mouse[1] < 814:
                cor1 = (125, 125, 125)
                if botao_mouse and pode_selecionar:
                    pass
                    # Vai retornar para o menu principal
            elif 960 < pos_mouse[0] < 1440 and 665 < pos_mouse[1] < 814:
                cor2 = (125, 125, 125)
                if botao_mouse and pode_selecionar:
                    janela.close()
            pygame.draw.rect(tela, cor1, (480, 665, 480, 149))
            pygame.draw.rect(tela, cor2, (960, 665, 480, 149))
            self.fundo.draw()
            janela.update()


class TelaPrologo(TelaMorte):
    def __init__(self, dir_imagem):
        # definir o fundo
        super().__init__(dir_imagem)
        self.fundo = GameImage(dir_imagem)

    def tela(self, janela):
        sair = False
        frase_proxima_mensagem = GameImage("Imagens/proxima_mensagem.png")
        while Keyboard().key_pressed("SPACE"):
            janela.update()
        while not (Keyboard().key_pressed("SPACE") and not sair):
            janela.set_background_color("BLACK")
            self.fundo.draw()
            frase_proxima_mensagem.draw()
            janela.update()
