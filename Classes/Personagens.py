from math import sqrt
from PPlay.keyboard import *
from PPlay.sprite import *


def fisica_personagens(personagem, janela, fundo, vel):
    # Variaveis Principais
    teclado = Keyboard()
    vel_diagonal = vel / sqrt(2)
    vel_padrao = vel

    # Controla a velocidade do jogador
    if (teclado.key_pressed("RIGHT") or teclado.key_pressed("LEFT")) and (
            teclado.key_pressed("UP") or teclado.key_pressed("DOWN")):
        vel = vel_diagonal
    else:
        vel = vel_padrao

    # Movimento no Eixo X
    if 0 <= personagem.x <= janela.width - personagem.width:
        if round(personagem.x) == round(janela.width / 2 - personagem.width / 2):
            if teclado.key_pressed("RIGHT"):
                if fundo.x + fundo.width > janela.width:
                    fundo.x -= vel
                else:
                    personagem.move_key_x(vel)
            if teclado.key_pressed("LEFT"):
                if fundo.x < 0:
                    fundo.x += vel
                else:
                    personagem.move_key_x(vel)
        else:
            personagem.move_key_x(vel)

    # Colisão com as laterais
    if personagem.x < 0:
        personagem.x = 0
    elif personagem.x > janela.width - personagem.width:
        personagem.x = janela.width - personagem.width

    if fundo.x > 0:
        fundo.x = 0
    elif fundo.x + fundo.width < janela.width:
        fundo.x = janela.width - fundo.width

    # Movimento no Eixo Y
    if 0 <= personagem.y <= janela.height - personagem.height:
        if round(personagem.y) == round(janela.height / 2 - personagem.height / 2):
            if teclado.key_pressed("DOWN"):
                if fundo.y + fundo.height > janela.height:
                    fundo.y -= vel
                else:
                    personagem.move_key_y(vel)
            if teclado.key_pressed("UP"):
                if fundo.y < 0:
                    fundo.y += vel
                else:
                    personagem.move_key_y(vel)
        else:
            personagem.move_key_y(vel)

    # Colisão com o topo e a base
    if personagem.y < 0:
        personagem.y = 0
    elif personagem.y > janela.height - personagem.height:
        personagem.y = janela.height - personagem.height

    if fundo.y > 0:
        fundo.y = 0
    elif fundo.y + fundo.height < janela.height:
        fundo.y = janela.height - fundo.height


class PersonagemPrincipal:

    def __init__(self):
        # Configurações Animação
        self.numero_sprites = 10
        self.tempo_animacao = 100
        # Dados do Personagem
        self.velocidade = 0.1

    def sprite_personagem_principal(self, dir_imagem):
        # Importa as imagens do personagem principal
        personagem = Sprite(dir_imagem, self.numero_sprites)
        personagem.set_sequence_time(0, self.numero_sprites - 1, self.tempo_animacao, True)
        return personagem
