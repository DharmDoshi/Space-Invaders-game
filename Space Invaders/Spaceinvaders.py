import pygame
import random
import math

pygame.init()

# Screen
screen = pygame.display.set_mode((800, 600))

# Title
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load('game.png')
player_x = 370
player_y = 510
player_x_dx = 0

# Enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_dx = []
enemy_y_dy = []
num_of_enemies = 10

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('battle.png'))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(10, 150))
    enemy_x_dx.append(0.3)
    enemy_y_dy.append(40)

# Bullet
bullet_img = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 510
bullet_x_dx = 0
bullet_y_dy = 1
bullet_state = "ready"

# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 24)
text_x = 10
text_y = 10

 # Game over
gameover_font = pygame.font.Font('freesansbold.ttf', 70)


def gameover_txt():
    over_txt = gameover_font.render("GAME OVER", True, (255, 255, 255) )
    screen.blit(over_txt, (200, 250))


def show_score(x, y):
    score_value = font.render("score: " + str(score), True, (255, 255, 255) )
    screen.blit(score_value, (x, y))

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x+16, y+10))

def collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((enemy_x - bullet_x)**2 + (enemy_y - bullet_y)**2)
    if distance < 27:
        return True
    else:
        return False

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
# Movement of player
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_dx -= 0.5
            if event.key == pygame.K_RIGHT:
                player_x_dx += 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or  event.key == pygame.K_RIGHT:
                player_x_dx = 0

# Boundaries
    player_x += player_x_dx

    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    for i in range(num_of_enemies):
        # Game over
        if enemy_y[i] > 475:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            gameover_txt()
            break

        enemy_x[i] += enemy_x_dx[i]
        if enemy_x[i] <= 0:
            enemy_x_dx[i]= 0.3
            enemy_y[i] += enemy_y_dy[i]
        elif enemy_x[i] >= 736:
            enemy_x_dx[i] -= 0.3
            enemy_y[i] += enemy_y_dy[i]

        # Collision
        in_collision = collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if in_collision:
            bullet_y = 510
            bullet_state = "ready"
            score += 100
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(10, 150)
        enemy(enemy_x[i], enemy_y[i], i)
    # Bullet Movement
    if bullet_y <= 0:
        bullet_y = 510
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_dy



    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()
