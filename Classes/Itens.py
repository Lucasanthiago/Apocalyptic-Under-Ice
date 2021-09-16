from PPlay.sound import *
from Classes.Personagens import *
from PPlay.mouse import *
from Classes.Tiro import *
import math


class Pistola:
    def __init__(self):
        F_R = InformacoesBase.fator_redimensionamento
        self.F_R = F_R
        self.imagem = GameImage("Imagens/" + InformacoesBase.resolucao + "pistola.png")
        self.imagem_escalada = GameImage("Imagens/" + InformacoesBase.resolucao + "pistola_escalada.png")
        self.imagem.x = (1215 / F_R)
        self.imagem.y = (593 / F_R)
        self.dano = 15
        self.raio_proximo = (100 / F_R)
        self.tempo_recarga = 0.3
        self.cronometro = 0
        self.som_tiro = pygame.mixer.Sound("Sons/tiro_arma.ogg")
        self.som_tiro.set_volume(0.3)
        self.nome = "Pistola"
        self.interacao = "F: Pegar "

    def desenha(self):
        self.imagem.draw()

    def desenha_imagem_escalada(self):
        self.imagem_escalada.draw()

    def verifica_proximo(self, sprite_jogador, janela):
        jogador_x = sprite_jogador.x + sprite_jogador.width / 2
        jogador_y = sprite_jogador.y + sprite_jogador.height
        arma_x = self.imagem.x + self.imagem.width / 2
        arma_y = self.imagem.y + self.imagem.height / 2

        equacao_circulo = (jogador_x - arma_x) ** 2 + (jogador_y - arma_y) ** 2
        if equacao_circulo <= self.raio_proximo ** 2:
            janela.draw_text(self.interacao + self.nome,
                             sprite_jogador.x - (200 / self.F_R), sprite_jogador.y + (100 / self.F_R),
                             int(20 / self.F_R), (100, 0, 255), "Arial", True, True)
            return True
        return False

    def atira(self, janela, sprite_jogador, matriz_tiros):
        mouse = Mouse()
        self.cronometro += janela.delta_time()

        if self.cronometro >= self.tempo_recarga and mouse.is_button_pressed(1):
            coord_mouse = mouse.get_position()
            coord_arma = (sprite_jogador.x + (10 / self.F_R), sprite_jogador.y + sprite_jogador.height / 2 -
                          (50 / self.F_R))
            # Distancias
            x = math.fabs(coord_arma[0] - coord_mouse[0])
            y = math.fabs(coord_arma[1] - coord_mouse[1])
            # Elimina o erro de quando o x for 0
            try:
                angulo_jogador_inimigo = math.atan(y / x)
            except ZeroDivisionError:
                angulo_jogador_inimigo = 0
            # Calcula os incrementos
            incremento_y = math.sin(angulo_jogador_inimigo)
            incremento_x = math.cos(angulo_jogador_inimigo)
            # Calculando a direção em que deve-se ir
            multi_x = 1
            multi_y = 1

            if coord_mouse[0] < coord_arma[0]:
                multi_x = -1
            if coord_mouse[1] <= coord_arma[1]:
                multi_y = -1

            # Incrementando
            incremento_x = incremento_x * janela.delta_time() * multi_x
            incremento_y = incremento_y * janela.delta_time() * multi_y
            tiro = Tiro((incremento_x, incremento_y), self.dano, sprite_jogador)
            matriz_tiros.append(tiro)
            self.som_tiro.stop()
            self.som_tiro.play()
            self.cronometro = 0


class FlorMedicinal(Pistola):
    def __init__(self):
        super().__init__()
        self.imagem_escalada = GameImage("Imagens/" + InformacoesBase.resolucao + "Flor_escalada.png")
        self.imagem = GameImage("Imagens/" + InformacoesBase.resolucao + "Flor_escalada.png")
        self.imagem.x = (1810 / self.F_R)
        self.imagem.y = (597 / self.F_R)
        self.raio_proximo = (70 / self.F_R)
        self.som_tiro = None
        self.nome = "Flor Medicinal"

    def atira(self, janela, sprite_jogador, matriz_tiros):
        return None


class ItemVida(FlorMedicinal):
    def __init__(self):
        super().__init__()
        self.imagem_escalada = GameImage("Imagens/" + InformacoesBase.resolucao + "item_vida.png")
        self.imagem = GameImage("Imagens/" + InformacoesBase.resolucao + "item_vida.png")
        self.imagem.x = (50 / self.F_R)
        self.imagem.y = (700 / self.F_R)
        self.raio_proximo = (70 / self.F_R)
        self.som_tiro = None
        self.quantia = 3
        self.nome = "Item de Vida"
        self.som = pygame.mixer.Sound("Sons/recuperar_vida.flac")
