from PPlay.gameimage import *
from PPlay.keyboard import *
from PPlay.mouse import *


class Inventario:
    def __init__(self, janela):
        # Atribuições
        self.cronometro = 0
        self.inventario = [0] * 9
        self.imagem_inventario = GameImage("Imagens/inv.png")
        self.janela = janela

        # Posição do Inventario
        self.imagem_inventario.x = self.janela.width / 2 - self.imagem_inventario.width / 2
        self.imagem_inventario.y = self.janela.height / 2 - self.imagem_inventario.height / 2
        # Dados do Slot
        self.largura_slot = self.imagem_inventario.width / 3
        # Posição dos Itens
        self.posicoes_item = []
        self.adiciona_coordenadas_itens(self.posicoes_item)

    def adiciona_coordenadas_itens(self, posicoes_item):
        g = 0
        inicio_y = self.imagem_inventario.y - self.largura_slot
        for i in range(len(self.inventario) // 3):
            incremento = self.largura_slot
            inicio_x = self.imagem_inventario.x
            inicio_y += incremento
            for j in range(len(self.inventario) // 3):
                posicoes_item.append([[inicio_x, inicio_y], [inicio_x + incremento, inicio_y + incremento]])
                inicio_x += incremento
                g += 1

    def mostra_lista_inventario(self):
        return self.inventario

    def adiciona_no_inventario(self, item):
        # Procura espaço vazio no inventario
        try:
            ind = self.inventario.index(0)
        except ValueError:
            ind = "Sem Espaço"
            print(ind)
        # Se existir, adiciona o item nele
        if ind != "Sem Espaço":
            self.inventario[ind] = item

    def retira_do_inventario(self, item):
        # Procura as coordenadas do item no inventário
        try:
            ind = self.inventario.index(item)
        except ValueError:
            ind = False
            print("Item não encontrado")
        # Se achar o item, transforma o espaço dele em espaço vazio
        if not ind:
            self.inventario[ind] = 0

    def mostra_inventario(self):
        # Atribuições
        teclado = Keyboard()
        # Loop do Inventario
        while not teclado.key_pressed("Q"):
            # Desenhos
            self.imagem_inventario.draw()
            # Desenha os itens do inventário
            for i in range(len(self.inventario)):
                if self.inventario[i] != 0:
                    self.inventario[i].imagem.x = self.posicoes_item[i][0][0] + 17
                    self.inventario[i].imagem.y = self.posicoes_item[i][0][1] + 17
                    self.inventario[i].desenha()
            # Updates
            self.janela.update()


class Bola:
    def __init__(self):
        self.imagem_bola = GameImage("Imagens/Bola.png")
