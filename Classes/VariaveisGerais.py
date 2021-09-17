from Classes.Janela import *


class InformacoesBase:
    resolucao_base = (1920, 1080)
    janela = Janela(1280, 720)
    janela.set_title("Apocalypse Under Ice")
    fator_redimensionamento = resolucao_base[0] / janela.width
    resolucao = "1080P/"
    morreu = False
    trocando_cenario = False
    terminou_jogo = False
