from math import sqrt
from random import uniform

import pygame.mixer

from PPlay.gameimage import *
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
        self.F_R = InformacoesBase.fator_redimensionamento
        # Configurações Animação
        self.numero_sprites = 1
        self.tempo_animacao = 120
        self.sprite = Sprite("Imagens/" + InformacoesBase.resolucao + "personagem-parado.png", 1)
        self.sprite_E = Sprite("Imagens/" + InformacoesBase.resolucao + "personagem-parado-E.png", 1)
        self.sprite_correndo_D = Sprite("Imagens/" + InformacoesBase.resolucao + "personagem-correndo-direita.png", 6)
        self.sprite_correndo_D.set_sequence_time(0, 6, self.tempo_animacao, True)
        self.sprite_correndo_E = Sprite("Imagens/" + InformacoesBase.resolucao + "personagem-correndo-esquerda.png", 6)
        self.sprite_correndo_E.set_sequence_time(0, 6, self.tempo_animacao, True)
        self.correcao_sprite_D = self.sprite.width
        self.correcao_sprite_E = + (30 / self.F_R)
        # Dados do Personagem
        self.vida = 100
        self.vida_maxima = 100
        self.velocidade = (500 / self.F_R)
        self.slot_equipado = 1
        self.ultimo_slot = 1
        self.inventario = None
        self.som_receber_dano = pygame.mixer.Sound("Sons/hit_aliado.flac")
        self.som_receber_dano.set_volume(0.6)
        # Dados de Movimento
        self.movendo_cima = False
        self.movendo_baixo = False
        self.movendo_esquerda = False
        self.movendo_direita = False
        self.ultimo_mov_D = True
        self.colisao_antiga = None

    def fisica(self, janela, sprite_jogador):
        # Atribuições
        personagem = sprite_jogador
        # Resetando Movimentos
        self.movendo_esquerda = False
        self.movendo_direita = False
        self.movendo_baixo = False
        self.movendo_cima = False
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
                self.movendo_direita = True
            elif teclado.key_pressed("A"):
                personagem.x -= vel
                InformacoesBase.movendo_esquerda = True
                self.movendo_esquerda = True

        if 0 <= personagem.y <= janela.height - personagem.height:
            if teclado.key_pressed("S"):
                personagem.y += vel
                InformacoesBase.movendo_baixo = True
                self.movendo_baixo = True
            elif teclado.key_pressed("W"):
                personagem.y -= vel
                InformacoesBase.movendo_cima = True
                self.movendo_cima = True
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

    def troca_sprite_armas(self):
        inventario = self.inventario
        if inventario.alterou_inventario or self.slot_equipado != self.ultimo_slot:
            x = self.sprite.x
            y = self.sprite.y
            if inventario.inventario[self.slot_equipado - 1] != 0:
                nome = "-" + inventario.inventario[self.slot_equipado - 1].__class__.__name__ + ".png"
            else:
                nome = ".png"

            if nome == "-FlorMedicinal.png" or nome == "-ItemVida.png" or nome == "-PlacaHabilidade.png":
                nome = ".png"

            self.sprite = Sprite("Imagens/" + InformacoesBase.resolucao + "personagem-parado" + nome, 1)
            self.sprite_E = Sprite("Imagens/" + InformacoesBase.resolucao + "personagem-parado-E" + nome, 1)
            self.sprite_correndo_D = Sprite("Imagens/" + InformacoesBase.resolucao + "personagem-correndo-direita" + nome, 6)
            self.sprite_correndo_D.set_sequence_time(0, 6, self.tempo_animacao, True)
            self.sprite_correndo_E = Sprite("Imagens/" + InformacoesBase.resolucao + "personagem-correndo-esquerda" + nome, 6)
            self.sprite_correndo_E.set_sequence_time(0, 6, self.tempo_animacao, True)
            self.sprite.x = x
            self.sprite.y = y
            self.ultimo_slot = self.slot_equipado
            inventario.alterou_inventario = False

    def troca_sprite(self):
        if self.movendo_direita:
            self.sprite_correndo_D.x = self.sprite.x - self.correcao_sprite_D
            self.sprite_correndo_D.y = self.sprite.y
            self.ultimo_mov_D = True
            return [self.sprite_correndo_D, True]
        elif self.movendo_esquerda:
            self.sprite_correndo_E.x = self.sprite.x - self.correcao_sprite_E
            self.sprite_correndo_E.y = self.sprite.y
            self.ultimo_mov_D = False
            return [self.sprite_correndo_E, True]
        else:
            if self.movendo_cima or self.movendo_baixo:
                if self.ultimo_mov_D:
                    self.sprite_correndo_D.x = self.sprite.x - self.correcao_sprite_D
                    self.sprite_correndo_D.y = self.sprite.y
                    return [self.sprite_correndo_D, True]
                else:
                    self.sprite_correndo_E.x = self.sprite.x - self.correcao_sprite_E
                    self.sprite_correndo_E.y = self.sprite.y
                    return [self.sprite_correndo_E, True]
            elif self.ultimo_mov_D:
                return [self.sprite, False]
            else:
                self.sprite_E.x = self.sprite.x
                self.sprite_E.y = self.sprite.y
                return [self.sprite_E, False]

    def recebe_dano(self, quantia):
        self.som_receber_dano.play()
        self.vida -= quantia
        if self.vida <= 0:
            self.vida = 0
            self.morreu()

    def morreu(self):
        InformacoesBase.morreu = True


class Inimigos(Personagem):

    def __init__(self):
        super().__init__()

        # Configurações Animação
        self.numero_sprites = 10
        self.tempo_animacao = 120
        self.sprite = Sprite("Imagens/" + InformacoesBase.resolucao + "inimigo-parado-D.png", 1)
        self.sprite_E = Sprite("Imagens/" + InformacoesBase.resolucao + "inimigo-parado-E.png", 1)
        self.sprite_correndo_D = Sprite("Imagens/" + InformacoesBase.resolucao + "Inimigo_Correndo_direita.png", 6)
        self.sprite_correndo_D.set_sequence_time(0, 6, self.tempo_animacao, True)
        self.sprite_correndo_E = Sprite("Imagens/" + InformacoesBase.resolucao + "Inimigo_Correndo_esquerda.png", 6)
        self.sprite_correndo_E.set_sequence_time(0, 6, self.tempo_animacao, True)
        self.correcao_sprite_D = (0 / self.F_R)
        self.correcao_sprite_E = (0 / self.F_R)

        # Dados do Personagem
        self.vida = 100
        self.velocidade = (330 / self.F_R)
        self.raio_de_agressividade = (1000 / self.F_R)
        self.raio_de_dano = self.raio_de_agressividade / 5
        self.tempo_dano = 1
        self.contador_dano = 0
        self.dano = 15
        self.tomou_dano = False

        # Dados de Som
        self.som = pygame.mixer.Sound("Sons/som_inimigo.ogg")
        self.som.set_volume(0.5)
        self.TEMPO_RECARGA_SOM = uniform(1.0, 5.0)
        self.contador_som = 0
        self.som_receber_dano = pygame.mixer.Sound("Sons/hit_monstro.ogg")
        self.som_receber_dano.set_volume(0.4)
        self.som_morte = pygame.mixer.Sound("Sons/morte_monstro.wav")

        # Dados de Movimento
        self.movendo_cima = False
        self.movendo_baixo = False
        self.movendo_esquerda = False
        self.movendo_direita = False
        self.ultimo_mov_D = True

    def inteligencia_artificial(self, janela, jogador):
        # Atribuições
        inimigo = self.sprite
        sprite_jogador = jogador.sprite
        # Cronometro
        self.contador_dano += janela.delta_time()
        self.contador_som += janela.delta_time()
        # Zerando posições
        self.movendo_cima = False
        self.movendo_baixo = False
        self.movendo_esquerda = False
        self.movendo_direita = False

        # Reproduzindo o som
        if self.contador_som >= self.TEMPO_RECARGA_SOM:
            self.som.play()
            self.contador_som = 0

        # Calcular as coordenadas do centro do jogador e inimigo
        inimigo_x = inimigo.x + inimigo.width / 2
        inimigo_y = inimigo.y + inimigo.height / 2
        jogador_x = sprite_jogador.x + sprite_jogador.width / 2
        jogador_y = sprite_jogador.y + sprite_jogador.height / 2

        # Equação do círculo
        equacao_circulo = (jogador_x - inimigo_x) ** 2 + (jogador_y - inimigo_y) ** 2

        if self.raio_de_dano ** 2 <= equacao_circulo <= self.raio_de_agressividade ** 2 or \
                (self.tomou_dano and self.raio_de_dano ** 2 < equacao_circulo):

            # Cálculo do Incremento
            x = sprite_jogador.x - inimigo.x
            y = sprite_jogador.y - inimigo.y
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

            if inimigo.x > sprite_jogador.x:
                multi_x = -1
                self.movendo_esquerda = True
            else:
                self.movendo_direita = True
            if inimigo.y >= sprite_jogador.y:
                multi_y = -1
                self.movendo_cima = True
            else:
                self.movendo_baixo = True

            # Incrementando
            incremento_x *= self.velocidade
            incremento_y *= self.velocidade
            inimigo.x += incremento_x * janela.delta_time() * multi_x
            inimigo.y += incremento_y * janela.delta_time() * multi_y

        elif self.raio_de_dano ** 2 > equacao_circulo:
            if self.contador_dano >= self.tempo_dano:
                jogador.recebe_dano(self.dano)
                self.contador_dano = 0

    def morreu(self):
        pass


class Chefao(Inimigos):
    def __init__(self):
        super().__init__()
        # Configurações Animação
        self.numero_sprites = 10
        self.tempo_animacao = 120
        self.sprite = Sprite("Imagens/" + InformacoesBase.resolucao + "Chefao-parado-D.png", 1)
        self.sprite_E = Sprite("Imagens/" + InformacoesBase.resolucao + "Chefao-parado-E.png", 1)
        self.sprite_correndo_D = Sprite("Imagens/" + InformacoesBase.resolucao + "Chefao_Correndo_direita.png", 6)
        self.sprite_correndo_D.set_sequence_time(0, 6, self.tempo_animacao, True)
        self.sprite_correndo_E = Sprite("Imagens/" + InformacoesBase.resolucao + "Chefao_Correndo_esquerda.png", 6)
        self.sprite_correndo_E.set_sequence_time(0, 6, self.tempo_animacao, True)
        self.correcao_sprite_D = 0
        self.correcao_sprite_E = 0
        self.som = pygame.mixer.Sound("Sons/som_chefao.ogg")
        # Dados do Personagem
        self.vida = 700
        self.velocidade = (250 / self.F_R)
        self.raio_de_agressividade = (2000 / self.F_R)
        self.raio_de_dano = self.raio_de_agressividade / 10
        self.tempo_dano = 1
        self.contador_dano = 0
        self.dano = 45


class Aliados:
    def __init__(self, dir_imagem, nome_aliado):

        self.F_R = InformacoesBase.fator_redimensionamento
        # Configurações Animação
        self.numero_sprites = 1
        self.sprite = Sprite(dir_imagem, self.numero_sprites)

        # Dados do Personagem
        self.raio_de_conversa = (self.sprite.width + self.sprite.height) / 3
        self.fala = 0
        self.nome_aliado = nome_aliado.replace(" ", "_").lower()
        self.nome_aliado_exibir = nome_aliado
        self.item_especial = "FlorMedicinal"
        self.jogador_com_item_especial = False
        self.jogador_entregou_item_especial = False
        self.interacao = "F: Falar com "

    def desenha(self):
        self.sprite.draw()

    def inteligencia_artificial(self, janela, sprite_atual, jogador):
        # Atribuições
        personagem = self.sprite
        teclado = Keyboard()

        # Calcular as coordenadas do centro do jogador e inimigo
        inimigo_x = personagem.x + personagem.width / 2
        inimigo_y = personagem.y + personagem.height / 2
        jogador_x = sprite_atual.x + sprite_atual.width / 2
        jogador_y = sprite_atual.y + sprite_atual.height / 2

        # Equação do círculo
        equacao_circulo = (jogador_x - inimigo_x) ** 2 + (jogador_y - inimigo_y) ** 2

        if equacao_circulo <= self.raio_de_conversa ** 2:
            if teclado.key_pressed("F"):
                indice_item_especial = jogador.inventario.verifica_item(self.item_especial)
                if indice_item_especial is not False:
                    self.jogador_com_item_especial = True
                    jogador.inventario.inventario.pop(indice_item_especial)
                    self.fala = 0
                self.conversa(janela, sprite_atual)
            else:
                janela.draw_text(self.interacao + self.nome_aliado_exibir,
                                 sprite_atual.x - (260 / self.F_R), sprite_atual.y + (100 / self.F_R),
                                 int(20 / self.F_R), (12, 34, 110), "Arial", True, True)

    def conversa(self, janela, sprite_jogador):
        # Atribuições
        Falas = FalasPersonagens()
        conversar = True
        mouse = Mouse()
        # Seleciona a lista de falas
        frase_proxima_mensagem = GameImage("Imagens/" + InformacoesBase.resolucao + "proxima_mensagem.png")
        if self.jogador_com_item_especial:
            falas = getattr(Falas, self.nome_aliado + "_item_especial")
            if self.fala == len(falas) - 1:
                self.jogador_com_item_especial = False
                self.jogador_entregou_item_especial = True
        elif self.jogador_entregou_item_especial is False:
            falas = getattr(Falas, self.nome_aliado)
        else:
            falas = getattr(Falas, self.nome_aliado + "_depois_item_especial")
            InformacoesBase.terminou_jogo = True
        fala = self.fala

        # Loop de Falas
        while conversar:
            # Desenha a fala
            fala_atual = GameImage(falas[fala])
            frase_proxima_mensagem.draw()
            fala_atual.draw()
            # Atualiza as falas e sai do diálogo
            if Keyboard().key_pressed("SPACE"):
                conversar = False
                fala += 1
                self.fala = fala % (len(falas))
            sprite_jogador.draw()
            janela.update()
