import pygame.mixer
from Classes.Personagens import *
from Classes.VariaveisGerais import InformacoesBase
from Classes.Cenarios import *
from Classes.Tiro import *
from Classes.UserInterface import *
from Classes.Inventario import *
from PPlay.collision import Collision

# Inicialização
janela = InformacoesBase.janela
teclado = Keyboard()
escolhe_resolucao = TelaResolucao()
escolhe_resolucao.tela(janela)
janela = InformacoesBase.janela
InformacoesBase.fator_redimensionamento = InformacoesBase.resolucao_base[0] / janela.width
F_R = InformacoesBase.fator_redimensionamento

# Inventário
inventario = Inventario(janela)
tecla_solta = True

# Cenarios
menu_principal = MenuPrincipal("Imagens/" + InformacoesBase.resolucao + "Cenario_2.png", "cenario_0")
cenario_atual = menu_principal

# Jogador
jogador = Personagem()
ultimo_mov_D = True
sprite_jogador = jogador.sprite
sprite_jogador.y = (400 / F_R)
pode_recuperar_vida = True
quantia_vida = 0

# Sons
musica_atual = None
musica_trocada = True
TEMPO_PASSOS = (jogador.tempo_animacao / 100) / 2.8
cronometro_passos = 0

# Inimigos
inimigos = []

# Aliados
aliados = []

# Arma
matriz_tiros = []

# Barra de Vida
barra_de_vida = BarraVida(jogador, janela)

# Troca de cenarios
TEMPO_SEGURANCA_TROCA_CENARIO = 0.05
cronometro_troca_cenario = 0

# Game Loop
while True:
    ################### Entrada de Dados ######################

    # Reseta o jogo quando começa um novo
    if cenario_atual == menu_principal:
        # Toca musica do menu principal
        pygame.mixer.music.load("Sons/musica_menu_principal.ogg")
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(-1)
        # Mostra o menu principal
        menu_principal.tela(janela)
        # Inicializa os cenários
        prologo = TelaPrologo("Imagens/" + InformacoesBase.resolucao + "prologo1.png")
        prologo_2 = TelaPrologo("Imagens/" + InformacoesBase.resolucao + "prologo2.png")
        manual = TelaPrologo("Imagens/" + InformacoesBase.resolucao + "manual.png")
        cenario_0 = Cenario0()
        cenario_1 = Cenario1()
        cenario_2 = Cenario2()
        cenario_atual = cenario_0
        # inicializa o som dos passos
        InformacoesBase.trocando_cenario = True
        # som_passos = pygame.mixer.Sound(cenario_atual.som_passos)
        # Mostra o prologo
        prologo.tela(janela)
        prologo_2.tela(janela)
        manual.tela(janela)

    sprite_jogador = jogador.sprite
    cenario_atual = eval(cenario_atual.proxima_fase(jogador, inimigos))
    itens_cenario_atual = cenario_atual.itens
    inimigos = cenario_atual.inimigos
    inimigos_na_frente = []
    aliados_na_frente = []

    # Aliados
    aliados = cenario_atual.aliados

    if cenario_atual.inicializando:
        cenario_atual.adiciona_lista_de_colisoes_anteriores(jogador)
        cenario_atual.inicializando = False
    ################### Updates ###############################

    if InformacoesBase.morreu:
        InformacoesBase.morreu = False
        Menu("Imagens/" + InformacoesBase.resolucao + "Tela_de_morte.png", "menu_principal").tela(janela)
        cenario_atual = menu_principal
        continue

    if InformacoesBase.terminou_jogo:
        InformacoesBase.terminou_jogo = False
        Menu("Imagens/" + InformacoesBase.resolucao + "epilogo.png", "menu_principal").tela(janela)
        cenario_atual = menu_principal
        continue

    print(sprite_jogador.y)
    if InformacoesBase.trocando_cenario or musica_atual is None:
        musica_atual = cenario_atual.som_cenario
        pygame.mixer.music.load(musica_atual)
        som_passos = pygame.mixer.Sound(cenario_atual.som_passos)
        som_passos.set_volume(cenario_atual.volume_passos)
        pygame.mixer.music.set_volume(cenario_atual.volume_som_cenario)
        pygame.mixer.music.play(-1, fade_ms=1000)
        musica_trocada = False

    if cronometro_passos >= TEMPO_PASSOS and (jogador.movendo_baixo or jogador.movendo_cima or jogador.movendo_direita
                                              or jogador.movendo_esquerda):
        som_passos.play()
        cronometro_passos = 0

    cronometro_passos += janela.delta_time()

    if len(inimigos) == 0 and cenario_atual.ordas_inimigos > 0:
        cenario_atual.cria_inimigos()
        cenario_atual.ordas_inimigos -= 1

    jogador.inventario = inventario
    jogador.troca_sprite_armas()

    if not teclado.key_pressed("I"):
        tecla_solta = True

    # Recuperação de Vida
    pos_item_vida = inventario.verifica_item("ItemVida")
    if pos_item_vida is not False:
        quantia_vida = inventario.inventario[pos_item_vida].quantia
        if teclado.key_pressed("Q") and pode_recuperar_vida:
            pode_recuperar_vida = False
            jogador.vida = jogador.vida_maxima
            inventario.inventario[pos_item_vida].quantia -= 1
            inventario.inventario[pos_item_vida].som.play()
            if inventario.inventario[pos_item_vida].quantia == 0:
                inventario.retira_do_inventario(pos_item_vida)
        elif not teclado.key_pressed("Q"):
            pode_recuperar_vida = True
    else:
        quantia_vida = 0

    ################### Game Physics ##########################

    # Fisica jogador
    if not InformacoesBase.trocando_cenario:
        jogador.fisica(janela, sprite_jogador)
    else:
        matriz_tiros = []
        while not cronometro_troca_cenario >= TEMPO_SEGURANCA_TROCA_CENARIO:
            cronometro_troca_cenario += janela.delta_time()
        cenario_atual.adiciona_lista_de_colisoes_anteriores(jogador)
        if cenario_atual == cenario_1 and inventario.verifica_item("FlorMedicinal") is not False:
            cenario_atual.cria_chefao()
            cenario_atual.chefao_criado = True
        InformacoesBase.trocando_cenario = False
        cronometro_troca_cenario = 0

    # Colisões cenário
    cenario_atual.colisoes_cenario(jogador)

    item_equipado = inventario.inventario[jogador.slot_equipado - 1]

    if item_equipado.__class__.__name__ == "Pistola":
        item_equipado.atira(janela, sprite_jogador, matriz_tiros)

    # Fisica Inimigos
    for i in range(len(inimigos)):
        inimigos[i].inteligencia_artificial(janela, jogador)
        cenario_atual.colisoes_cenario(inimigos[i])

    # Fisica Tiros
    for i in range(len(matriz_tiros)):
        tiro = matriz_tiros[i]
        tiro.movimenta_tiro()
        tiro.imagem.draw()
        tiro_sumir = False
        for j in range(len(inimigos)):
            inimigo_atual = inimigos[j]
            if Collision.collided(tiro.imagem, inimigo_atual.sprite):
                inimigo_atual.recebe_dano(tiro.dano)
                inimigo_atual.tomou_dano = True
                tiro_sumir = True
                if inimigo_atual.vida <= 0:
                    inimigo_atual.som_morte.play()
                    inimigos.pop(j)
                break
        if tiro.imagem.x > janela.width or tiro.imagem.x < 0 or tiro.imagem.y > janela.height or tiro.imagem.y < 0 \
                or tiro_sumir:
            matriz_tiros.pop(i)
            break

    ################### Desenho ###############################

    cenario_atual.fundo.draw()

    # Desenha os itens e o texto para adicionar eles
    for i in range(len(itens_cenario_atual)):
        item = itens_cenario_atual[i]
        item.desenha()
        if item.verifica_proximo(sprite_jogador, janela) and teclado.key_pressed("F"):
            if inventario.adiciona_no_inventario(item) is not False:
                itens_cenario_atual.pop(i)
            else:
                janela.draw_text("Inventário Cheio",
                                 janela.width / 2, janela.height * 2 / 3, int(40 / F_R), (0, 255, 105), "Arial", True,
                                 True)
            break

    # Escolhe o sprite do jogador
    sprite_correndo = jogador.troca_sprite()

    # Escolhe e desenha o sprite dos inimigos atrás
    for i in range(len(inimigos)):
        sprite_inimigo = inimigos[i].troca_sprite()
        if sprite_inimigo[0].y < sprite_correndo[0].y:
            sprite_inimigo[0].draw()
            if sprite_inimigo[1]:
                sprite_inimigo[0].update()
        else:
            inimigos_na_frente.append(i)

    # Desenha aliados e lida com suas falas
    for aliado in aliados:
        if aliado.sprite.y < sprite_correndo[0].y:
            aliado.desenha()
            aliado.inteligencia_artificial(janela, sprite_correndo[0], jogador)
        else:
            aliados_na_frente.append(aliado)
    # Desenha os tiros
    for i in range(len(matriz_tiros)):
        matriz_tiros[i].imagem.draw()

    # Desenha o jogador
    sprite_correndo[0].draw()
    if sprite_correndo[1]:
        sprite_correndo[0].update()

    for aliado in aliados_na_frente:
        aliado.desenha()
        aliado.inteligencia_artificial(janela, sprite_correndo[0], jogador)

    # Desenha os inimigos a frente
    for num in range(len(inimigos_na_frente)):
        sprite_inimigo = inimigos[inimigos_na_frente[num]].troca_sprite()
        sprite_inimigo[0].draw()
        if sprite_inimigo[1]:
            sprite_inimigo[0].update()

    # Atualiza e desenha a barra de vida
    barra_de_vida.update(jogador)

    # Desenha a quantia de vidas
    if quantia_vida > 0:
        janela.draw_text("Itens de vida: " + str(quantia_vida),
                         janela.width - (350 / F_R), (10 / F_R), int(40 / F_R), (0, 255, 105), "Arial", True, True)

    # Desenha o inventário
    if teclado.key_pressed("I") and tecla_solta:
        tecla_solta = False
        inventario.mostra_inventario()

    janela.update()
    # Encerramento
