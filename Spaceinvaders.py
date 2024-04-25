import pygame
import random
import math
from pygame import mixer

# Initialiserer Pygame
pygame.init()

# Oppretter skjermen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
color = (255, 255, 255)
screen.fill(color)

# Navn og ikon
pygame.display.set_caption("Welcome to Albuquerque New Mexico")

# Poeng
score_val = 0
scoreX = 5
scoreY = 5
font = pygame.font.Font('freesansbold.ttf', 20)

# Game Over
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Points: " + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (190, 250))

# Bakgrunnsmusikk
music = pygame.mixer.Sound('A Horse with No Name - America.mp3')
music.play(-1)
music.set_volume(1.5)

# Spiller
playerImage = pygame.image.load('car.png')
playerImage = pygame.transform.scale(playerImage, (80, 80))
player_X = 0
player_Y = 500
player_Xchange = 0

# Invader
invaderImage = []
invader_X = []
invader_Y = []
invader_Xchange = []
invader_Ychange = []
no_of_invaders = 8

for num in range(no_of_invaders):
    invaderImage.append(pygame.image.load('hector.jpeg'))
    invaderImage[num] = pygame.transform.scale(invaderImage[num], (70, 70))
    invader_X.append(random.randint(64, 737))
    invader_Y.append(random.randint(30, 180))
    invader_Xchange.append(0.2)
    invader_Ychange.append(50)

# Kule
bulletImage = pygame.image.load('meth.jpeg')
bulletImage = pygame.transform.scale(bulletImage, (50, 50))
bullet_X = 0
bullet_Y = 500
bullet_Xchange = 0
bullet_Ychange = 0.5
bullet_state = "rest"

# Kollisjon
def isCollision(x1, x2, y1, y2):
    distance = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
    if distance <= 50:
        return True
    else:
        return False

def player(x, y):
    screen.blit(playerImage, (x - 16, y + 10))

def invader(x, y, i):
    screen.blit(invaderImage[i], (x, y))

def bullet(x, y):
    global bullet_state
    screen.blit(bulletImage, (x, y))
    bullet_state = "fire"

# Legg til en teller for å holde styr på antall iterasjoner
invader_spawn_timer = 0
spawn_interval = 100  # 600 iterasjoner tilsvarer 10 sekunder med 60 oppdateringer per sekund

# Spill-løkke
running = True
game_over_flag = False

while running:

    screen.fill((0, 0, 0))

    # Øk telleren i hver iterasjon
    invader_spawn_timer += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_Xchange = -0.5
            if event.key == pygame.K_RIGHT:
                player_Xchange = 0.5
            if event.key == pygame.K_UP:
                if bullet_state == "rest":
                    bullet_X = player_X
                    bullet(bullet_X, bullet_Y)
                    bullet_sound = mixer.Sound('9mm-pistol-shot-6349.mp3')
                    bullet_sound.play()
                    bullet_sound.set_volume(0.1)
        if event.type == pygame.KEYUP:
            player_Xchange = 0

    player_X += player_Xchange

    for i in range(no_of_invaders):
        invader_X[i] += invader_Xchange[i]

        if invader_Y[i] >= 450:
            if abs(player_X - invader_X[i]) < 80:
                for j in range(no_of_invaders):
                    invader_Y[j] = 2000
                game_over_flag = True
                

        if invader_X[i] >= 735 or invader_X[i] <= 0:
            invader_Xchange[i] *= -1
            invader_Y[i] += invader_Ychange[i]

        collision = isCollision(bullet_X, invader_X[i], bullet_Y, invader_Y[i])
        if collision:
            score_val += 1
            bullet_Y = 600
            bullet_state = "rest"
            invader_X[i] = random.randint(64, 736)
            invader_Y[i] = random.randint(30, 200)
            invader_Xchange[i] *= -1
            
        invader(invader_X[i], invader_Y[i], i)

    # Legg til en ny invader hvis det er tid
    if invader_spawn_timer >= spawn_interval:
        # Legg til en ny invader
        invaderImage.append(pygame.image.load('hector.jpeg'))
        invaderImage[-1] = pygame.transform.scale(invaderImage[-1], (70, 70))
        invader_X.append(random.randint(64, 737))
        invader_Y.append(random.randint(30, 180))
        invader_Xchange.append(0.2)
        invader_Ychange.append(50)

        # Tilbakestill telleren
        invader_spawn_timer = 0

    if player_X <= 16:
        player_X = 16
    elif player_X >= 750:
        player_X = 750

    if game_over_flag:
        game_over()
    else:
        player(player_X, player_Y)
        show_score(scoreX, scoreY)

    if bullet_Y <= 0:
        bullet_Y = 600
        bullet_state = "rest"
    if bullet_state == "fire":
        bullet(bullet_X, bullet_Y)
        bullet_Y -= bullet_Ychange

    pygame.display.update()
