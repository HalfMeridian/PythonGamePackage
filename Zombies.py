import pygame
import sys
import math
import time
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 40
PLAYER_SPEED = 1
ZOMBIE_SIZE = 30
ZOMBIE_SPEED = 0.1
BULLET_SIZE = 10
BULLET_SPEED = 15
BULLET_DURATION = 2

# Speed increment after shooting a zombie
SPEED_INCREMENT = 0.025

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Attack Game")

# Initialize player variables
player_x = (WIDTH - PLAYER_SIZE) // 2
player_y = HEIGHT - PLAYER_SIZE - 20
player_speed_x = 0
player_speed_y = 0

# Initialize bullet variables
bullets = []

# Initialize zombie variables
zombies = [{"x": random.randint(0, WIDTH - ZOMBIE_SIZE), "y": random.randint(0, HEIGHT - ZOMBIE_SIZE)} for _ in range(2)]

# Initialize game state
game_over = False
zombies_shot = 0
health = 3

# Calculate zombie velocity towards the player
def calculate_zombie_velocity(zombie_x, zombie_y, player_x, player_y):
    angle = math.atan2(player_y - zombie_y, player_x - zombie_x)
    velocity_x = ZOMBIE_SPEED * math.cos(angle)
    velocity_y = ZOMBIE_SPEED * math.sin(angle)
    return velocity_x, velocity_y

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player controls
        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player_speed_y = -PLAYER_SPEED
                if event.key == pygame.K_s:
                    player_speed_y = PLAYER_SPEED
                if event.key == pygame.K_a:
                    player_speed_x = -PLAYER_SPEED
                if event.key == pygame.K_d:
                    player_speed_x = PLAYER_SPEED
                if event.key == pygame.K_SPACE:
                    bullet = {
                        "x": player_x + (PLAYER_SIZE - BULLET_SIZE) // 2,
                        "y": player_y,
                        "speed_x": player_speed_x,
                        "speed_y": player_speed_y,
                        "start_time": time.time(),
                    }
                    bullets.append(bullet)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player_speed_y = 0
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    player_speed_x = 0

    if not game_over:
        # Update player position and prevent player from leaving the screen
        player_x += player_speed_x
        player_y += player_speed_y
        player_x = max(0, min(player_x, WIDTH - PLAYER_SIZE))
        player_y = max(0, min(player_y, HEIGHT - PLAYER_SIZE))

        # Update bullet positions and remove expired bullets
        for bullet in bullets.copy():
            bullet["x"] += bullet["speed_x"]
            bullet["y"] += bullet["speed_y"]
            if time.time() - bullet["start_time"] > BULLET_DURATION:
                bullets.remove(bullet)

        # Update zombie positions
        for zombie in zombies:
            zombie_velocity_x, zombie_velocity_y = calculate_zombie_velocity(zombie["x"], zombie["y"], player_x, player_y)
            zombie["x"] += zombie_velocity_x
            zombie["y"] += zombie_velocity_y

        # Collision detection - Zombie touching player
        for zombie in zombies.copy():
            if (
                player_x < zombie["x"] + ZOMBIE_SIZE
                and player_x + PLAYER_SIZE > zombie["x"]
                and player_y < zombie["y"] + ZOMBIE_SIZE
                and player_y + PLAYER_SIZE > zombie["y"]
            ):
                zombies.remove(zombie)
                health -= 1
                zombies.append({"x": random.randint(0, WIDTH - ZOMBIE_SIZE), "y": random.randint(0, HEIGHT - ZOMBIE_SIZE)})

        # Collision detection - Bullet hitting zombie
        for bullet in bullets.copy():
            for zombie in zombies.copy():
                if (
                    bullet["x"] < zombie["x"] + ZOMBIE_SIZE
                    and bullet["x"] + BULLET_SIZE > zombie["x"]
                    and bullet["y"] < zombie["y"] + ZOMBIE_SIZE
                    and bullet["y"] + BULLET_SIZE > zombie["y"]
                ):
                    bullets.remove(bullet)
                    zombies.remove(zombie)
                    zombies.append({"x": random.randint(0, WIDTH - ZOMBIE_SIZE), "y": random.randint(0, HEIGHT - ZOMBIE_SIZE)})
                    zombies_shot += 1
                    # Increase player and zombie speeds
                    PLAYER_SPEED += SPEED_INCREMENT
                    ZOMBIE_SPEED += SPEED_INCREMENT

        # Game over condition
        if health <= 0:
            game_over = True

    # Draw everything
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))

    for zombie in zombies:
        pygame.draw.rect(screen, GREEN, (zombie["x"], zombie["y"], ZOMBIE_SIZE, ZOMBIE_SIZE))

    for bullet in bullets:
        pygame.draw.rect(screen, ORANGE, (bullet["x"], bullet["y"], BULLET_SIZE, BULLET_SIZE))

    # Display health
    font = pygame.font.Font(None, 36)
    health_text = font.render(f"Health: {health}", True, BLUE)
    screen.blit(health_text, (10, 10))

    # Game over screen
    if game_over:
        game_over_text = f"Zombies shot: {zombies_shot}. Press SPACE to play again."
        font = pygame.font.Font(None, 36)
        text = font.render(game_over_text, True, RED)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Reset the game
                game_over = False
                player_x = (WIDTH - PLAYER_SIZE) // 2
                player_y = HEIGHT - PLAYER_SIZE - 20
                bullets = []
                zombies = [{"x": random.randint(0, WIDTH - ZOMBIE_SIZE), "y": random.randint(0, HEIGHT - ZOMBIE_SIZE)} for _ in range(2)]
                zombies_shot = 0
                health = 3
                PLAYER_SPEED = 1
                ZOMBIE_SPEED = 0.1

    pygame.display.update()

# Quit the game
pygame.quit()
sys.exit()
