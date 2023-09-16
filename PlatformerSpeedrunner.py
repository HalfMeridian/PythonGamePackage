import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1300, 700
PLAYER_SIZE = 40
OBSTACLE_SIZE = 30
ENDZONE_SIZE = 40
PLAYER_SPEED = 2
GRAVITY = 0.03
JUMP_STRENGTH = -4
MAX_JUMPS = 1

# Colors
WHITE = (135, 130, 120)
BLUE = (0, 65, 106)
RED = (134, 1, 17)
GREEN = (118, 255, 122)
GRAY = (169, 169, 169)
YELLOW = (184, 134, 11)
BLACK = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PlatformerSpeedrunner")

# Player attributes
player_x = WIDTH // 2 - PLAYER_SIZE // 2
player_y = HEIGHT - PLAYER_SIZE
player_vel_x = 0
player_vel_y = 0
on_ground = False
jumps = 0

# Level attributes
level = 1
level_start_time = 0

# Scoring
score_font = pygame.font.Font(None, 36)
score = 0

# Red obstacles list
red_obstacles = []

def generate_level():
    global obstacle_x, obstacle_y, endzone_x, endzone_y, platforms, level_start_time, red_obstacles

    # Clear the list of red obstacles
    red_obstacles = []

    # Randomize obstacle and endzone positions
    obstacle_x = random.randint(50, WIDTH - 50)
    obstacle_y = random.randint(100, HEIGHT - 100)
    endzone_x = random.randint(50, WIDTH - 50)
    endzone_y = random.randint(100, HEIGHT - 100)

    # Randomize platform positions (change every new level)
    if level < 10:
        num_platforms = 20 - level 
    else:
        num_platforms = 10
    platforms = [(random.randint(50, WIDTH - 50), random.randint(100, HEIGHT - 100)) for _ in range(num_platforms)]

    level_start_time = time.time()  # Start timing the level

    # Add red obstacles based on the level
    if level < 20:
        for _ in range(int(level/2)):
            red_obstacles.append((random.randint(50, WIDTH - 50), random.randint(100, HEIGHT - 100)))
    else:
        for _ in range(10):
            red_obstacles.append((random.randint(50, WIDTH - 50), random.randint(100, HEIGHT - 100)))

generate_level()

# Title screen
title_font = pygame.font.Font(None, 72)
button_font = pygame.font.Font(None, 36)

title_text = title_font.render("Platformer Speedrunner", True, BLACK)
title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

button_text = button_font.render("Start (E)", True, BLACK)
button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))

controls_text = button_font.render("Controls:", True, BLACK)
controls_rect = controls_text.get_rect(topleft=(50, 50))

controls_desc = [
    "A: Move Left",
    "D: Move Right",
    "W: Jump",
    "E: Start/Generate New Level"
]
controls_desc_surface = [button_font.render(text, True, BLACK) for text in controls_desc]
controls_desc_rects = [text.get_rect(topleft=(50, 100 + i * 40)) for i, text in enumerate(controls_desc_surface)]

show_title_screen = True
while show_title_screen:
    screen.fill(WHITE)
    screen.blit(title_text, title_rect)
    screen.blit(button_text, button_rect)
    screen.blit(controls_text, controls_rect)
    
    for text, rect in zip(controls_desc_surface, controls_desc_rects):
        screen.blit(text, rect)

    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                show_title_screen = False
                generate_level()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_x -= PLAYER_SPEED
    if keys[pygame.K_d]:
        player_x += PLAYER_SPEED
    if keys[pygame.K_w] and (on_ground or jumps < MAX_JUMPS):
        player_vel_y = JUMP_STRENGTH
        on_ground = False
        jumps += 1
    if keys[pygame.K_e]:
        #Generate a new level
        screen.fill(GRAY)
        GenerationScreen = score_font.render("Generating New Level", True, BLACK)
        screen.blit(GenerationScreen, (WIDTH // 2 - GenerationScreen.get_width() // 2, HEIGHT // 2 - GenerationScreen.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(1000)
        generate_level()
        score = score - 1
    

    # Apply gravity
    if not on_ground:
        player_vel_y += GRAVITY

    # Update player position
    player_x += player_vel_x
    player_y += player_vel_y

    # Collision with obstacles and endzone
    if player_x < 0:
        player_x = 0
    if player_x > WIDTH - PLAYER_SIZE:
        player_x = WIDTH - PLAYER_SIZE
    if player_y > HEIGHT - PLAYER_SIZE:
        player_y = HEIGHT - PLAYER_SIZE
        player_vel_y = 0
        on_ground = True
        jumps = 0

    # Check collision with obstacle
    obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, OBSTACLE_SIZE, OBSTACLE_SIZE)
    player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)

    if player_rect.colliderect(obstacle_rect):
        # Do not reset the level on collision with obstacle
        player_x = WIDTH // 2 - PLAYER_SIZE // 2
        player_y = HEIGHT - PLAYER_SIZE
        jumps = 0

    # Check collision with endzone
    endzone_rect = pygame.Rect(endzone_x, endzone_y, ENDZONE_SIZE, ENDZONE_SIZE)

    if player_rect.colliderect(endzone_rect):
        level += 1
        score = time.time() - level_start_time  # Calculate the score (time taken)
        generate_level()

        # Display a yellow square for about 1 second along with the score
        screen.fill(GRAY)
        score = score - 1
        score_text = score_font.render(f"Level {level} Time: {score:.2f}s", True, BLACK)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - score_text.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(1000)

    # Check collision with platforms
    on_ground = False
    player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
    for platform_x, platform_y in platforms:
        platform_rect = pygame.Rect(platform_x, platform_y, OBSTACLE_SIZE, OBSTACLE_SIZE)
        if player_rect.colliderect(platform_rect) and player_y + PLAYER_SIZE <= platform_y + 10:
            player_vel_y = 0
            player_y = platform_y - PLAYER_SIZE
            on_ground = True
            jumps = 0

    # Check collision with red obstacles
    for red_obstacle_x, red_obstacle_y in red_obstacles:
        red_obstacle_rect = pygame.Rect(red_obstacle_x, red_obstacle_y, OBSTACLE_SIZE, OBSTACLE_SIZE)
        if player_rect.colliderect(red_obstacle_rect):
            # Do not reset the level on collision with red obstacles
            player_x = WIDTH // 2 - PLAYER_SIZE // 2
            player_y = HEIGHT - PLAYER_SIZE
            jumps = 0
            pygame.time.wait(100)

    # Clear the screen
    screen.fill(WHITE)

    # Draw the player, obstacles, endzone, platforms, and red obstacles
    pygame.draw.rect(screen, BLUE, (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))
    pygame.draw.rect(screen, RED, (obstacle_x, obstacle_y, OBSTACLE_SIZE, OBSTACLE_SIZE))
    pygame.draw.rect(screen, GREEN, (endzone_x, endzone_y, ENDZONE_SIZE, ENDZONE_SIZE))

    for platform_x, platform_y in platforms:
        pygame.draw.rect(screen, GRAY, (platform_x, platform_y, OBSTACLE_SIZE, OBSTACLE_SIZE))

    for red_obstacle_x, red_obstacle_y in red_obstacles:
        pygame.draw.rect(screen, RED, (red_obstacle_x, red_obstacle_y, OBSTACLE_SIZE, OBSTACLE_SIZE))

    # Update the display
    pygame.display.update()

# Quit the game
pygame.quit()

