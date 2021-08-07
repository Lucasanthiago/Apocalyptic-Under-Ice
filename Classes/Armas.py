from PPlay.sprite import *


class Pistola:
    def __init__(self, dir_imagem):
        self.dir_imagem = dir_imagem
        self.dano = 10

    def retorna_sprite_pistola(self):
        sprite = Sprite(self.dir_imagem)
        return sprite
