import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

background = pygame.image.load("background.png")

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
player_image = pygame.image.load("spaceship.png")
player_x = 370
player_y = 480
player_x_change = 0
player_y_change = 0
#
# Enemy
enemy_image = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_image.append(pygame.image.load("enemy1.png"))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(2)
    enemy_y_change.append(40)
#
# Bullet
bullet_image = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 3
bullet_state = "ready"
#
# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 40)
text_x = 10
text_y = 10
#
game_over_font = pygame.font.Font("freesansbold.ttf", 64)


def game_over_text(x, y):
    over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(player_image, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (x+16, y+10))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)
            if event.key == pygame.K_ESCAPE:
                exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

# Player movement
    player_x += player_x_change
#
# Player boundaries control
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736
    if player_y <= 0:
        player_y = 0
    elif player_y >= 534:
        player_y = 534
#
# Enemy movement
    for i in range(num_of_enemies):
        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over_text(200, 250)
            break

        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 2
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -2
            enemy_y[i] += enemy_y_change[i]
        # Collision
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)
    #
        enemy(enemy_x[i], enemy_y[i], i)
#
# Enemy boundaries control
    if enemy_x[i] <= 0:
        enemy_x[i] = 0
    elif enemy_x[i] >= 736:
        enemy_x[i] = 736
#
# Bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
#

    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()
