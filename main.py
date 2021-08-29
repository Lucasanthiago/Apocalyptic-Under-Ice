from Classes.Personagens import Personagem
from Classes.VariaveisGerais import InformacoesBase
from Classes.Cenarios import *
from PPlay.sprite import *
from Classes.UserInterface import *
from Classes.Inventario import *

# Inicialização
janela = InformacoesBase.janela
teclado = Keyboard()

# Inventário
inventario = Inventario(janela)

# Cenarios
cenario_0 = Cenario0()
cenario_1 = Cenario1()
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

# Barra de Vida
barra_de_vida = BarraVida(jogador, janela)

# Game Loop
while True:
    ################### Entrada de Dados ######################

    ################### Updates ###############################
    cenario_atual = eval(cenario_atual.proxima_fase(sprite_jogador))
    itens_cenario_atual = cenario_atual.itens


    ################### Game Physics ##########################

    # Fisica jogador
    jogador.fisica(janela, sprite_jogador)
    # Colisões cenário
    cenario_atual.colisoes_cenario(sprite_jogador)

    ################### Desenho ###############################

    cenario_atual.fundo.draw()

    for i in range(len(itens_cenario_atual)):
        item = itens_cenario_atual[i]
        item.desenha()
        if item.verifica_proximo(sprite_jogador):
            janela.draw_text("F: Pegar " + item.__class__.__name__,
                             sprite_jogador.x - 200, sprite_jogador.y + 100, 20, (160, 82, 45), "Arial", True, True)
            if teclado.key_pressed("F"):
                inventario.adiciona_no_inventario(item)
                itens_cenario_atual.pop(i)

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

    barra_de_vida.update()
    if teclado.key_pressed("I"):
        inventario.mostra_inventario()
    janela.update()
    # Encerramento
