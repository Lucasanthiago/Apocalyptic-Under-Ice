from PPlay.gameimage import *


class Tiro:
    def __init__(self, incremento, dano, jogador_x, jogador_y):
        self.imagem = GameImage("Imagens/tiro.png")
        self.imagem.x = jogador_x
        self.imagem.y = jogador_y

        self.incremento_x = incremento[0]
        self.incremento_y = incremento[1]
        self.dano = dano
        self.velocidade = 3000

    def movimenta_tiro(self):
        self.imagem.x += self.incremento_x * self.velocidade
        self.imagem.y += self.incremento_y * self.velocidade
