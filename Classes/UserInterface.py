import pygame.draw


class BarraVida:
    def __init__(self, jogador, janela):
        self.vida = jogador.vida
        self.vida_maxima = jogador.vida_maxima
        self.largura_maxima = 250
        self.taxa_da_vida = self.vida_maxima / self.largura_maxima
        self.janela = janela
        self.tela = pygame.display.set_mode((janela.width, janela.height))

    def adiciona_vida(self, quantia):
        self.vida += quantia

    def retira_vida(self, quantia):
        self.vida -= quantia

    def update(self, jogador):
        self.vida = jogador.vida
        taxa_vida_barra = self.vida/self.taxa_da_vida
        if taxa_vida_barra < 0:
            taxa_vida_barra = 0
        self.janela.draw_text("+", 20, 0, 70, (173, 255, 47), "Arial", True, False)
        pygame.draw.rect(self.tela, (34, 139, 34), (75, 24, self.largura_maxima + 10, 30))
        pygame.draw.rect(self.tela, (173, round(taxa_vida_barra), 47), (80, 29, taxa_vida_barra, 20))
