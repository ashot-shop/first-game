import pygame

def bullet_movement():
    global player_anim_count
    global bullet_rect
    global bullet
    global ghost_list_in_game  # Added to access ghosts
    global gameplay  # Added to access gameplay

    for bullet_rect in bullets[:]:  # Iterate over a copy of the list
        screen.blit(bullet, bullet_rect)
        bullet_rect.x += 10

        # Check for collision with ghosts
        for ghost_rect in ghost_list_in_game[:]:  # Iterate over a copy of the list
            if bullet_rect.colliderect(ghost_rect):
                ghost_list_in_game.remove(ghost_rect)  # Remove the ghost
                bullets.remove(bullet_rect)  # Remove the bullet
                break  # Exit the loop after a collision

        if bullet_rect.x > 675:
            bullets.remove(bullet_rect)

def animation_count():
    global player_anim_count
    global current_animation_frame
    global animation_rate
    current_animation_frame += 1
    if current_animation_frame >= animation_rate:
        current_animation_frame = 0
        player_anim_count += 1 
        if player_anim_count >= 4:
            player_anim_count = 0

def player_movement():
    global player_speed
    global keys
    global walk_left
    global walk_right
    global player_anim_count
    global bg_x
    if keys[pygame.K_LEFT]:
        screen.blit(walk_left[player_anim_count], (player_x, player_y))
        bg_x += 2
    elif keys[pygame.K_RIGHT]:
        screen.blit(walk_right[player_anim_count], (player_x, player_y))
        bg_x -= 2
    else:
        screen.blit(pygame.image.load( "=3/person/13.png").convert_alpha(), (player_x, player_y))
    animation_count()

def ghost_left():
    global ghost_list_in_game
    global player_anim_count
    global ghost
    global player_speed
    global bg_sound
    global gameplay

    if ghost_list_in_game:
        for (i, el) in enumerate(ghost_list_in_game):
            screen.blit(ghost, el)
            el.x -= 5

            if el.x < -10:
                ghost_list_in_game.pop(i)

            if player_rect.colliderect(el):
                gameplay = False
                bg_sound.stop()

def bullet_shot():
    global bullet
    global bullets
    global bullets_quantity
    bullets.append(bullet.get_rect(topleft = (player_x + 30, player_y + 10)))
    bullets_quantity -= 1


def draw_menu():
    global bg_menu
    global bg_menu_x

    screen.blit(bg_menu, (0, 0))  # Background color for the menu
    screen.blit(menu_label, (250, 50))  # Draw the menu title
    screen.blit(button, (185, 198))
    screen.blit(button, (180, 50))
    screen.blit(game_button, game_button_rect)  # Draw the GAME button
    screen.blit(exit_button, exit_button_rect)  # Draw the EXIT button



clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((675, 385))
pygame.display.set_caption("SCOOL")
icon = pygame.image.load("=3/icon.png").convert_alpha()
pygame.display.set_icon(icon)

bg = pygame.image.load( "=3/background.jpg").convert_alpha()
player = pygame.image.load("=3/person/9.png").convert_alpha()
walk_left = [
    pygame.image.load("=3/person/9.png").convert_alpha(),
    pygame.image.load( "=3/person/10.png").convert_alpha(),
    pygame.image.load( "=3/person/11.png").convert_alpha(),
    pygame.image.load( "=3/person/12.png").convert_alpha(),
]
walk_right = [
    pygame.image.load( "=3/person/5.png").convert_alpha(),
    pygame.image.load( "=3/person/6.png").convert_alpha(),
    pygame.image.load( "=3/person/7.png").convert_alpha(),
    pygame.image.load( "=3/person/8.png").convert_alpha(),
]
ghost = pygame.image.load( "=3/ghost.png").convert_alpha()
ghost_list_in_game = []

player_anim_count = 0
current_animation_frame = 0
animation_rate = 10
bg_x = 0

player_speed = 5
player_x = 150
player_y = 295

is_jump = False
jump_count = 8

bg_sound = pygame.mixer.Sound( "sounds/bg.mp3")
bg_sound.play(-1)

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 4000)

label = pygame.font.Font( "fonts/menu.ttf", 60)
lose_label = label.render("LOSE", True, (193, 196, 199))
restart_label = label.render("REPLAY", True, (115, 132, 148))
restart_label_rect = restart_label.get_rect(topleft=(250, 200))

menu_label = label.render("MENU", True, (255, 255, 255))  # Menu title
game_button = label.render("GAME", True, (255, 255, 255))  # GAME button
exit_button = label.render("EXIT", True, (255, 255, 255))  # EXIT button
game_button_rect = game_button.get_rect(topleft=(250, 150))  # Position for GAME button
exit_button_rect = exit_button.get_rect(topleft=(265, 300))  # Position for EXIT button

bullets_quantity = 100
bullet = pygame.image.load( "=3/bullet.png").convert_alpha()
bullets = []


bg_menu = pygame.image.load("=3/bg_menu.jpg").convert_alpha()

button = pygame.image.load( "=3/button2.png").convert_alpha()

gameplay = False  # Start with the menu
running = True
while running:
    keys = pygame.key.get_pressed()
    draw_menu()

    screen.blit(button,(250,250))
    if gameplay:
        screen.blit(bg, (bg_x, 0))
        screen.blit(bg, (bg_x + 675, 0))
        screen.blit(bg, (bg_x - 675, 0))
        if gameplay:
            player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))
            ghost_left()
            player_movement()
            bullet_movement()


        if keys[pygame.K_LEFT] and keys[pygame.K_UP] and bullets_quantity > 0:
            bullet_shot()
        elif keys[pygame.K_RIGHT] and keys[pygame.K_UP] and bullets_quantity > 0:
            bullet_shot()



        pygame.display.flip()
    else:
        draw_menu()
        pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if gameplay:
                if player_x < event.pos[0] < player_x + 30 and player_y < event.pos[1] < player_y + 30:
                    bullet_shot()
            else:
                if game_button_rect.collidepoint(event.pos):
                    gameplay = True
                    bg_sound.play(-1)
                    ghost_left()
                    player_movement()
                elif exit_button_rect.collidepoint(event.pos):
                    running = False
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(675, 295)))

    clock.tick(60)

pygame.quit()