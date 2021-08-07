from PPlay.sprite import *


class Pistola:
    def __init__(self, dir_imagem):
        self.dir_imagem = dir_imagem
        self.dano = 15

    def retorna_sprite_pistola(self):
        sprite = Sprite(self.dir_imagem)
        return sprite


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
