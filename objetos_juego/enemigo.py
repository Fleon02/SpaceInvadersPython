import pygame

class Enemigo:

    IMAGEN = pygame.image.load("img/enemigo.png")

    def __init__(self,posX, posY):
        self.x = posX
        self.y = posY
        self.imagen = Enemigo.IMAGEN
