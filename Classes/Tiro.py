from PPlay.gameimage import *
from PPlay.sprite import *

class Tiro:
    class Tiro():
        def __init__(self):
            self.tiros = []

        def add_shot(self, jogador):
            tiro = Sprite("Imagens/Bola.jpg")
            print(tiro.width)
            tiro.set_position(jogador.x + jogador.width / 2, jogador.y - tiro.height)
            self.tiros.append(tiro)

        def draw_shots(self):
            for i in range(len(self.tiros)):
                self.tiros[i].draw()

        def update(self, janela):
            variacao = 0
            for shot in self.tiros:
                shot.x = shot.x + 300 * janela.delta_time()
                if shot.x <= 0 - shot.width:
                    self.tiros.remove(shot)
                    variacao += 1

            self.draw_shots()