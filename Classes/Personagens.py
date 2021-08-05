from math import sqrt
from PPlay.keyboard import *
from PPlay.sprite import *
from PPlay.mouse import *
from Classes.Falas import *
import math


class Personagem:

    def __init__(self, dir_imagem, janela, fundo):
        # Dados Gerais
        self.janela = janela
        self.fundo = fundo
        self.teclado = Keyboard()

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

    def fisica(self):
        # Atribuições
        personagem = self.personagem
        vel = self.velocidade
        janela = self.janela
        fundo = self.fundo

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


class Inimigos(Personagem):

    def __init__(self, dir_imagem, janela, fundo, sprite_jogador, velocidade_jogador):
        super().__init__(dir_imagem, janela, fundo)

        # Configurações Animação
        self.numero_sprites = 10
        self.tempo_animacao = 20
        self.personagem = Sprite(dir_imagem, self.numero_sprites)

        # Dados do Personagem
        self.velocidade = 100
        self.raio_de_agressividade = (self.personagem.width + self.personagem.height)
        self.raio_de_dano = self.raio_de_agressividade / 5

        # Dados do jogador
        self.jogador = sprite_jogador
        self.velocidade_jogador = velocidade_jogador

    def fisica_outros(self):
        # Atribuições
        teclado = Keyboard()
        inimigo = self.personagem
        vel = self.velocidade_jogador
        vel_diagonal = vel / sqrt(2)
        vel_padrao = vel
        janela = self.janela
        fundo = self.fundo
        jogador = self.jogador

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

    def inteligencia_artificial(self):
        # Atribuições
        inimigo = self.personagem
        jogador = self.jogador
        janela = self.janela

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


class Aliados(Inimigos):
    def __init__(self, dir_imagem, janela, fundo, sprite_jogador, velocidade_jogador, aliado):
        super().__init__(dir_imagem, janela, fundo, sprite_jogador, velocidade_jogador)

        # Configurações Animação
        self.numero_sprites = 10
        self.tempo_animacao = 20
        self.personagem = Sprite(dir_imagem, self.numero_sprites)

        # Dados do Personagem
        self.raio_de_conversa = (self.personagem.width + self.personagem.height) / 5
        self.aliado = aliado
        self.fala = 0

        # Dados do jogador
        self.jogador = sprite_jogador

    def inteligencia_artificial(self):
        # Atribuições
        jogador = self.jogador
        personagem = self.personagem
        teclado = self.teclado

        # Calcular as coordenadas do centro do jogador e inimigo
        inimigo_x = personagem.x + personagem.width / 2
        inimigo_y = personagem.y + personagem.height / 2
        jogador_x = jogador.x + jogador.width / 2
        jogador_y = jogador.y + jogador.height / 2

        # Equação do círculo
        equacao_circulo = (jogador_x - inimigo_x) ** 2 + (jogador_y - inimigo_y) ** 2

        if equacao_circulo <= self.raio_de_conversa ** 2 and teclado.key_pressed("F"):
            self.conversa()

    def conversa(self):
        # Atribuições
        janela = self.janela
        conversar = True
        mouse = Mouse()
        falas = getattr(Falas, self.aliado)
        fala = self.fala

        # Loop de Falas
        while conversar:
            # Desenha a fala
            janela.draw_text(falas[fala], 20, 20, 22, "RED", "Arial")

            # Atualiza as falas e sai do diálogo
            if mouse.is_button_pressed(1):
                conversar = False
                fala += 1
                self.fala = fala % (len(falas))

            janela.update()

    def verifica_especial(self):
        if self.aliado == "nomeAliadoEspecial":
            return True
        return False
