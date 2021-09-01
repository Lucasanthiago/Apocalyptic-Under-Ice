from math import sqrt
from PPlay.keyboard import *
from PPlay.sprite import *
from PPlay.mouse import *
from Classes.Falas import *
from Classes.VariaveisGerais import *
import math


class Personagem:

    def __init__(self):
        # Dados Gerais
        self.teclado = Keyboard()

        # Configurações Animação
        self.numero_sprites = 1
        self.tempo_animacao = 100
        self.sprite_jogador = Sprite("Imagens/personagem-parado.png", 1)
        self.sprite_jogador_E = Sprite("Imagens/personagem-parado-E.png", 1)
        self.sprite_jogador_correndo_D = Sprite("Imagens/personagem-correndo-direita.png", 6)
        self.sprite_jogador_correndo_D.set_sequence_time(0, 6, 120, True)
        self.sprite_jogador_correndo_E = Sprite("Imagens/personagem-correndo-esquerda.png", 6)
        self.sprite_jogador_correndo_E.set_sequence_time(0, 6, 120, True)
        # Dados do Personagem
        self.vida = 100
        self.vida_maxima = 100
        self.velocidade = 500
        self.slot_equipado = 1
        self.ultimo_slot = 1

    def fisica(self, janela, sprite_jogador):
        # Atribuições
        personagem = sprite_jogador
        # Resetando Movimentos
        InformacoesBase.movendo_esquerda = False
        InformacoesBase.movendo_direita = False
        InformacoesBase.movendo_baixo = False
        InformacoesBase.movendo_cima = False
        # Variaveis Principais
        teclado = Keyboard()
        vel = self.velocidade
        vel_diagonal = vel / sqrt(2)
        vel_padrao = vel

        # Controla a velocidade do jogador
        if (teclado.key_pressed("D") or teclado.key_pressed("A")) and (
                teclado.key_pressed("W") or teclado.key_pressed("S")):
            vel = vel_diagonal * janela.delta_time()
        else:
            vel = vel_padrao * janela.delta_time()
        # Movimento no Eixo X e Y
        if 0 <= personagem.x <= janela.width - personagem.width:
            if teclado.key_pressed("D"):
                personagem.x += vel
                InformacoesBase.movendo_direita = True
            elif teclado.key_pressed("A"):
                personagem.x -= vel
                InformacoesBase.movendo_esquerda = True

        if 0 <= personagem.y <= janela.height - personagem.height:
            if teclado.key_pressed("S"):
                personagem.y += vel
                InformacoesBase.movendo_baixo = True
            elif teclado.key_pressed("W"):
                personagem.y -= vel
                InformacoesBase.movendo_cima = True
        # Colisão com as laterais
        if personagem.x < 0:
            personagem.x = 0
        elif personagem.x > janela.width - personagem.width:
            personagem.x = janela.width - personagem.width

        # Colisão com o topo e a base
        if personagem.y < 0:
            personagem.y = 0
        elif personagem.y > janela.height - personagem.height:
            personagem.y = janela.height - personagem.height

    def troca_sprite_armas(self, sprite_jogador, inventario):
        if inventario.alterou_inventario or self.slot_equipado != self.ultimo_slot:
            x = sprite_jogador.x
            y = sprite_jogador.y
            if inventario.inventario[self.slot_equipado - 1] != 0:
                nome = "-" + inventario.inventario[self.slot_equipado - 1].__class__.__name__ + ".png"
            else:
                nome = ".png"
            self.sprite_jogador = Sprite("Imagens/personagem-parado" + nome, 1)
            self.sprite_jogador_E = Sprite("Imagens/personagem-parado-E" + nome, 1)
            self.sprite_jogador_correndo_D = Sprite("Imagens/personagem-correndo-direita" + nome, 6)
            self.sprite_jogador_correndo_D.set_sequence_time(0, 6, 120, True)
            self.sprite_jogador_correndo_E = Sprite("Imagens/personagem-correndo-esquerda" + nome, 6)
            self.sprite_jogador_correndo_E.set_sequence_time(0, 6, 120, True)
            self.sprite_jogador.x = x
            self.sprite_jogador.y = y
            self.ultimo_slot = self.slot_equipado
            inventario.alterou_inventario = False

class Inimigos(Personagem):

    def __init__(self, dir_imagem, fundo, sprite_jogador, velocidade_jogador):
        super().__init__(dir_imagem, fundo)

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

    def fisica_outros(self, janela):
        # Atribuições
        teclado = Keyboard()
        inimigo = self.personagem
        vel = self.velocidade_jogador
        vel_diagonal = vel / sqrt(2)
        vel_padrao = vel
        fundo = self.fundo
        jogador = self.jogador

        # Controla a velocidade do inimigo
        if (teclado.key_pressed("RIGHT") or teclado.key_pressed("LEFT")) and (
                teclado.key_pressed("UP") or teclado.key_pressed("DOWN")):
            vel = vel_diagonal * janela.delta_time()
        else:
            vel = vel_padrao * janela.delta_time()

        # Física Eixo X
        if round(janela.width / 2 - jogador.width / 2) - 10 \
                < round(jogador.y) < \
                round(janela.width / 2 - jogador.width / 2) + 10:
            if teclado.key_pressed("RIGHT"):
                if fundo.x + fundo.width > janela.width:
                    inimigo.x -= vel
            if teclado.key_pressed("LEFT"):
                if fundo.x < 0:
                    inimigo.x += vel
        # Física Eixo Y
        if round(janela.height / 2 - jogador.height / 2) - 10 \
                < round(jogador.y) < \
                round(janela.height / 2 - jogador.height / 2) + 10:
            if teclado.key_pressed("DOWN"):
                if fundo.y + fundo.height > janela.height:
                    inimigo.y -= vel
            if teclado.key_pressed("UP"):
                if fundo.y < 0:
                    inimigo.y += vel

    def inteligencia_artificial(self, janela):
        # Atribuições
        inimigo = self.personagem
        jogador = self.jogador

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
            # Elimina o erro de quando o x for 0
            try:
                angulo_jogador_inimigo = math.fabs(math.atan(y / x))
            except ZeroDivisionError:
                angulo_jogador_inimigo = 0
            # Calcula os incrementos
            incremento_y = math.sin(angulo_jogador_inimigo)
            incremento_x = math.cos(angulo_jogador_inimigo)

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
    def __init__(self, dir_imagem, fundo, sprite_jogador, velocidade_jogador, aliado):
        super().__init__(dir_imagem, fundo, sprite_jogador, velocidade_jogador)

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

    def inteligencia_artificial(self, janela):
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
            self.conversa(janela)

    def conversa(self, janela):
        # Atribuições
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
