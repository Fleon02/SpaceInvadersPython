import pygame

class Jugador:
    # Imagen compartida por todos los jugadores (constante de clase)
    IMAGEN = pygame.image.load("img/nave.png") ## desde donde está el main

    def __init__(self, nombre, posX, posY):
        self.nombre = nombre
        self.x = posX
        self.y = posY
        self.imagen = Jugador.IMAGEN
