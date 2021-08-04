from Classes.Personagens import *
from Classes.VariaveisGerais import InformacoesBase
from PPlay.gameimage import *

# Inicialização
janela = InformacoesBase.janela
fundo = GameImage("Imagens/FundoMenuPrincipal.png")

# Personagem Principal
personagem_principal = Personagem("Imagens/teste.png")
sprite_personagem_principal = personagem_principal.sprite()
velocidade_personagem_principal = personagem_principal.velocidade

# Inimigo
inimigo = Inimigos("Imagens/teste.png")
sprite_inimigo = inimigo.sprite()

sprite_inimigo.x = 200
sprite_inimigo.y = 200

# Game Loop
while True:
    # Entrada de Dados

    # Updates

    # Game Physics

    # Física do personagem em relação ao mapa
    personagem_principal.fisica(janela, fundo)
    inimigo.fisica_inimigo(janela, fundo, sprite_personagem_principal, velocidade_personagem_principal)
    inimigo.inteligencia_artificial(janela, sprite_personagem_principal)

    # Desenho
    fundo.draw()
    sprite_personagem_principal.draw()
    sprite_personagem_principal.update()
    sprite_inimigo.draw()

    janela.update()

    # Encerramento
