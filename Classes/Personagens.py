from math import sqrt
from PPlay.keyboard import *
from PPlay.sprite import *
import math


class Personagem:

    def __init__(self, dir_imagem):
        # Configurações Animação
        self.numero_sprites = 10
        self.tempo_animacao = 100
        self.personagem = Sprite(dir_imagem, self.numero_sprites)

        # Dados do Personagem
        self.velocidade = 200

    def sprite(self):
        # Importa as imagens do personagem principal
        self.personagem.set_sequence_time(0, self.numero_sprites - 1, self.tempo_animacao, True)
        return self.personagem

    def fisica(self, janela, fundo):
        # Atribuições
        personagem = self.personagem
        vel = self.velocidade

        # Variaveis Principais
        teclado = Keyboard()
        vel_diagonal = vel / sqrt(2)
        vel_padrao = vel

        # Controla a velocidade do jogador
        if (teclado.key_pressed("RIGHT") or teclado.key_pressed("LEFT")) and (
                teclado.key_pressed("UP") or teclado.key_pressed("DOWN")):
            vel = vel_diagonal * janela.delta_time()
        else:
            vel = vel_padrao * janela.delta_time()

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

    def fisica_outros(self, fundo):
        personagem = self.personagem

        # Colisão com as laterais
        if personagem.x < fundo.x:
            personagem.x = fundo.x
        elif personagem.x > fundo.x + fundo.width:
            personagem.x = fundo.x + fundo.width

        # Colisão com o topo e a base
        if personagem.y < fundo.y:
            personagem.y = fundo.y
        elif personagem.y > fundo.y + fundo.height:
            personagem.y = fundo.y + fundo.height


class Inimigos(Personagem):

    def __init__(self, dir_imagem):
        super().__init__(dir_imagem)

        # Configurações Animação
        self.numero_sprites = 10
        self.tempo_animacao = 20
        self.personagem = Sprite(dir_imagem, self.numero_sprites)

        # Dados do Personagem
        self.velocidade = 100
        self.raio_de_agressividade = (self.personagem.width + self.personagem.height)
        self.raio_de_dano = self.raio_de_agressividade / 5

    def fisica_inimigo(self, janela, fundo, jogador, vel):
        # Atribuições
        teclado = Keyboard()
        inimigo = self.personagem
        vel_diagonal = vel / sqrt(2)
        vel_padrao = vel

        # Controla a velocidade do inimigo
        if (teclado.key_pressed("RIGHT") or teclado.key_pressed("LEFT")) and (
                teclado.key_pressed("UP") or teclado.key_pressed("DOWN")):
            vel = vel_diagonal * janela.delta_time()
        else:
            vel = vel_padrao * janela.delta_time()

        # Física Eixo X
        if round(jogador.x) == round(janela.width / 2 - jogador.width / 2):
            if teclado.key_pressed("RIGHT"):
                if fundo.x + fundo.width > janela.width:
                    inimigo.x -= vel
            if teclado.key_pressed("LEFT"):
                if fundo.x < 0:
                    inimigo.x += vel
        # Física Eixo Y
        if round(jogador.y) == round(janela.height / 2 - jogador.height / 2):
            if teclado.key_pressed("DOWN"):
                if fundo.y + fundo.height > janela.height:
                    inimigo.y -= vel
            if teclado.key_pressed("UP"):
                if fundo.y < 0:
                    inimigo.y += vel

    def inteligencia_artificial(self, janela, jogador):
        # Atribuições
        inimigo = self.personagem

        # Calcular as coordenadas do centro do jogador e inimigo
        inimigo_x = inimigo.x + inimigo.width / 2
        inimigo_y = inimigo.y + inimigo.height / 2
        jogador_x = jogador.x + jogador.width / 2
        jogador_y = jogador.y + jogador.height / 2

        # Equação do círculo
        equacao_circulo = (jogador_x - inimigo_x) ** 2 + (jogador_y - inimigo_y) ** 2

        if self.raio_de_dano ** 2 <= equacao_circulo <= self.raio_de_agressividade ** 2:
            # Cálculo do Incremento
            x = jogador.x - inimigo.x
            y = jogador.y - inimigo.y
            angulo_jogador_inimigo = math.fabs(math.atan(x / y))
            incremento_x = math.sin(angulo_jogador_inimigo)
            incremento_y = math.cos(angulo_jogador_inimigo)

            # Calculando a direção em que deve-se ir
            multi_x = 1
            multi_y = 1

            if inimigo.x > jogador.x:
                multi_x = -1
            if inimigo.y >= jogador.y:
                multi_y = -1

            # Incrementando
            incremento_x *= self.velocidade
            incremento_y *= self.velocidade
            inimigo.x += incremento_x * janela.delta_time() * multi_x
            inimigo.y += incremento_y * janela.delta_time() * multi_y
