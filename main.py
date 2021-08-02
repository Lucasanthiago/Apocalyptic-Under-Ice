from Classes.Personagens import *
from Classes.VariaveisGerais import InformacoesBase
from PPlay.gameimage import *


# Inicialização
janela = InformacoesBase.janela
fundo = GameImage("Imagens/FundoMenuPrincipal.png")

personagem_principal = PersonagemPrincipal()
sprite_personagem_principal = personagem_principal.sprite_personagem_principal("Imagens/teste.png")
velocidade_personagem_principal = personagem_principal.velocidade

# Game Loop
while True:
    # Entrada de Dados

    # Updates

    # Game Physics

    # Física do personagem em relação ao mapa
    fisica_personagens(sprite_personagem_principal, janela, fundo, velocidade_personagem_principal)

    # Desenho
    fundo.draw()
    sprite_personagem_principal.draw()
    sprite_personagem_principal.update()
    janela.update()

    # Encerramento
