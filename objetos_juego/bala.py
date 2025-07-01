import pygame

class Bala:

    IMAGEN = pygame.image.load("img/bala.png")

    def __init__(self,posX, posY):
        self.x = posX
        self.y = posY
        self.imagen = Bala.IMAGEN
