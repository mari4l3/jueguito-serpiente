import pygame
import numpy as np
import random

pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de la Serpiente")

# Colores
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Configuración de la serpiente
snake_size = 20
snake_speed = 15

# Dirección inicial
direction = 'RIGHT'

# Posición inicial de la serpiente
snake_body = np.array([[100, 100], [80, 100], [60, 100]])

# Posición inicial de la comida
food_position = np.array([random.randrange(1, WIDTH // snake_size) * snake_size,
                          random.randrange(1, HEIGHT // snake_size) * snake_size])

# Contador de comidas
food_counter = 0

# Reloj para el FPS
clock = pygame.time.Clock()

def draw_snake(snake_body):
    for segment in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], snake_size, snake_size))

def draw_food(food_position):
    pygame.draw.rect(screen, RED, pygame.Rect(food_position[0], food_position[1], snake_size, snake_size))

def draw_score(score):
    font = pygame.font.SysFont('Arial', 20)
    score_text = font.render(f'Comidas: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

def check_collision(snake_head, snake_body):
    if any(np.array_equal(snake_head, segment) for segment in snake_body[1:]):
        return True
    if snake_head[0] < 0 or snake_head[0] >= WIDTH or snake_head[1] < 0 or snake_head[1] >= HEIGHT:
        return True
    return False

def game_loop():
    global direction, snake_body, food_position, food_counter

    running = True
    while running:
        screen.fill(BLACK)

        # Verificar eventos (teclado, cierre de ventana)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    direction = 'UP'
                if event.key == pygame.K_DOWN and direction != 'UP':
                    direction = 'DOWN'
                if event.key == pygame.K_LEFT and direction != 'RIGHT':
                    direction = 'LEFT'
                if event.key == pygame.K_RIGHT and direction != 'LEFT':
                    direction = 'RIGHT'

        # Movimiento de la serpiente
        head = snake_body[0].copy()
        if direction == 'UP':
            head[1] -= snake_size
        elif direction == 'DOWN':
            head[1] += snake_size
        elif direction == 'LEFT':
            head[0] -= snake_size
        elif direction == 'RIGHT':
            head[0] += snake_size

        snake_body = np.insert(snake_body, 0, head, axis=0)

        # Comida
        if np.array_equal(head, food_position):
            food_counter += 1  # Incrementar el contador de comidas
            food_position = np.array([random.randrange(1, WIDTH // snake_size) * snake_size,
                                      random.randrange(1, HEIGHT // snake_size) * snake_size])
        else:
            snake_body = snake_body[:-1]

        # Verificar colisiones
        if check_collision(head, snake_body):
            running = False

        # Dibujar la serpiente y la comida
        draw_snake(snake_body)
        draw_food(food_position)
        draw_score(food_counter)  # Mostrar el contador de comidas

        pygame.display.update()

        # Controlar la velocidad de la serpiente
        clock.tick(snake_speed)

    pygame.quit()

if __name__ == "__main__":
    game_loop()
