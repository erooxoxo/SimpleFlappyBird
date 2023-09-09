import pygame
import sys
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
BACKGROUND_COLOR = (0, 0, 0)
BIRD_COLOR = (255, 255, 0)
PIPE_COLOR = (0, 255, 0)

# Bird properties
bird_x = 50
bird_y = HEIGHT // 2
bird_radius = 20
bird_velocity = 0

# Pipe properties
pipe_width = 50
pipe_height = random.randint(100, 400)
pipe_x = WIDTH
pipe_gap = 200
pipe_speed = 5

score = 0
high_score = 0  # Initialize high score

# Load high score from file
try:
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    high_score = 0

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Game clock for limiting frame rate
clock = pygame.time.Clock()
frame_rate = 30  # Adjust the frame rate as needed

# Initialize game states
game_over = False
game_start = False  # New state to control game start

# Increase pipe speed over time
speed_increase_interval = 100  # Increase speed every 100 frames
current_frame = 0

# Gravity acceleration
gravity = 0.7  # Increase this value to make the bird fall faster

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save the high score before quitting
            with open("highscore.txt", "w") as file:
                file.write(str(high_score))
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    # Reset the game
                    bird_y = HEIGHT // 2
                    bird_velocity = 0
                    pipe_x = WIDTH
                    pipe_height = random.randint(100, 400)
                    score = 0
                    game_over = False
                else:
                    game_start = True  # Start the game when SPACE is pressed
                    bird_velocity = -10

    if game_start and not game_over:  # Update the game only if it's started and not over
        # Update bird position with increased gravity
        bird_velocity += gravity
        bird_y += bird_velocity

        # Update pipe position with the current speed
        pipe_x -= pipe_speed

        # Check for collisions
        if bird_y > HEIGHT or bird_y < 0:
            game_over = True

        if pipe_x < -pipe_width:
            pipe_x = WIDTH
            pipe_height = random.randint(100, 400)
            score += 1

        if (
            bird_x + bird_radius > pipe_x
            and bird_x - bird_radius < pipe_x + pipe_width
        ):
            if bird_y - bird_radius < pipe_height or bird_y + bird_radius > pipe_height + pipe_gap:
                game_over = True

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Draw bird
    pygame.draw.circle(screen, BIRD_COLOR, (bird_x, int(bird_y)), bird_radius)

    # Draw pipes
    pygame.draw.rect(screen, PIPE_COLOR, (pipe_x, 0, pipe_width, pipe_height))
    pygame.draw.rect(
        screen,
        PIPE_COLOR,
        (pipe_x, pipe_height + pipe_gap, pipe_width, HEIGHT - pipe_height - pipe_gap),
    )

    if not game_start:
        # Display start message
        font = pygame.font.Font(None, 36)
        start_text = font.render("Press SPACE to start", True, (255, 255, 255))
        screen.blit(start_text, (WIDTH // 2 - 120, HEIGHT // 2))

    if game_over:
        # Update the high score if needed
        if score > high_score:
            high_score = score

        # Display game over message and score
        font = pygame.font.Font(None, 36)
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
        restart_text = font.render("Press SPACE to restart", True, (255, 255, 255))
        screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 50))
        screen.blit(score_text, (WIDTH // 2 - 60, HEIGHT // 2))
        screen.blit(high_score_text, (WIDTH // 2 - 90, HEIGHT // 2 + 30))  # Display high score
        screen.blit(restart_text, (WIDTH // 2 - 120, HEIGHT // 2 + 80))

        # Check for restart input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_start = False  # Reset the start state
            bird_y = HEIGHT // 2
            bird_velocity = 0
            pipe_x = WIDTH
            pipe_height = random.randint(100, 400)
            score = 0
            game_over = False

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    clock.tick(frame_rate)

    # Increase pipe speed over time
    current_frame += 1
    if current_frame % speed_increase_interval == 0:
        pipe_speed += 1  # Increase the pipe speed every 100 frames
