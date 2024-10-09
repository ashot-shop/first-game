import pygame

pygame.init()
screen = pygame.display.set_mode((600,300))
pygame.display.set_caption("SCOOL")
icon = pygame.image.load("=3/icon.png")
pygame.display.set_icon(icon)

square = pygame.Surface((50,170))
square.fill("Blue")

myfont = pygame.font.Font("fonts/RobotoMono-Medium.ttf",50)
text_surface = myfont.render("sChOOL is COOL", True, "Yellow")

player = pygame.image.load("=3/icon.png")


running = True
while running:
    screen.fill((169,217,93))


    screen.blit(square, (10,7))
    screen.blit(text_surface, (100,100))
    screen.blit(player, (50,2))

    pygame.draw.circle(screen, "White", (10,7), 5)


    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()


