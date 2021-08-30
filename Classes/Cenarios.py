from PPlay import sprite
from PPlay.gameimage import *
from Classes.Arma import *
from PPlay.keyboard import *
from Classes.Colisoes import *
from Classes.VariaveisGerais import *
from math import sqrt


class Cenario0:
    def __init__(self):
        self.fundo = GameImage("Imagens/Cenario-0.png")
        self.area_colisoes = [[0, 780, 339, 1080], [463, 862, 829, 1080], [1141, 362, 1466, 567],
                              [829, 781, 1182, 1080], [1182, 919, 1288, 1004], [1203, 571, 1403, 635],
                              [1559, 579, 1678, 661], [1563, 710, 1920, 803], [1687, 300, 1920, 597]]
        self.colisao_antiga = [[] for _ in range(len(self.area_colisoes))]
        self.limite = 213.45
        arma = Pistola()
        self.itens = [arma]

    def colisoes_cenario(self, sprite_jogador):
        atras = False
        if sprite_jogador.y > self.limite:
            for i in range(len(self.area_colisoes)):
                if self.area_colisoes[i][1] > sprite_jogador.y + sprite_jogador.height:
                    atras = True
                colisao = colisao_retangulo(sprite_jogador, self.area_colisoes[i], atras)
                if colisao is not True:
                    self.colisao_antiga[i] = colisao
                else:
                    indice = self.colisao_antiga[i].index(False)
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

    def proxima_fase(self, sprite_jogador):
        if 1638 < sprite_jogador.x + sprite_jogador.width < 1703 \
                and 640 < sprite_jogador.y + sprite_jogador.height < 703:
            sprite_jogador.x = 0
            sprite_jogador.y = 0
            return "cenario_1"
        return "cenario_0"


class Cenario1(Cenario0):
    def __init__(self):
        super().__init__()
        self.fundo = GameImage("Imagens/Cenario3.png")
        self.area_colisoes = [[0, 780, 339, 1080], [463, 862, 829, 1080], [1141, 362, 1466, 567],
                              [829, 781, 1182, 1080], [1182, 919, 1288, 1004], [1203, 571, 1403, 635],
                              [1559, 579, 1678, 661], [1563, 710, 1920, 803], [1687, 300, 1920, 597]]
        self.colisao_antiga = [[] for _ in range(len(self.area_colisoes))]
        self.itens = []
        self.limite = 0

    def proxima_fase(self, sprite_jogador):
        if 0 <= sprite_jogador.x < 20 \
                and 519 < sprite_jogador.y + sprite_jogador.height < 598:
            sprite_jogador.x = 0
            sprite_jogador.y = 0
            return "cenario_0"
        return "cenario_1"