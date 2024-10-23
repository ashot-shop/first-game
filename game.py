import pygame

def bullet_shot():
    global bullets
    global bullets_quantity    
    bullets.append(bullet.get_rect(topleft = (player_x + 30, player_y + 10))) 
    bullets_quantity -= 1

def draw_menu():
    screen.fill((87, 88, 89))  # Background color for the menu
    screen.blit(menu_label, (250, 100))  # Draw the menu title
    screen.blit(game_button, game_button_rect)  # Draw the GAME button
    screen.blit(exit_button, exit_button_rect)  # Draw the EXIT button

image_path = '/data/data/org.test.myapp/files/app/'

clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((675, 385))
pygame.display.set_caption("SCOOL")
icon = pygame.image.load(image_path + "=3/icon.png").convert_alpha()
pygame.display.set_icon(icon)

bg = pygame.image.load(image_path + "=3/background.jpg").convert_alpha()
player = pygame.image.load(image_path + "=3/person/9.png").convert_alpha()
walk_left = [
    pygame.image.load(image_path + "=3/person/9.png").convert_alpha(),
    pygame.image.load(image_path + "=3/person/10.png").convert_alpha(),
    pygame.image.load(image_path + "=3/person/11.png").convert_alpha(),
    pygame.image.load(image_path + "=3/person/12.png").convert_alpha(),
]
walk_right = [
    pygame.image.load(image_path + "=3/person/5.png").convert_alpha(),
    pygame.image.load(image_path + "=3/person/6.png").convert_alpha(),
    pygame.image.load(image_path + "=3/person/7.png").convert_alpha(),
    pygame.image.load(image_path + "=3/person/8.png").convert_alpha(),
]
ghost = pygame.image.load(image_path + "=3/ghost.png").convert_alpha()
ghost_list_in_game = []

player_anim_count = 0
bg_x = 0

player_speed = 5
player_x = 150
player_y = 295

is_jump = False
jump_count = 8

bg_sound = pygame.mixer.Sound(image_path + "sounds/bg.mp3")
bg_sound.play(-1)

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 4000)

label = pygame.font.Font(image_path + "fonts/menu.ttf", 60)
lose_label = label.render("LOSE", True, (193, 196, 199))
restart_label = label.render("REPLAY", True, (115, 132, 148))
restart_label_rect = restart_label.get_rect(topleft=(250, 200))

menu_label = label.render("MENU", True, (255, 255, 255))  # Menu title
game_button = label.render("GAME", True, (255, 255, 255))  # GAME button
exit_button = label.render("EXIT", True, (255, 255, 255))  # EXIT button
game_button_rect = game_button.get_rect(topleft=(250, 100))  # Position for GAME button
exit_button_rect = exit_button.get_rect(topleft=(250, 200))  # Position for EXIT button

bullets_quantity = 5
bullet = pygame.image.load(image_path + "=3/bullet.png").convert_alpha()
bullets = []

gameplay = False  # Start with the menu
running = True
while running:
    keys = pygame.key.get_pressed()

    if gameplay:
        screen.blit(bg, (bg_x, 0))
        screen.blit(bg, (bg_x + 675, 0))
        screen.blit(bg, (bg_x - 675, 0))
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if ghost_list_in_game:
            for (i, el) in enumerate(ghost_list_in_game):
                screen.blit(ghost, el)
                el.x -= 10

                if el.x < -10:
                    ghost_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False
                    bg_sound.stop()

        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
            bg_x += 2
        elif keys[pygame.K_RIGHT]:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))
            bg_x -= 2
        else:
            screen.blit(pygame.image.load(image_path + "=3/person/13.png").convert_alpha(), (player_x, player_y))

        if keys[pygame.K_LEFT] and keys[pygame.K_SPACE]:
            bullet_shot()
        elif keys[pygame.K_RIGHT] and keys[pygame.K_SPACE]:
            bullet_shot()

        for bullet_rect in bullets:
            screen.blit(bullet, bullet_rect)
            bullet_rect.x += 10

            if bullet_rect.x > 675:
                bullets.remove(bullet_rect)

        player_anim_count += 0.5
        if player_anim_count >= 4:
            player_anim_count = 0

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
                elif exit_button_rect.collidepoint(event.pos):
                    running = False
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(675, 295)))

    clock.tick(60)

pygame.quit()