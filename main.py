from setup import *
from rectangle import Rectangle
#game class:
class game():
    def __init__(self):
        self.score = 0
        self.player_caught = False
        self.tutorial_view = Rectangle((230,100),(150,height-150),(0,0,0),"freeroam_controls.png")
        self.background = Rectangle((width,height),(width/2,height/2),(0,0,0),"ocean1.png")
        self.boat = Rectangle((100,100),(width/2,height/2),(0,0,0),"boat.png")
        self.rot = 0
        self.speed_multiplikator = 1
        self.boat_move = [0.1,0]

    def play_game(self):
        while self.player_caught == False:
            #here is the controller manager can also be used by multiple controlers
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.joysticks[0].stop_rumble()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.speed_multiplikator += 0.1
            print(self.boat.get_pos())
            self.boat.change_position(self.boat_move[0]*self.speed_multiplikator,self.boat_move[1]*self.speed_multiplikator)
            print(self.boat.get_pos())
            screen.fill((0,0,0))
            self.background.update()
            self.tutorial_view.update()
            self.boat.update()
            pygame.display.update()

#main menu:
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
if running == "play":
    ga = game()
    ga.play_game()