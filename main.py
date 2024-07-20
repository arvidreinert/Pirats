from setup import *
from rectangle import Rectangle
#game class:
class game():
    def __init__(self):
        self.score = 0
        self.player_caught = False
        self.tutorial_view = Rectangle((230,100),(150,height-150),(0,0,0),"freeroam_controls.png")
        self.background = Rectangle((width*2,height*2),(width/2,height/2),(0,0,0),"ocean1.png")
        self.boat = Rectangle((100,100),(width/2,height/2),(0,0,0),"boat.png")
        self.rot = 0
        self.water_flow = (random.uniform(-0.3,0.3),random.randint(5,360))
        self.water_shower = Rectangle((100,100*(self.water_flow[0]+1)),(300,height-150),(0,0,0),"water-floe.png")
        #self.water_shower.set_rotation(self.water_flow[1])
        #-self.boat_speed[1]
        self.boat_speed = (0.1,self.water_flow[1])
        self.water_shower.change_rotation(-90-self.water_flow[1])
        print(self.boat_speed)
        self.boat.change_rotation(-self.boat_speed[1])

    def play_game(self):
        while self.player_caught == False:
            if self.boat.get_colliding_with(self.background) == False:
                self.background.set_position(width/2,height/2)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if self.boat_speed[0]+0.095 <= 1:
                            self.boat_speed = self.boat_speed[0]+0.095,self.boat_speed[1]
                    if event.key == pygame.K_LEFT:
                        self.boat_speed = self.boat_speed[0],self.boat_speed[1]-1
                        self.boat.change_rotation(1)
                    if event.key == pygame.K_RIGHT:
                        self.boat_speed = self.boat_speed[0],self.boat_speed[1]+1
                        self.boat.change_rotation(-1)
                    if event.key == pygame.K_DOWN:
                        if self.boat_speed[0]-0.095 >= -1:
                            self.boat_speed = self.boat_speed[0]-0.095,self.boat_speed[1]

            z = self.boat_speed[1]/180*math.pi
            #boat speed[0] = Speed boat speed[1] = rotatiomn
            x = self.boat_speed[0]*math.cos(z)
            y = self.boat_speed[0]*math.sin(z)
            x1= self.water_flow[0]*math.cos(z)
            y1 = self.water_flow[0]*math.sin(z)
            #print(y,y1,x,x1)
            self.background.change_position((x+x1)*-1,(y+y1)*-1)
    
            screen.fill((0,0,0))
            self.background.update(screen)
            self.tutorial_view.update(screen)
            self.boat.update(screen)
            self.water_shower.update(screen)
            pygame.display.update()

#main menu:
play_button = Rectangle((width/2,height/4),(width/2,height/2),(255,255,255),"play.png")
background = Rectangle((width,height),(width/2,height/2),(255,255,255), "menu.jpg")
running = True

while running == True:
    clock.tick(30)
    mous_pos = pygame.mouse.get_pos()
    if play_button.get_point_collide(mous_pos):
        play_button.set_transparency(100)
    else:
        play_button.set_transparency(255)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        #here is the button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.get_point_collide(mous_pos):
                print("click")
                screen.fill((0,0,0))
                running = "play"

    if running == True:
        background.update(screen)
        play_button.update(screen)
        pygame.display.update()

print(running)
if running == "play":
    ga = game()
    ga.play_game()