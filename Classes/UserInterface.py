import pygame.draw
from Classes.VariaveisGerais import *


class BarraVida:
    def __init__(self, jogador, janela):
        self.F_R = InformacoesBase.fator_redimensionamento
        self.vida = jogador.vida
        self.vida_maxima = jogador.vida_maxima
        self.largura_maxima = (250 / self.F_R)
        self.taxa_da_vida = self.vida_maxima / self.largura_maxima
        self.janela = janela
        self.tela = pygame.display.set_mode((janela.width, janela.height))

    def adiciona_vida(self, quantia):
        self.vida += quantia

    def retira_vida(self, quantia):
        self.vida -= quantia

    def update(self, jogador):
        self.vida = jogador.vida
        taxa_vida_barra = self.vida / self.taxa_da_vida
        if taxa_vida_barra < 0:
            taxa_vida_barra = 0
        self.janela.draw_text("+", (20 / self.F_R), (0 / self.F_R), int(70 / self.F_R), (173, 255, 47), "Arial",
                                                    True, False)
        pygame.draw.rect(self.tela, (34, 139, 34), ((75 / self.F_R), (24 / self.F_R), self.largura_maxima +
                                                    (10 / self.F_R), (30 / self.F_R)))
        pygame.draw.rect(self.tela, (173, round(taxa_vida_barra), 47), ((80 / self.F_R),
                                                    (29 / self.F_R), taxa_vida_barra, (20 / self.F_R)))
