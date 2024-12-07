import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.25
FLAP_STRENGTH = -7
PIPE_WIDTH = 60
PIPE_GAP = 150
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (135, 206, 235)

# Setup Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load Bird Image
bird_image = pygame.image.load("bird.png")  # Make sure to replace this with your own image file
bird_image = pygame.transform.scale(bird_image, (40, 40))  # Resize the bird image if needed

# Font for the score
font = pygame.font.SysFont('Arial', 32)

# Bird Class
class Bird:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.width = 40
        self.height = 40
        self.velocity = 0
        self.flap = False

    def update(self):
        if self.flap:
            self.velocity = FLAP_STRENGTH
            self.flap = False
        self.velocity += GRAVITY
        self.y += self.velocity

        # Prevent the bird from going out of bounds (top/bottom)
        if self.y <= 0:
            self.y = 0
        elif self.y >= SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height

    def draw(self, screen):
        # Draw the bird image instead of a rectangle
        screen.blit(bird_image, (self.x, self.y))

    def flap_action(self):
        self.flap = True

# Pipe Class
class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        self.top = self.height
        self.bottom = self.height + PIPE_GAP
        self.width = PIPE_WIDTH
        self.speed = 3

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.top))  # Top pipe
        pygame.draw.rect(screen, GREEN, (self.x, self.bottom, self.width, SCREEN_HEIGHT - self.bottom))  # Bottom pipe

    def is_off_screen(self):
        return self.x + self.width < 0

# Function to check collisions
def check_collisions(bird, pipes):
    for pipe in pipes:
        if bird.x + bird.width > pipe.x and bird.x < pipe.x + pipe.width:
            if bird.y < pipe.top or bird.y + bird.height > pipe.bottom:
                return True
    return False

# Game Loop
def game_loop():
    bird = Bird()
    pipes = []
    score = 0
    level = 1
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(FPS)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Flap on spacebar press
                    bird.flap_action()

        # Update
        bird.update()

        # Create new pipes
        if len(pipes) == 0 or pipes[-1].x < SCREEN_WIDTH - 300:
            pipes.append(Pipe())

        # Update pipes
        for pipe in pipes:
            pipe.update()

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if not pipe.is_off_screen()]

        # Check for collisions
        if check_collisions(bird, pipes):
            running = False

        # Increase score
        for pipe in pipes:
            if pipe.x + pipe.width < bird.x and not hasattr(pipe, 'scored'):
                score += 1
                pipe.scored = True

        # Increase level based on score (makes pipes move faster)
        if score % 10 == 0 and score > 0 and score // 10 > level:
            level += 1
            for pipe in pipes:
                pipe.speed += 1

        # Drawing everything
        screen.fill(BLUE)

        # Draw bird
        bird.draw(screen)

        # Draw pipes
        for pipe in pipes:
            pipe.draw(screen)

        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Draw level
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(level_text, (SCREEN_WIDTH - 150, 10))

        # Update the display
        pygame.display.flip()

    # Game Over screen
    game_over_text = font.render(f"Game Over! Final Score: {score}", True, WHITE)
    screen.fill(BLACK)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.update()

    pygame.time.wait(2000)

# Start the game loop
game_loop()
