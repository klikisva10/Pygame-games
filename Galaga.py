import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 1920
window_height = 1080
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Galaga')

# Load the background image
background_image = pygame.image.load('galaxy.jpg')
background_image = pygame.transform.scale(background_image, (window_width, window_height))

# Define colors
BLACK = (0, 0, 0)
BLUE = (20, 225, 211)
RED = (255, 0, 0)

# Load the player's ship image
player_image = pygame.image.load('player.png')
player_image = pygame.transform.scale(player_image, (100, 100))
player_rect = player_image.get_rect()
player_rect.centerx = window_width // 2
player_rect.bottom = window_height - 10
player_speed = 20

# Load the enemy image
enemy_image = pygame.image.load('enemy.png')
enemy_image = pygame.transform.scale(enemy_image, (150, 100))
# Set up the enemy wave
enemies = []
enemy_speed = 3
enemy_spawn_rate = 40
next_enemy_spawn = enemy_spawn_rate

# Set up the bullets
bullets = []
bullet_speed = 40

# Set up sounds
pygame.mixer.init()
pygame.mixer.music.load('sounds.ogg')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.2)

# Set up the score
score = 0
font = pygame.font.Font(None, 36)

# Set up the game clock
clock = pygame.time.Clock()

# Initialize the joystick
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()
if joystick_count > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

# Define joystick button constants
JOY_X_BUTTON = 1  # Button for shooting
JOY_A_BUTTON = 0  # Button for special ability

# Initialize the enemies_left counter
enemies_left = 0

# Track the elapsed time
start_time = time.time()

# Initialize the game_over flag
game_over = False

# Initialize special ability flag
special_ability_used = False

# Main game loop
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_rect = pygame.Rect(player_rect.centerx - 3, player_rect.top - 20, 6, 20)
                bullets.append(bullet_rect)
        elif event.type == pygame.JOYBUTTONDOWN:
            if joystick_count > 0:
                if event.button == JOY_X_BUTTON:
                    bullet_rect = pygame.Rect(player_rect.centerx - 3, player_rect.top - 20, 6, 20)
                    bullets.append(bullet_rect)
                elif event.button == JOY_A_BUTTON:
                    if not special_ability_used:
                        # Kill all enemies
                        enemies.clear()
                        special_ability_used = True

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.move_ip(-player_speed, 0)
    if keys[pygame.K_RIGHT] and player_rect.right < window_width:
        player_rect.move_ip(player_speed, 0)

        # Move the player with the joystick
    if joystick_count > 0:
        joystick_x = joystick.get_axis(0)
        player_rect.move_ip(int(joystick_x * player_speed), 0)

    # Calculate the elapsed time
    elapsed_time = time.time() - start_time

    # Adjust the enemy spawn rate based on elapsed time
    enemy_spawn_rate = max(40 - int(elapsed_time), 10)

    # Spawn enemies
    next_enemy_spawn -= 1
    if next_enemy_spawn <= 0:
        enemy_rect = enemy_image.get_rect()
        enemy_rect.left = random.randint(0, window_width - enemy_rect.width)
        enemy_rect.top = -enemy_rect.height
        enemies.append(enemy_rect)
        next_enemy_spawn = enemy_spawn_rate

    # Move the enemies
    for enemy_rect in enemies:
        enemy_rect.move_ip(0, enemy_speed)

    # Move the bullets
    for bullet_rect in bullets:
        bullet_rect.move_ip(0, -bullet_speed)

    # Check for collisions between bullets and enemies
    for bullet_rect in bullets:
        for enemy_rect in enemies:
            if bullet_rect.colliderect(enemy_rect):
                bullets.remove(bullet_rect)
                enemies.remove(enemy_rect)
                score += 10

    # Check if enemies have left the screen
    for enemy_rect in enemies:
        if enemy_rect.bottom > window_height:
            enemies.remove(enemy_rect)
            enemies_left += 1

    # Check if enough enemies have left to end the game
    if enemies_left >= 3:
        game_over = True

    # Draw everything
    window.blit(background_image, (0, 0))
    window.blit(player_image, player_rect)
    for enemy_rect in enemies:
        window.blit(enemy_image, enemy_rect)
    for bullet_rect in bullets:
        pygame.draw.rect(window, BLUE, bullet_rect)
    score_text = font.render('Score: {}'.format(score), True, RED)
    window.blit(score_text, (10, 10))
    left_text = font.render('Enemies Escaped: {}'.format(enemies_left), True, RED)
    window.blit(left_text, (10, 50))

    # Draw special ability text if it has been used
    if special_ability_used:
        special_text = font.render('Special Ability Used!', True, RED)
        window.blit(special_text, (window_width // 2 - special_text.get_width() // 2, 10))

    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

# Display "You lose" and stop the game
if game_over:
    lose_text = font.render('U DED', True, RED)
    lose_text = pygame.transform.scale(lose_text, (lose_text.get_width() * 10, lose_text.get_height() * 10))  # Scale the text
    lose_rect = lose_text.get_rect(center=(window_width // 2, window_height // 2))
    window.blit(lose_text, lose_rect)
    pygame.display.flip()
    time.sleep(2)

# Clean up
pygame.quit()


