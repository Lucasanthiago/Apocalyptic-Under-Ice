from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.keyboard import *
import math

class Pistola:
    def __init__(self):
        self.imagem = GameImage("Imagens/pistola.png")
        self.imagem_escalada = GameImage("Imagens/pistola_escalada.png")
        self.imagem.x = 1215
        self.imagem.y = 593
        self.dano = 15
        self.raio_proximo = 70
        self.tiros = []

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
        print(equacao_circulo)
        if equacao_circulo <= self.raio_proximo ** 2:
            return True
        return False

    def atirar(self, jogador, janela):
        if Keyboard().key_pressed("SPACE"):
            tiro = Sprite("Imagens/Bola.png")
            print(tiro.width)
            tiro.set_position(jogador.x + jogador.width / 2, jogador.y - tiro.height)
            self.tiros.append(tiro)

        variacao = 0
        for shot in self.tiros:
            shot.x = shot.x + 300 * janela.delta_time()
            if shot.x <= 0 - shot.width:
                self.tiros.remove(shot)
                variacao += 1

    def desenha_tiro(self):
        for i in range(len(self.tiros)):
            self.tiros[i].draw()


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
