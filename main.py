from setup import *
from rectangle import Rectangle
play_button = Rectangle((width/2,height/4),(width/2,height/2-height/5.5),(255,255,255),"play.png")
background = Rectangle((width,height),(width/2,height/2),(255,255,255), "menu.jpg")
running = True

while running == True:
    clock.tick(30)
    mous_pos = pygame.mouse.get_pos()
    if play_button.get_point_colide(mous_pos):
        play_button.set_transparency(100)
    else:
        play_button.set_transparency(255)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        #here is the button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.get_point_colide(mous_pos):
                print("click")
                screen.fill((0,0,0))
                running = "play"
    if running == True:
        background.update()
        play_button.update()
        pygame.display.update()
print(running)