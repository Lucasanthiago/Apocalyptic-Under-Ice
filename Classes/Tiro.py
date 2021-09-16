from Classes.VariaveisGerais import *
from PPlay.gameimage import *


class Tiro:
    def __init__(self, incremento, dano, sprite_jogador):
        self.F_R = InformacoesBase.fator_redimensionamento
        self.imagem = GameImage("Imagens/" + InformacoesBase.resolucao + "tiro.png")
        self.imagem.x = sprite_jogador.x + sprite_jogador.width / 2.8
        self.imagem.y = sprite_jogador.y + (sprite_jogador.height / 4)

        self.incremento_x = incremento[0]
        self.incremento_y = incremento[1]
        self.dano = dano
        self.velocidade = (3000 / self.F_R)

    def movimenta_tiro(self):
        self.imagem.x += self.incremento_x * self.velocidade
        self.imagem.y += self.incremento_y * self.velocidade
