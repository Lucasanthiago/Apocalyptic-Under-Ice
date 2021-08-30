from PPlay.sprite import *
from PPlay.gameimage import *


class Pistola:
    def __init__(self):
        self.imagem = GameImage("Imagens/pistola.png")
        self.imagem.x = 1215
        self.imagem.y = 593
        self.dano = 15
        self.raio_proximo = 70

    def desenha(self):
        self.imagem.draw()

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

    def atira(self):
        print("ATIRANDO")

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
