from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.mouse import *
from Classes.Tiro import *
import math


class Pistola:
    def __init__(self):
        self.imagem = GameImage("Imagens/pistola.png")
        self.imagem_escalada = GameImage("Imagens/pistola_escalada.png")
        self.imagem.x = 1215
        self.imagem.y = 593
        self.dano = 15
        self.raio_proximo = 70
        self.tempo_recarga = 0.6
        self.cronometro = 0

    def desenha(self):
        self.imagem.draw()

    def desenha_imagem_escalada(self):
        self.imagem_escalada.draw()

    def verifica_proximo(self, sprite_jogador):
        jogador_x = sprite_jogador.x + sprite_jogador.width
        jogador_y = sprite_jogador.y + sprite_jogador.height - 20
        arma_x = self.imagem.x + self.imagem.width / 2
        arma_y = self.imagem.y + self.imagem.height / 2

        equacao_circulo = (jogador_x - arma_x) ** 2 + (jogador_y - arma_y) ** 2
        if equacao_circulo <= self.raio_proximo ** 2:
            return True
        return False

    def atira(self, janela, sprite_jogador, matriz_tiros):
        mouse = Mouse()
        self.cronometro += janela.delta_time()

        if self.cronometro >= self.tempo_recarga and mouse.is_button_pressed(1):
            coord_mouse = mouse.get_position()
            coord_arma = (sprite_jogador.x + 10, sprite_jogador.y + sprite_jogador.height / 2 - 50)
            # Distancias
            x = math.fabs(coord_arma[0] - coord_mouse[0])
            y = math.fabs(coord_arma[1] - coord_mouse[1])
            print(x, y)
            # Elimina o erro de quando o x for 0
            try:
                angulo_jogador_inimigo = math.atan(y / x)
            except ZeroDivisionError:
                angulo_jogador_inimigo = 0
            # Calcula os incrementos
            incremento_y = math.sin(angulo_jogador_inimigo)
            incremento_x = math.cos(angulo_jogador_inimigo)
            #print((incremento_x, incremento_y))
            # Calculando a direção em que deve-se ir
            multi_x = 1
            multi_y = 1

            if coord_mouse[0] < coord_arma[0]:
                multi_x = -1
            if coord_mouse[1] <= coord_arma[1]:
                multi_y = -1

            # Incrementando
            incremento_x = incremento_x * janela.delta_time() * multi_x
            incremento_y = incremento_y * janela.delta_time() * multi_y
            tiro = Tiro((incremento_x, incremento_y), self.dano, coord_arma[0], coord_arma[1])
            matriz_tiros.append(tiro)

            self.cronometro = 0


class Faca:
    def __init__(self, dir_imagem):
        self.dir_imagem = dir_imagem
        self.dano = 5

    def retorna_sprite_faca(self):
        sprite = Sprite(self.dir_imagem)
        return sprite


class Arco:
    def __init__(self, dir_imagem):
        self.dir_imagem = dir_imagem
        self.dano = 10

    def retorna_sprite_arco(self):
        sprite = Sprite(self.dir_imagem)
        return sprite


class Fuzil:
    def __init__(self, dir_imagem):
        self.dir_imagem = dir_imagem
        self.dano = 30

    def retorna_sprite_fuzil(self):
        sprite = Sprite(self.dir_imagem)
        return sprite
