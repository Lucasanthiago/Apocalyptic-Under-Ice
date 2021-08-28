from Classes.Personagens import Personagem
from Classes.VariaveisGerais import InformacoesBase
from Classes.Cenarios import *
from PPlay.sprite import *

# Inicialização
janela = InformacoesBase.janela
# Cenarios
cenario_0 = Cenario0()
cenario_atual = cenario_0

# Jogador
jogador = Personagem()
sprite_jogador = Sprite("Imagens/personagem-parado.png", 1)
sprite_jogador_E = Sprite("Imagens/personagem-parado-E.png", 1)
sprite_jogador_correndo_D = Sprite("Imagens/personagem-correndo-direita.png", 6)
sprite_jogador_correndo_D.set_sequence_time(0, 6, 120, True)
sprite_jogador_correndo_E = Sprite("Imagens/personagem-correndo-esquerda.png", 6)
sprite_jogador_correndo_E.set_sequence_time(0, 6, 120, True)
ultimo_mov_D = True

sprite_jogador.y = 400
# Game Loop
while True:
    ################### Entrada de Dados ######################

    ################### Updates ###############################

    ################### Game Physics ##########################

    # Fisica jogador
    jogador.fisica(janela, sprite_jogador)
    # Colisões cenário
    cenario_atual.colisoes_cenario(sprite_jogador)

    ################### Desenho ###############################

    cenario_atual.fundo.draw()

    # Cuida de qual sprite vai ser desenhado
    if InformacoesBase.movendo_direita:
        sprite_jogador_correndo_D.x = sprite_jogador.x - sprite_jogador.width
        sprite_jogador_correndo_D.y = sprite_jogador.y
        sprite_jogador_correndo_D.draw()
        sprite_jogador_correndo_D.update()
        ultimo_mov_D = True
    elif InformacoesBase.movendo_esquerda:
        sprite_jogador_correndo_E.x = sprite_jogador.x - 5
        sprite_jogador_correndo_E.y = sprite_jogador.y
        sprite_jogador_correndo_E.draw()
        sprite_jogador_correndo_E.update()
        ultimo_mov_D = False
    else:
        if InformacoesBase.movendo_cima or InformacoesBase.movendo_baixo:
            if ultimo_mov_D:
                sprite_jogador_correndo_D.x = sprite_jogador.x - sprite_jogador.width
                sprite_jogador_correndo_D.y = sprite_jogador.y
                sprite_jogador_correndo_D.draw()
                sprite_jogador_correndo_D.update()
            else:
                sprite_jogador_correndo_E.x = sprite_jogador.x - 5
                sprite_jogador_correndo_E.y = sprite_jogador.y
                sprite_jogador_correndo_E.draw()
                sprite_jogador_correndo_E.update()
        elif ultimo_mov_D:
            sprite_jogador.draw()
        else:
            sprite_jogador_E.x = sprite_jogador.x
            sprite_jogador_E.y = sprite_jogador.y
            sprite_jogador_E.draw()

    janela.update()
    # Encerramento
