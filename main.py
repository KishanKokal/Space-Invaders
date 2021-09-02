import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen (width, height))px
screen = pygame.display.set_mode((800, 600))

# Background
backgroundImg = pygame.image.load('SpaceBackground.png')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('GameLogo.jpg')
pygame.display.set_icon(icon)

# Player 
playerImg = pygame.image.load('SpaceCraft.png')
playerX = 370 
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
# ready - You can't see the bullet on the screen
# fire - The bullet is currently moving

bulletImg = pygame.image.load('Bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 12
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('LLPIXEL3.ttf', 32)
textX = 10
textY = 10

# Game Over text
game_over_font = pygame.font.Font('LLPIXEL3.ttf', 64)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 0))
    screen.blit(score, (x, y))
    
def game_over():
    over_text = game_over_font.render("GAME OVER", True, (255, 255, 0))
    screen.blit(over_text, (200, 250))

def player(x, y):
    # Blit means to draw
    screen.blit(playerImg, (x, y)) # It has 2-parameters
    
def enemy(x, y, i):
    # Blit means to draw
    screen.blit(enemyImg[i], (x, y)) # It has 2-parameters
    
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))
    
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX)**2 + (enemyY - bulletY)**2)
    if distance < 27:
        return True
    else:
        return False

# Game Loop
running = True
while running:
    # RGB - Red, Green, Blue values lies between 0-255
    screen.fill((0, 0, 0))
    screen.blit(backgroundImg, (0, 0))
     
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # Event for Left key pressed
            if event.key == pygame.K_LEFT:
                playerX_change = -5
                
            # Event for Right key pressed
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
                
            # Event for Space key pressed
            if event.key == pygame.K_SPACE: 
                if bullet_state == "ready":
                    # Get the current x-coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    bullet_sound = mixer.Sound('shoot.wav')
                    bullet_sound.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
        
        # Check for the program if quit button is pressed
        if event.type == pygame.QUIT:
            running = False 
                            
    # Checking for boundaries of spaceship so it doesn't go out of bounds
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0 
    elif playerX >= 736:
        playerX = 736
            
    playerY += playerY_change
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536
        
    # Enemy movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break
        
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
            
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
            score_value += 1
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            
        enemy(enemyX[i], enemyY[i], i)
     
    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
        
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

pygame.quit()   