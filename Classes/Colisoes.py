""" Verifica se houve colisão com um retângulo, e se não houve, ele mostra os lados em que o player esta
    dentro da area de colisao """


def colisao_retangulo(sprite_jogador, retangulo, atras):
    if atras:
        sprite_jogador_y = sprite_jogador.y + sprite_jogador.height - 20
    else:
        sprite_jogador_y = sprite_jogador.y
    # Inicializações
    colisao_cima = False
    colisao_baixo = False
    colisao_direita = False
    colisao_esquerda = False
    colisoes_verdadeiras = [False, False, False, False]
    # Checagem das colisões
    if retangulo[0] - sprite_jogador.width < sprite_jogador.x:
        colisao_esquerda = True
    if sprite_jogador.x < retangulo[2]:
        colisao_direita = True
    if retangulo[1] - sprite_jogador.height < sprite_jogador.y:
        colisao_cima = True
    if sprite_jogador_y < retangulo[3]:
        colisao_baixo = True

    if colisao_cima and colisao_baixo and colisao_direita and colisao_esquerda:
        return True
    else:
        colisoes_verdadeiras[0] = colisao_esquerda
        colisoes_verdadeiras[1] = colisao_cima
        colisoes_verdadeiras[2] = colisao_direita
        colisoes_verdadeiras[3] = colisao_baixo
        return colisoes_verdadeiras
