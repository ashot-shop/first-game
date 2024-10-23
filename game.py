import pygame

image_path = '/data/data/org.test.myapp/files/app/'

clock = pygame.time.Clock()
#Hello
pygame.init()
screen = pygame.display.set_mode((675,385))
pygame.display.set_caption("SCOOL")#надпись сверху над игрой(ее название)
icon = pygame.image.load(image_path + "=3/icon.png").convert_alpha()#иконка игры
pygame.display.set_icon(icon)


bg = pygame.image.load(image_path + "=3/background.jpg").convert_alpha()#картинка заднего фона
# bg_2 = pygame.image.load(image_path + "=3/background_2.jpg").convert_alpha()#картинка заднего фона №2
player = pygame.image.load(image_path + "=3/person/9.png").convert_alpha()#иконка игрока
walk_left = [
    pygame.image.load(image_path + "=3/person/9.png").convert_alpha(),
    pygame.image.load(image_path + "=3/person/10.png").convert_alpha(),
    pygame.image.load(image_path + "=3/person/11.png").convert_alpha(),
    pygame.image.load(image_path + "=3/person/12.png").convert_alpha(),
]#анимация ходьбы игрока влево
walk_right = [
    pygame.image.load(image_path + "=3/person/5.png").convert_alpha(),
    pygame.image.load(image_path + "=3/person/6.png").convert_alpha(),
    pygame.image.load(image_path + "=3/person/7.png").convert_alpha(),
    pygame.image.load(image_path + "=3/person/8.png").convert_alpha(),
]#анимация ходьбы игрока вправо

ghost = pygame.image.load(image_path + "=3/ghost.png").convert_alpha()#иконка призрака
ghost_list_in_game = []

player_anim_count = 0
bg_x = 0

player_speed = 5
player_x = 150
player_y = 295

is_jump = False
jump_count = 8

bg_sound = pygame.mixer.Sound(image_path + "sounds/bg.mp3")#звук шагов НАДО ЗАЦИКЛИТЬ!
bg_sound.play(-1)


ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 4000)

label = pygame.font.Font(image_path + "fonts/menu.ttf", 60)#надпись
lose_label = label.render("LOSE", True, (193, 196, 199))#надпись
restart_label = label.render("REPLAY", True, (115, 132, 148))#надпись
restart_label_rect = restart_label.get_rect(topleft = (250,200))#надпись

bullets_quantity = 5 #количество снарядов в игре
bullet = pygame.image.load(image_path + "=3/bullet.png").convert_alpha() #картинка пули
bullets = [] #список пуль


gameplay = True

running = True
while running:
    keys = pygame.key.get_pressed()

    screen.blit(bg, (bg_x,0))
    screen.blit(bg, (bg_x+675,0))
    screen.blit(bg, (bg_x-675, 0))
    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if ghost_list_in_game:
            for (i, el) in enumerate(ghost_list_in_game):
                screen.blit(ghost, el)
                el.x -= 10

                if el.x < -10: #удаляем улетевших призраков
                    ghost_list_in_game.pop(i)

                if player_rect.colliderect(el): #если игрок столкнется с призраком, то конец
                    gameplay = False
                    bg_sound.stop()



        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))#движение фона враво
            bg_x += 2
        elif keys[pygame.K_RIGHT]:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))#двжиение фона влево
            bg_x -= 2
        else:
            screen.blit(pygame.image.load(image_path + "=3/person/13.png").convert_alpha(), (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT]:
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
            # bg_x -= 1.5
        if bg_x == -675 :
            bg_x = 0
        elif bg_x == 675:
            bg_x = 0




        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 4

                if el.x > 600:
                    bullets.pop(i)

                if ghost_list_in_game:
                    for (index, ghost_el) in enumerate(ghost_list_in_game):
                        if el.colliderect(ghost_el):
                            ghost_list_in_game.pop(index)
                            bullets.pop(i)

    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (280, 145))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            ghost_list_in_game.clear()
            bg_sound.play(-1)
            bullets.clear()
            bullets_quantity = 5

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(677,295)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_UP and bullets_quantity >0: # если мы находжимся в игре и мы нажали на стрелочку вверх, то
            bullets.append(bullet.get_rect(topleft = (player_x+30, player_y+10))) #в список пуль добавляется одна пуля в кордах игрока +30 +10
            bullets_quantity -= 1

    clock.tick(15)