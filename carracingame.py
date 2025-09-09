import pygame
import random

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600
CAR_WIDTH, CAR_HEIGHT = 50, 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing Game")

# Load images
car_img = pygame.image.load("car.png")
car_img = pygame.transform.scale(car_img, (CAR_WIDTH, CAR_HEIGHT))
road_img = pygame.image.load("road.png")
road_img = pygame.transform.scale(road_img, (WIDTH, HEIGHT))
obstacle_img = pygame.image.load("obstacle.png")
obstacle_img = pygame.transform.scale(obstacle_img, (50, 50))

# Game Variables
car_x, car_y = WIDTH // 2 - CAR_WIDTH // 2, HEIGHT - 150
obstacle_x = random.randint(0, WIDTH - 50)
obstacle_y = -50
obstacle_speed = 5
car_speed = 5  # Speed of car movement
score = 0  # Initialize score
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
paused = False  # Pause state

def draw_objects():
    screen.fill(WHITE)
    screen.blit(road_img, (0, 0))
    screen.blit(car_img, (car_x, car_y))
    screen.blit(obstacle_img, (obstacle_x, obstacle_y))
    
    # Display score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    # Display pause message
    if paused:
        pause_text = font.render("Game Paused - Press P to Resume", True, RED)
        screen.blit(pause_text, (WIDTH // 2 - 150, HEIGHT // 2))
    
    pygame.display.update()

# Game Loop
running = True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Toggle pause
                paused = not paused
    
    if not paused:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_x > 0:
            car_x -= car_speed
        if keys[pygame.K_RIGHT] and car_x < WIDTH - CAR_WIDTH:
            car_x += car_speed
        if keys[pygame.K_UP] and car_y > 0:
            car_y -= car_speed
        if keys[pygame.K_DOWN] and car_y < HEIGHT - CAR_HEIGHT:
            car_y += car_speed
        
        # Move obstacle
        obstacle_y += obstacle_speed
        if obstacle_y > HEIGHT:
            obstacle_y = -50
            obstacle_x = random.randint(0, WIDTH - 50)
            score += 1  # Increase score when passing obstacle
        
        # Collision detection
        car_rect = pygame.Rect(car_x, car_y, CAR_WIDTH, CAR_HEIGHT)
        obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, 50, 50)
        if car_rect.colliderect(obstacle_rect):
            print("Game Over! Final Score:", score)
            running = False
    
    draw_objects()
    clock.tick(30)

pygame.quit()
