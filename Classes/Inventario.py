from Classes.VariaveisGerais import *
from PPlay.gameimage import *
from PPlay.keyboard import *
from PPlay.mouse import *


class Inventario:
    def __init__(self, janela):
        # Atribuições
        self.cronometro = 0
        self.inventario = [0] * 3
        self.imagem_inventario = GameImage("Imagens/" + InformacoesBase.resolucao + "inv.png")
        self.janela = janela
        F_R = InformacoesBase.fator_redimensionamento
        self.F_R = F_R
        # Dados do Slot
        self.largura_slot = (160 / F_R)
        self.pos_x_0 = self.janela.width / 2 - self.largura_slot - self.largura_slot / 2
        self.pos_y_0 = self.janela.height / 2 - self.largura_slot - self.largura_slot / 2

        # Posição dos Itens
        self.posicoes_item = []
        self.preenche_posicoes_inventario()
        self.alterou_inventario = False

        # Sons
        self.som_adicionando = pygame.mixer.Sound("Sons/adiciona_inventario.wav")
        self.som_retirando = pygame.mixer.Sound("Sons/retira_inventario.wav")
        self.som_adicionando.set_volume(0.9)
        self.som_retirando.set_volume(0.6)

    def preenche_posicoes_inventario(self):
        self.posicoes_item = [
            [self.pos_x_0, self.pos_y_0 + self.largura_slot],
            [self.pos_x_0 + self.largura_slot, self.pos_y_0 + self.largura_slot],
            [self.pos_x_0 + self.largura_slot * 2, self.pos_y_0 + self.largura_slot]
        ]

    def lista_inventario(self):
        return self.inventario

    def adiciona_no_inventario(self, item):
        # Procura espaço vazio no inventario
        try:
            ind = self.inventario.index(0)
        except ValueError:
            ind = "Sem Espaço"
            return False
        # Se existir, adiciona o item nele
        if ind != "Sem Espaço":
            self.som_adicionando.play()
            self.inventario[ind] = item
        self.alterou_inventario = True

    def retira_do_inventario(self, indice):
        self.inventario[indice] = 0
        self.alterou_inventario = True
        self.som_retirando.play()

    def mostra_inventario(self):
        # Atribuições
        teclado = Keyboard()
        mouse = Mouse()
        tecla_solta = False
        movendo_item = False
        nova_pos = None

        lixeira = GameImage("Imagens/" + InformacoesBase.resolucao + "Lixeira.png")
        lixeira.x = (960 / self.F_R) - lixeira.width / 2
        lixeira.y = (930 / self.F_R) - lixeira.height / 2

        # Loop do Inventario
        while (not teclado.key_pressed("ESC") and not teclado.key_pressed("I")) or (not tecla_solta):
            # Updates
            if not teclado.key_pressed("I"):
                tecla_solta = True
            botao_pressionado = mouse.is_button_pressed(1)
            pos_mouse = mouse.get_position()
            # Desenhos
            self.imagem_inventario.draw()
            # Desenha os itens do inventário
            for i in range(len(self.inventario)):
                if self.inventario[i] != 0:
                    pos_mouse = mouse.get_position()
                    clique_botao_1 = mouse.is_button_pressed(1)
                    imagem_item = self.inventario[i].imagem_escalada

                    self.inventario[i].imagem_escalada.x = self.posicoes_item[i][0] + self.largura_slot / 2 \
                                                           - imagem_item.width / 2
                    self.inventario[i].imagem_escalada.y = self.posicoes_item[i][1] + self.largura_slot / 2 \
                                                           - imagem_item.height / 2
                    self.inventario[i].desenha_imagem_escalada()

            if botao_pressionado:
                item_selecionado = self.posicao_mouse(pos_mouse)
                if item_selecionado is not None and self.inventario[item_selecionado] != 0:
                    pegoudif = False
                    while botao_pressionado and item_selecionado is not None:
                        # Desenha o Inventário e lixeira
                        self.imagem_inventario.draw()
                        lixeira.draw()
                        # Atribuições
                        pos_mouse = mouse.get_position()
                        botao_pressionado = mouse.is_button_pressed(1)
                        item_atual = self.posicao_mouse(pos_mouse)

                        # Faz o item "andar" com o mouse
                        if not pegoudif:
                            dif_x = self.inventario[item_selecionado].imagem_escalada.x - pos_mouse[0]
                            dif_y = self.inventario[item_selecionado].imagem_escalada.y - pos_mouse[1]
                            pegoudif = True

                        self.inventario[item_selecionado].imagem_escalada.x = pos_mouse[0] + dif_x
                        self.inventario[item_selecionado].imagem_escalada.y = pos_mouse[1] + dif_y
                        # Desenha os os itens do inventário
                        for i in range(len(self.inventario)):
                            if self.inventario[i] != 0:
                                self.inventario[i].desenha_imagem_escalada()
                        # Exclui os itens do inventário, se o jogador quiser
                        if (lixeira.collided(self.inventario[item_selecionado].imagem_escalada)) \
                                and not botao_pressionado:
                            self.retira_do_inventario(item_selecionado)
                            break

                        # Troca o item selecionado de lugar, se não tiver nenhum item no novo local
                        if item_atual != item_selecionado and not botao_pressionado and item_atual is not None:
                            if self.inventario[item_atual] == 0:
                                self.inventario[item_atual] = self.inventario[item_selecionado]
                                self.retira_do_inventario(item_selecionado)
                            elif self.inventario[item_atual] is not None:
                                item_no_slot = self.inventario[item_atual]
                                self.inventario[item_atual] = self.inventario[item_selecionado]
                                self.retira_do_inventario(item_selecionado)
                                self.inventario[item_selecionado] = item_no_slot
                            break

                        # Atualiza a janela

                        self.janela.update()
            # Updates
            lixeira.draw()
            self.janela.update()

    def posicao_mouse(self, pos_mouse):
        novo_indice = None
        for i in range(len(self.posicoes_item)):
            if self.posicoes_item[i][0] <= pos_mouse[0] < self.posicoes_item[i][0] + self.largura_slot \
                    and self.posicoes_item[i][1] <= pos_mouse[1] < self.posicoes_item[i][1] + self.largura_slot:
                novo_indice = i
        return novo_indice

    def move_item(self, indice, botao_pressionado, pos_mouse):
        while botao_pressionado:
            self.inventario[indice].imagem.x = pos_mouse[0] - (15 / self.F_R)
            self.inventario[indice].imagem.y = pos_mouse[1] - (15 / self.F_R)

            self.inventario[indice].desenha()
            self.janela.update()

    def verifica_item(self, nome_item):
        for i in range(len(self.inventario)):
            if self.inventario[i].__class__.__name__ == nome_item:
                return i
        return False
