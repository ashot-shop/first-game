import pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((600,360))
pygame.display.set_caption("SCOOL")
icon = pygame.image.load("=3/icon.png")
pygame.display.set_icon(icon)


bg = pygame.image.load("=3/background.jpg")
player = pygame.image.load("=3/person/9.png")
walk_left = [
    pygame.image.load("=3/person/9.png"),
    pygame.image.load("=3/person/10.png"),
    pygame.image.load("=3/person/11.png"),
    pygame.image.load("=3/person/12.png"),
]

walk_right = [
    pygame.image.load("=3/person/5.png"),
    pygame.image.load("=3/person/6.png"),
    pygame.image.load("=3/person/7.png"),
    pygame.image.load("=3/person/8.png"),
]

player_anim_count = 0
bg_x = 0

player_speed = 5
player_x = 150
player_y = 209

is_jump = False
jump_count = 7

bg_sound = pygame.mixer.Sound("sounds/bg.mp3")
bg_sound.play()

running = True
while running:
    keys = pygame.key.get_pressed()

    screen.blit(bg, (bg_x,0))
    screen.blit(bg, (bg_x+600,0))

    if keys[pygame.K_LEFT]:
        screen.blit(walk_left[player_anim_count], (player_x, player_y))
    else:
        screen.blit(walk_right[player_anim_count], (player_x, player_y))




    if keys[pygame.K_LEFT] and player_x > 50:
        player_x -= player_speed
    elif keys[pygame.K_RIGHT] and player_x < 300:
        player_x += player_speed

    if not is_jump:
        if keys[pygame.K_SPACE]:
            is_jump = True
    else:
        if jump_count >= -7:
            if jump_count > 0:
                player_y -= (jump_count**2)/2
            else:
                player_y += (jump_count**2)/2
            jump_count -= 1
        else:
            is_jump = False
            jump_count = 7

    if player_anim_count == 3:
        player_anim_count = 0
    else:
        player_anim_count += 1
    bg_x-=1.5
    if bg_x == -600:
        bg_x=0

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    clock.tick(15)
