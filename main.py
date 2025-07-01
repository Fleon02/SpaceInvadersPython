import pygame
import random
import math
from pygame import mixer

from objetos_juego.enemigo import Enemigo
from objetos_juego.jugador import Jugador
from objetos_juego.bala import Bala

# Inicializar Pygame
pygame.init()

# Crear pantalla
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders by Francisco Leon")
icono = pygame.image.load("img/icon_ovni.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("img/fondo.jpg")

# Fuente para texto
fuente = pygame.font.Font(None, 50)

# Sonido de Game Over (se cargan fuera para no recargar cada vez)
sonido_game_over = mixer.Sound("ost/game-over_sonic.mp3")

def pedir_nombre():
    texto = ''
    escribiendo = True

    while escribiendo:
        pantalla.fill((0, 0, 0))  # Fondo negro
        mensaje = fuente.render("Ingresa tu nombre:", True, (255, 255, 255))
        pantalla.blit(mensaje, (200, 200))

        entrada = fuente.render(texto, True, (0, 255, 0))
        pantalla.blit(entrada, (200, 300))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    escribiendo = False
                elif e.key == pygame.K_BACKSPACE:
                    texto = texto[:-1]
                else:
                    if len(texto) < 15:
                        texto += e.unicode

    return texto

def leer_max_puntuacion():
    try:
        with open("max_puntuacion.txt", "r") as f:
            return int(f.read().strip())
    except:
        return 0

def guardar_max_puntuacion(puntuacion):
    with open("max_puntuacion.txt", "w") as f:
        f.write(str(puntuacion))

def main():
    puntuacion = 0

    # Música de fondo inicial
    mixer.music.load("ost/MusicaFondo.mp3")
    mixer.music.set_volume(0.3)
    mixer.music.play(-1)

    # ⬇️ Primero pedimos el nombre
    nombre_jugador = pedir_nombre()

    mixer.music.load("ost/Super Smash Bros. Ultimate - Blast Away_ -Gummi Ship II- [HQ] [qKrcOLn5JOk].mp3")
    mixer.music.set_volume(0.3)
    mixer.music.play(-1)

    # Instanciar jugador
    jugador = Jugador(nombre_jugador, 368, 536)
    jugador_x_cambio = 0

    # Lista de enemigos
    enemigos = []
    cantidad_enemigos = 4
    for _ in range(cantidad_enemigos):
        x = random.randint(0, 736)
        y = random.randint(50, 200)
        enemigo = Enemigo(x, y)
        enemigos.append({
            'obj': enemigo,
            'x_cambio': 0.2,
            'y_cambio': 50
        })

    # Instanciar bala
    bala = Bala(0, jugador.y)
    bala_y_cambio = 0.4
    bala_visible = False

    reloj = pygame.time.Clock()

    def pintar_jugador(x, y):
        pantalla.blit(jugador.imagen, (x, y))

    def pintar_bala(x, y):
        nonlocal bala_visible
        bala_visible = True
        pantalla.blit(bala.imagen, (x + 16, y + 10))

    def hay_colision(x_obj1, y_obj1, x_obj2, y_obj2):
        distancia = math.sqrt(math.pow(x_obj1 - x_obj2, 2) + math.pow(y_obj1 - y_obj2, 2))
        return distancia < 27

    se_ejecuta = True
    derrota = False

    while se_ejecuta:
        pantalla.blit(fondo, (0, 0))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                se_ejecuta = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:
                    jugador_x_cambio = -0.2
                if evento.key == pygame.K_d:
                    jugador_x_cambio = 0.2
                if evento.key == pygame.K_SPACE:
                    sonido_bala = mixer.Sound("ost/disparo.mp3")
                    sonido_bala.play()
                    if not bala_visible:
                        bala.x = jugador.x
                        pintar_bala(bala.x, bala.y)
            if evento.type == pygame.KEYUP:
                if evento.key in [pygame.K_a, pygame.K_d]:
                    jugador_x_cambio = 0

        jugador.x += jugador_x_cambio
        jugador.x = max(0, min(jugador.x, 736))

        # Mover y pintar enemigos
        for enemigo_data in enemigos:
            enemigo = enemigo_data['obj']
            enemigo.x += enemigo_data['x_cambio']

            if enemigo.x <= 0:
                enemigo_data['x_cambio'] = 0.2
                enemigo.y += enemigo_data['y_cambio']
            elif enemigo.x >= 736:
                enemigo_data['x_cambio'] = -0.2
                enemigo.y += enemigo_data['y_cambio']

            # Game Over: si el enemigo baja demasiado
            if enemigo.y > 490:
                derrota = True
                break

            if hay_colision(enemigo.x, enemigo.y, bala.x, bala.y):
                sonido_colision = mixer.Sound("ost/roblox.mp3")
                sonido_colision.play()
                bala.y = 500
                bala_visible = False
                puntuacion += 1
                enemigo.x = random.randint(0, 736)
                enemigo.y = random.randint(50, 200)

            pantalla.blit(enemigo.imagen, (enemigo.x, enemigo.y))

        if derrota:
            mixer.music.stop()
            sonido_game_over.play()

            max_puntuacion = leer_max_puntuacion()
            nuevo_record = False
            if puntuacion > max_puntuacion:
                guardar_max_puntuacion(puntuacion)
                max_puntuacion = puntuacion
                nuevo_record = True

            opciones = ["Volver a jugar", "Salir"]
            opcion_seleccionada = 0
            seleccionando = True

            while seleccionando:
                pantalla.fill((0, 0, 0))

                # Texto multilinea manual
                lines = [
                    f"Moriste, {jugador.nombre}",
                    f"Puntuación: {puntuacion}",
                    f"Récord: {max_puntuacion}"
                ]
                if nuevo_record:
                    lines.append("¡Enhorabuena, superaste el récord!")

                for i, linea in enumerate(lines):
                    texto_render = fuente.render(linea, True, (255, 0, 0) if i == 0 else (255, 255, 255))
                    rect = texto_render.get_rect(center=(400, 150 + i * 50))
                    pantalla.blit(texto_render, rect)

                mouse_pos = pygame.mouse.get_pos()
                for i, texto in enumerate(opciones):
                    color = (255, 255, 255)
                    texto_render = fuente.render(texto, True, color)
                    rect = texto_render.get_rect(center=(400, 350 + i * 80))

                    if rect.collidepoint(mouse_pos):
                        opcion_seleccionada = i
                        texto_render = fuente.render(texto, True, (0, 255, 0))
                    elif i == opcion_seleccionada:
                        texto_render = fuente.render(texto, True, (0, 255, 0))

                    pantalla.blit(texto_render, rect)

                pygame.display.flip()

                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_UP:
                            opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones)
                        elif evento.key == pygame.K_DOWN:
                            opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones)
                        elif evento.key == pygame.K_RETURN:
                            seleccionando = False
                    elif evento.type == pygame.MOUSEBUTTONDOWN:
                        for i, texto in enumerate(opciones):
                            rect = fuente.render(texto, True, (255, 255, 255)).get_rect(center=(400, 350 + i * 80))
                            if rect.collidepoint(mouse_pos):
                                opcion_seleccionada = i
                                seleccionando = False

            if opciones[opcion_seleccionada] == "Salir":
                pygame.quit()
                exit()
            elif opciones[opcion_seleccionada] == "Volver a jugar":
                main()
                return

        if bala.y <= 64:
            bala.y = 500
            bala_visible = False
        if bala_visible:
            pintar_bala(bala.x, bala.y)
            bala.y -= bala_y_cambio

        pintar_jugador(jugador.x, jugador.y)

        nombre_render = fuente.render(jugador.nombre, True, (255, 255, 255))
        pantalla.blit(nombre_render, nombre_render.get_rect(topright=(790, 10)))

        puntuacion_render = fuente.render(f"Puntuación: {puntuacion}", True, (255, 255, 255))
        pantalla.blit(puntuacion_render, (10, 10))

        pygame.display.update()
        reloj.tick(600)

    pygame.quit()

if __name__ == "__main__":
    main()
