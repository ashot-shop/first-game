import pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((600,360))
pygame.display.set_caption("SCOOL")
icon = pygame.image.load("=3/icon.png").convert_alpha()
pygame.display.set_icon(icon)


bg = pygame.image.load("=3/background.jpg").convert_alpha()
player = pygame.image.load("=3/person/9.png").convert_alpha()
walk_left = [
    pygame.image.load("=3/person/9.png").convert_alpha(),
    pygame.image.load("=3/person/10.png").convert_alpha(),
    pygame.image.load("=3/person/11.png").convert_alpha(),
    pygame.image.load("=3/person/12.png").convert_alpha(),
]
walk_right = [
    pygame.image.load("=3/person/5.png").convert_alpha(),
    pygame.image.load("=3/person/6.png").convert_alpha(),
    pygame.image.load("=3/person/7.png").convert_alpha(),
    pygame.image.load("=3/person/8.png").convert_alpha(),
]

ghost = pygame.image.load("=3/ghost.png").convert_alpha()
ghost_list_in_game = []

player_anim_count = 0
bg_x = 0

player_speed = 5
player_x = 150
player_y = 209

is_jump = False
jump_count = 8

bg_sound = pygame.mixer.Sound("sounds/bg.mp3")
bg_sound.play()

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 3000)

running = True
while running:
    keys = pygame.key.get_pressed()

    screen.blit(bg, (bg_x,0))
    screen.blit(bg, (bg_x+600,0))


    player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

    if ghost_list_in_game:
        for el in ghost_list_in_game:
            screen.blit(ghost, el)
            el.x -= 10


            if player_rect.colliderect(el):
                print("WARNING")


    if keys[pygame.K_LEFT]:
        screen.blit(walk_left[player_anim_count], (player_x, player_y))
    elif keys[pygame.K_RIGHT]:
        screen.blit(walk_right[player_anim_count], (player_x, player_y))
    else:
        screen.blit(pygame.image.load("=3/person/13.png").convert_alpha(), (player_x, player_y))



    if keys[pygame.K_LEFT] and player_x > 50:
        player_x -= player_speed
    elif keys[pygame.K_RIGHT] and player_x < 300:
        player_x += player_speed

    if not is_jump:
        if keys[pygame.K_SPACE]:
            is_jump = True
    else:
        if jump_count >= -8:
            if jump_count > 0:
                player_y -= (jump_count**2)/2
            else:
                player_y += (jump_count**2)/2
            jump_count -= 1
        else:
            is_jump = False
            jump_count = 8

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
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(602,209)))

    clock.tick(15)
