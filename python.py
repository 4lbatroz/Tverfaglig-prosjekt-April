import pygame
import sys

# Initialiser Pygame
pygame.init()

# Definer konstanter
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Opprett et vindu
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Adventure")

# Opprett spilleren
player = pygame.Rect(100, 100, 50, 50)
player_speed = 1

# Opprett vegger for første rom
wall_thickness = 30
room1_top_wall = pygame.Rect(0, 0, SCREEN_WIDTH, wall_thickness)
room1_bottom_wall = pygame.Rect(0, SCREEN_HEIGHT - wall_thickness, SCREEN_WIDTH, wall_thickness)
room1_left_wall = pygame.Rect(0, 0, wall_thickness, SCREEN_HEIGHT)
room1_right_wall = pygame.Rect(SCREEN_WIDTH - wall_thickness, 0, wall_thickness, SCREEN_HEIGHT)

# Opprett åpning (portal) for å koble rommene sammen
portal_width = 200
portal_height = 30
portal_x = (SCREEN_WIDTH - portal_width) // 2
portal_y_room1 = 0
portal_y_room2 = SCREEN_HEIGHT - portal_height
portal1 = pygame.Rect(portal_x, portal_y_room1, portal_width, portal_height)
portal2 = pygame.Rect(portal_x, portal_y_room2, portal_width, portal_height)

# Opprett vegger for andre rom
room2_top_wall = pygame.Rect(0, 0, SCREEN_WIDTH, wall_thickness)
room2_bottom_wall = pygame.Rect(0, SCREEN_HEIGHT - wall_thickness, SCREEN_WIDTH, wall_thickness)
room2_right_wall = pygame.Rect(SCREEN_WIDTH - wall_thickness, 0, wall_thickness, SCREEN_HEIGHT)
room2_left_wall = pygame.Rect(0, SCREEN_HEIGHT // 2, wall_thickness, SCREEN_HEIGHT // 2)

# Opprett åpning (portal) for å bytte rom mellom 2 og 3
room2_portal_width = 30
room2_portal_height = SCREEN_HEIGHT
room2_portal_x_left = 0
room2_portal_x_right = SCREEN_WIDTH - room2_portal_width
room2_portal_y = 0
room2_portal1 = pygame.Rect(room2_portal_x_left, room2_portal_y, room2_portal_width, room2_portal_height)
room2_portal2 = pygame.Rect(room2_portal_x_right, room2_portal_y, room2_portal_width, room2_portal_height)

# Opprett vegger for tredje rom
room3_top_wall = pygame.Rect(0, 0, SCREEN_WIDTH, wall_thickness)
room3_bottom_wall = pygame.Rect(0, SCREEN_HEIGHT - wall_thickness, SCREEN_WIDTH, wall_thickness)
room3_right_wall = pygame.Rect(SCREEN_WIDTH - wall_thickness, 0, wall_thickness, SCREEN_HEIGHT)
room3_left_wall = pygame.Rect(0, SCREEN_HEIGHT - wall_thickness, wall_thickness, SCREEN_HEIGHT // 2)

# Opprett vegger for fjerde rom
room4_top_wall = pygame.Rect(0, 0, SCREEN_WIDTH, wall_thickness)
room4_bottom_wall = pygame.Rect(0, SCREEN_HEIGHT - wall_thickness, SCREEN_WIDTH, wall_thickness)
room4_right_wall = pygame.Rect(SCREEN_WIDTH - wall_thickness, 0, wall_thickness, SCREEN_HEIGHT)
room4_left_wall = pygame.Rect(0, 0, wall_thickness, SCREEN_HEIGHT // 2)

# Spill-løkke
current_room = 1  # Indikerer hvilket rom spilleren er i
running = True
while running:
    screen.fill(WHITE)  # Fyll skjermen med hvit farge

    # Tegn vegger og åpninger basert på hvilket rom spilleren er i
    if current_room == 1:
        pygame.draw.rect(screen, BLACK, room1_top_wall)
        pygame.draw.rect(screen, BLACK, room1_bottom_wall)
        pygame.draw.rect(screen, BLACK, room1_left_wall)
        pygame.draw.rect(screen, BLACK, room1_right_wall)
        pygame.draw.rect(screen, WHITE, portal1)  # Tegn åpning (portal)
    elif current_room == 2:
        pygame.draw.rect(screen, BLACK, room2_top_wall)
        pygame.draw.rect(screen, BLACK, room2_bottom_wall)
        pygame.draw.rect(screen, BLACK, room2_left_wall)
        pygame.draw.rect(screen, BLACK, room2_right_wall)
        pygame.draw.rect(screen, WHITE, portal2)  # Tegn åpning (portal)
        pygame.draw.rect(screen, WHITE, room2_portal1)  # Tegn portal
        pygame.draw.rect(screen, WHITE, room2_portal2)  # Tegn portal
    elif current_room == 3:
        pygame.draw.rect(screen, BLACK, room3_top_wall)
        pygame.draw.rect(screen, BLACK, room3_bottom_wall)
        pygame.draw.rect(screen, BLACK, room3_left_wall)
        pygame.draw.rect(screen, BLACK, room3_right_wall)
    elif current_room == 4:
        pygame.draw.rect(screen, BLACK, room4_top_wall)
        pygame.draw.rect(screen, BLACK, room4_bottom_wall)
        pygame.draw.rect(screen, BLACK, room4_left_wall)
        pygame.draw.rect(screen, BLACK, room4_right_wall)

    # Tegn spilleren
    pygame.draw.rect(screen, BLACK, player)

    # Håndter tastaturinndata
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed
    if keys[pygame.K_UP]:
        player.y -= player_speed
    if keys[pygame.K_DOWN]:
        player.y += player_speed

    # Sjekk om spilleren går gjennom portalen for å bytte rom
    if current_room == 1 and player.colliderect(portal1):
        current_room = 2
        player.y = portal_y_room2 + portal_height + 1
    elif current_room == 2 and player.colliderect(portal2):
        current_room = 1
        player.y = portal_y_room1 - player.height - 1
    elif current_room == 2 and player.colliderect(room2_portal1):
        current_room = 3
        player.x = room2_portal_x_right + 1
    elif current_room == 2 and player.colliderect(room2_portal2):
        current_room = 4
        player.x = room2_portal_x_left - player.width - 1
    elif current_room == 3:
        # Logikk for å gå tilbake til rom 2 kan legges til her
        pass
    elif current_room == 4:
        # Logikk for å gå tilbake til rom 2 kan legges til her
        pass

    # Begrens spillerens bevegelse innenfor skjermen og åpningen (portal)
    if current_room == 1:
        player.left = max(player.left, room1_left_wall.right)
        player.top = max(player.top, room1_top_wall.bottom)
        player.right = min(player.right, room1_right_wall.left)
        player.bottom = min(player.bottom, room1_bottom_wall.top)
    elif current_room == 2:
        player.left = max(player.left, room2_left_wall.right)
        player.top = max(player.top, room2_top_wall.bottom)
        player.right = min(player.right, room2_right_wall.left)
        player.bottom = min(player.bottom, room2_bottom_wall.top)
    elif current_room == 3:
        player.left = max(player.left, room3_left_wall.right)
        player.top = max(player.top, room3_top_wall.bottom)
        player.right = min(player.right, room3_right_wall.left)
        player.bottom = min(player.bottom, room3_bottom_wall.top)
    elif current_room == 4:
        player.left = max(player.left, room4_left_wall.right)
        player.top = max(player.top, room4_top_wall.bottom)
        player.right = min(player.right, room4_right_wall.left)
        player.bottom = min(player.bottom, room4_bottom_wall.top)

    # Oppdater skjermen
    pygame.display.flip()

# Avslutt Pygame
pygame.quit()
sys.exit()
