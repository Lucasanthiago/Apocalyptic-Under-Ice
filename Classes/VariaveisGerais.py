from PPlay.window import *


class InformacoesBase:
    resolucao_base = (1920, 1080)
    janela = Window(1280, 720)
    fator_redimensionamento = resolucao_base[0] / janela.width
    resolucao = "1080P/"
    morreu = False
    trocando_cenario = False
    terminou_jogo = False
