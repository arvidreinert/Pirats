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
        self.water_shower = Rectangle((100,100),(300,height-150),(0,0,0),"water-floe.png")
        self.rot = 0
        self.boat_speed = (0,90)
        self.water_flow = (random.uniform(-1.5,1.5),random.randint(5,360))
        self.water_shower.set_rotation(self.water_flow[1])

    def play_game(self):
        while self.player_caught == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.boat_speed[0] += 0.5 

            x = self.boat_speed[1]*math.cos(self.boat_speed[1]/180*math.pi)
            y = self.boat_speed[1]*math.sin(self.boat_speed[1]/180*math.pi)
            x1= self.water_flow[1]*math.cos(self.water_flow[1]/180*math.pi)
            y1 = self.boat_speed[1]*math.sin(self.boat_speed[1]/180*math.pi)
            self.boat.change_position(x+x1,y+y1)
            self.boat.set_rotation(self.boat_speed[1])
    
            screen.fill((0,0,0))
            self.background.update()
            self.tutorial_view.update()
            self.boat.update()
            self.water_shower.update()
            pygame.display.update()

#main menu:
play_button = Rectangle((width/2,height/4),(width/2,height/2),(255,255,255),"play.png")
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