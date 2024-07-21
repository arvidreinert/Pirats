from setup import *
from rectangle import Rectangle
#game class:
class game():
    def __init__(self):
        self.score = 0
        self.inventory = {"banana":0,"fish":0,"metal":0,"coconuts":0,"trophies":0}
        self.visited_continents = []
        self.waiting_conttap = False
        self.reward_count = False
        self.player_caught = False
        self.reward_shower = Rectangle((width/2,height/2),(width/2,height/2),(0,0,0),"metal_reward.png")
        self.cont1 = Rectangle((width/2.75,height/2.75),(width/2+800,height/2),(0,0,0),"continent1.png")
        self.cont2 = Rectangle((width/2.75,height/2.75),(width/2+2400,height/2+700),(0,0,0),"continent2.png")
        self.cont3 = Rectangle((width/2.75,height/2.75),(-width/2,-500),(0,0,0),"continent3.png")
        self.cont4 = Rectangle((width/2.7,height/2.7),(width+500,-250),(0,0,0),"continent4.png")
        self.tutorial_view = Rectangle((230,100),(120,height-120),(0,0,0),"freeroam_controls.png")
        self.background = Rectangle((width*3,height*3),(width/2,height/2),(0,0,0),"ocean1.png")
        self.boat = Rectangle((100,100),(width/2,height/2),(0,0,0),"boat.png")
        self.rot = 0
        self.water_flow = (random.uniform(-0.7,0.7),random.randint(5,360))
        self.water_shower = Rectangle((100,100*(self.water_flow[0]+1)),(300,height-150),(0,0,0),"water-floe.png")
        #self.water_shower.set_rotation(self.water_flow[1])
        #-self.boat_speed[1]
        self.boat_speed = (0,self.water_flow[1])
        self.water_shower.change_rotation(-90-self.water_flow[1])
        print(self.boat_speed)
        self.boat.change_rotation(-self.boat_speed[1])

    def play_game(self):
        multiplier = 1
        self.visited_continents = []
        while self.player_caught == False:
            clock.tick(30)
            mous_pos = pygame.mouse.get_pos()
            if self.reward_count != False:
                if self.reward_count >= 1:
                    self.reward_count -= 1
                else: 
                    self.reward_count = False
            if self.boat.get_colliding_with(self.cont1) == True and "1" not in self.visited_continents:
                self.tutorial_view.set_image("continent_tutorial.png")
                self.waiting_conttap = "1"
            elif self.boat.get_colliding_with(self.cont2) == True and "2" not in self.visited_continents:
                self.tutorial_view.set_image("continent_tutorial.png")
                self.waiting_conttap = "2"
            elif self.boat.get_colliding_with(self.cont3) == True and "3" not in self.visited_continents:
                self.tutorial_view.set_image("continent_tutorial.png")
                self.waiting_conttap = "3"
            elif self.boat.get_colliding_with(self.cont4) == True and "4" not in self.visited_continents:
                self.tutorial_view.set_image("continent_tutorial.png")
                self.waiting_conttap = "4"
            else:
                self.waiting_conttap = False
                self.tutorial_view.set_image("freeroam_controls.png")

            if self.boat.get_colliding_with(self.background) == False:
                self.background.set_position(width/2,height/2)
                self.cont1.set_position(width/2+800,height/2)
                self.cont2.set_position(width/2+2400,height/2+700)
                self.cont3.set_position(-width/2,-500)
                self.cont4.set_position(width+500,-250)
            for event in pygame.event.get():
                #inputs
                if event.type == pygame.QUIT:
                    sys.exit()
                #shift in or decrease the stearing 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RSHIFT:
                        multiplier += 1
                    if event.key == pygame.K_LSHIFT:
                        if multiplier >= 2:
                            multiplier -= 1
                    if event.key == pygame.K_UP:
                        if self.boat_speed[0]+0.095 <= 5:
                            self.boat_speed = self.boat_speed[0]+0.095,self.boat_speed[1]
                    if event.key == pygame.K_LEFT:
                        self.boat_speed = self.boat_speed[0],self.boat_speed[1]-1*multiplier
                        self.boat.change_rotation(1*multiplier)
                    if event.key == pygame.K_RIGHT:
                        self.boat_speed = self.boat_speed[0],self.boat_speed[1]+1*multiplier
                        self.boat.change_rotation(-1*multiplier)
                    if event.key == pygame.K_DOWN:
                        if self.boat_speed[0]-0.095 >= -1:
                            self.boat_speed = self.boat_speed[0]-0.095,self.boat_speed[1]
                    if event.key == pygame.K_SPACE:
                        multiplier = 1
                        self.boat_speed = 0,self.boat_speed[1]
                #managing the tap on the continent
                if self.waiting_conttap != False:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        print(True)
                        if self.cont1.get_point_collide(mous_pos) or self.cont2.get_point_collide(mous_pos) or self.cont3.get_point_collide(mous_pos) or self.cont4.get_point_collide(mous_pos):
                            self.visited_continents.append(self.waiting_conttap)
                            self.waiting_conttap = False
                            self.reward_count = 60
                            x = random.randint(0,4)
                            print(x)
                            if x == 0:
                                self.reward_shower.set_image("metal_reward.png")
                                self.inventory["metal"] += 1
                            elif x == 1:
                                self.reward_shower.set_image("banana_reward.png")
                                self.inventory["banana"] += 1
                            elif x == 2:
                                self.reward_shower.set_image("coconut_reward.png")
                                self.inventory["coconuts"] += 1
                            elif x == 3:
                                self.reward_shower.set_image("fish_reward.png")
                                self.inventory["fish"] += 1
                            elif x == 4:
                                self.reward_shower.set_image("trophies reward.png") 
                                self.inventory["trophies"] += 1

            z = self.boat_speed[1]/180*math.pi
            w = self.water_flow[1]/180*math.pi
            #boat speed[0] = Speed boat speed[1] = rotatiomn
            x = self.boat_speed[0]*math.cos(z)
            y = self.boat_speed[0]*math.sin(z)
            x1= self.water_flow[0]*math.cos(w)
            y1 = self.water_flow[0]*math.sin(w)
            #print(y,y1,x,x1)
            movement = ((x+x1)*-1,(y+y1)*-1)
            self.background.change_position(movement[0],movement[1])
            self.cont1.change_position(movement[0],movement[1])
            self.cont2.change_position(movement[0],movement[1])
            self.cont3.change_position(movement[0],movement[1])
            self.cont4.change_position(movement[0],movement[1])
    
            screen.fill((0,0,0))
            self.background.update(screen)
            self.cont1.update(screen)
            self.cont2.update(screen)
            self.cont3.update(screen)
            self.cont4.update(screen)
            self.tutorial_view.update(screen)
            self.boat.update(screen)
            self.water_shower.update(screen)
            if self.reward_count != False:
                self.reward_shower.update(screen)
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