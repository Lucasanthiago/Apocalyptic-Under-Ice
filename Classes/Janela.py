from PPlay.window import *


class Janela(Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        Window.keyboard = keyboard.Keyboard()
        Window.mouse = mouse.Mouse()

        Window.screen = pygame.display.set_mode([self.width, self.height], pygame.FULLSCREEN)
        pygame.display.update()
