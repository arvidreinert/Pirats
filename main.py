from setup import *
from rectangle import Rectangle
#game class:
class game():
    def __init__(self):
        self.score = 0
        self.player_caught = False
        self.joysticks = []
        self.tutorial_view = Rectangle((230,100),(150,height-150),(0,0,0),"freeroam_controls.png")
        self.background = Rectangle((width,height),(width/2,height/2),(0,0,0),"ocean1.png")
        self.boat = Rectangle((100,100),(width/2,height/2),(0,0,0),"menu.jpg")
        self.rot = 0

    def play_game(self):
        while self.player_caught == False:
            #here is the controller manager can also be used by multiple controlers
            if pygame.joystick.get_count() >= 1 and self.joysticks == []:
                joy = pygame.joystick.Joystick(0)
                joy = (joy,joy.get_name())
                #call with [0]

                if len(self.joysticks) <= 1 and joy not in self.joysticks:
                    joy = pygame.joystick.Joystick(0)
                    joy.init()
                    print("test")
                    print(joy.rumble(1,1,160))
                    #feels like a litle punch:joy.rumble(1,1,8)
                    self.joysticks.append(joy)
            for event in pygame.event.get():
                if event.type == pygame.JOYDEVICEREMOVED:
                    del self.joysticks[0]
                elif event.type == pygame.QUIT:
                    self.joysticks[0].stop_rumble()
                    sys.exit()

            # here the controller input is used:
            if len(self.joysticks) >= 1:
                if self.joysticks[0].get_button(3) == 1:
                    print("rotate")
                    self.rot += 1
                    if self.rot >= 360:
                        self.rot = 0
                else:
                    pass
            self.boat.set_rotation(0.1)
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