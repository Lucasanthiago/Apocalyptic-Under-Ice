from Classes.Personagens import *
from Classes.VariaveisGerais import InformacoesBase
from Classes.Inventario import *
from PPlay.gameimage import *

# Inicialização
janela = InformacoesBase.janela
fundo = GameImage("Imagens/FundoMenuPrincipal.png")

# Personagem Principal
jogador = Personagem("Imagens/teste.png", janela, fundo)
sprite_jogador = jogador.sprite()
velocidade_jogador = jogador.velocidade

# Inimigo
inimigo = Inimigos("Imagens/teste.png", janela, fundo, sprite_jogador, velocidade_jogador)
sprite_inimigo = inimigo.sprite()

# Aliado
aliado = Aliados("Imagens/teste.png", janela, fundo, sprite_jogador, velocidade_jogador, "FalaTeste")
sprite_aliado = aliado.sprite()

# Inventario
inventario = Inventario(janela)
bola = Bola()


sprite_inimigo.x = 200
sprite_inimigo.y = 200

sprite_aliado.x = 400
sprite_aliado.y = 400

# Game Loop
while True:
    # Entrada de Dados

    # Updates

    aliado.inteligencia_artificial()
    if Keyboard().key_pressed("K"):
        inventario.adiciona_no_inventario(bola.imagem_bola)

    if Keyboard().key_pressed("I"):
        # Game Physics
        inventario.mostra_inventario()

    # Física do personagem em relação ao mapa
    jogador.fisica()
    inimigo.fisica_outros()
    inimigo.inteligencia_artificial()
    aliado.fisica_outros()

    # Desenho
    fundo.draw()
    sprite_jogador.draw()
    sprite_jogador.update()
    sprite_inimigo.draw()
    sprite_aliado.draw()
    janela.update()

    # Encerramento
