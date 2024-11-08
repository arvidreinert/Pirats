from setup import *
from rectangle import Rectangle
import time

#game class:
class game():
    def __init__(self):
        pygame.display.set_caption("CHASE THE SEA")
        self.score = 0
        self.enenmy_counter = 0
        self.enenmies = {}
        self.enemy_speed_multiplier = 0.9
        self.start_time = time.time()
        self.my_font = pygame.font.SysFont('Rage Italic', 100)
        self.text_surface = self.my_font.render(str(self.score), False, (0, 0, 0))
        self.inventory = {"banana":0,"fish":0,"metal":0,"coconuts":0,"trophies":0}
        self.visited_continents = []
        self.waiting_tavern_tap = False
        self.waiting_conttap = False
        self.reward_count = False
        self.player_caught = False
        self.reward_shower = Rectangle((width/2,height/2),(width/2,height/2),(0,0,0),"metal_reward.png")
        self.cont1 = Rectangle((width/2.75,height/2.75),(width/2+800,height/2),(0,0,0),"continent1.png")
        self.cont2 = Rectangle((width/2.75,height/2.75),(width/2+2400,height/2+700),(0,0,0),"continent2.png")
        self.cont3 = Rectangle((width/2.75,height/2.75),(-width/2,-500),(0,0,0),"continent3.png")
        self.cont4 = Rectangle((width/2.7,height/2.7),(width+500,-250),(0,0,0),"continent4.png")
        self.home_island = Rectangle((width/2.6,height/2.6),(-width/2,height/2+800),(0,0,0),"home island.png")
        self.tutorial_view = Rectangle((230,100),(120,height-120),(0,0,0),"freeroam_controls.png")
        self.background = Rectangle((width*3,height*3),(width/2,height/2),(0,0,0),"ocean1.png")
        #thanks to "tree" on png tree for the free boat image link here:https://pngtree.com/tree_4021051?type=1,https://pngtree.com/freepng/pirate-ship-top-down-view_15791217.html 
        self.boat = Rectangle((150,100),(width/2,height/2),(0,0,0),"boat.png")
        self.rot = 0
        self.water_flow = (random.uniform(-0.7,0.7),random.randint(5,360))
        self.water_shower = Rectangle((100,100*(self.water_flow[0]+1)),(300,height-150),(0,0,0),"water-floe.png")
        #self.water_shower.set_rotation(self.water_flow[1])
        #-self.boat_speed[1]
        self.boat_speed = (0,self.water_flow[1])
        self.water_shower.change_rotation(-90-self.water_flow[1])
        print(self.boat_speed)
        self.boat.change_rotation(-self.boat_speed[1])

    def taverne(self):
        pygame.mixer.Channel(1).set_volume(1)
        pygame.mixer.Channel(1).stop()
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("door-open.mp3"))
        screen.fill((0,0,0))
        play_button = Rectangle((width/2,height/4),(width/2,height/2),(255,255,255),"sell_stuff_b.png")
        leave_button = Rectangle((width/2,height/4),(width/2,height/2+height/4+50),(255,255,255),"leave_button.png")
        background = Rectangle((width,height),(width/2,height/2),(255,255,255), "tavern.jpg")
        running = True

        while running == True:
            clock.tick(30)
            mous_pos = pygame.mouse.get_pos()
            if play_button.get_point_collide(mous_pos):
                play_button.set_transparency(100)
            else:
                play_button.set_transparency(255)

            if leave_button.get_point_collide(mous_pos):
                leave_button.set_transparency(100)
            else:
                leave_button.set_transparency(255)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                #here is the button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.get_point_collide(mous_pos):
                        print("click")
                        screen.fill((0,0,0))
                        running = "sell"
                        for key in self.inventory:
                            if key == "banana":
                                self.score += self.inventory[key]*2
                                self.inventory[key] = 0
                            elif key == "fish":
                                self.score += self.inventory[key]*4
                                self.inventory[key] = 0
                            elif key == "trophies":
                                self.score += self.inventory[key]*6
                                self.inventory[key] = 0
                            elif key == "coconuts":
                                self.score += self.inventory[key]*3
                                self.inventory[key] = 0
                            elif key == "metal":
                                self.score += self.inventory[key]*5
                                self.inventory[key] = 0
                            self.visited_continents = []
                            pygame.mixer.Channel(1).play(pygame.mixer.Sound("wood-door-cl.mp3"))

                    if leave_button.get_point_collide(mous_pos):
                        print("click")
                        screen.fill((0,0,0))
                        running = "play"
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound("wood-door-cl.mp3"))

            if running == True:
                screen.fill((0,0,0))
                background.update(screen)
                play_button.update(screen)
                leave_button.update(screen)
                pygame.display.update()

    def play_game(self):
        multiplier = 1
        self.visited_continents = []
        while self.player_caught == False:
            if pygame.mixer.Channel(0).get_busy() == False:
                pygame.mixer.Channel(0).play(pygame.mixer.Sound("water-strea.mp3"))
                pygame.mixer.Channel(1).set_volume(2)
            if pygame.mixer.Channel(1).get_busy() == False and len(self.enenmies) >= 1:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound("battle-ship-111902.mp3"))
                pygame.mixer.Channel(1).set_volume(0.075)
            clock.tick(30)
            #enemy movement
            for enemy in self.enenmies:
                x0,y0 = self.enenmies[enemy][0].get_pos()
                x1,y1 = self.boat.get_pos()
                x = math.degrees(math.atan2(y1-y0, x1-x0))
                self.enenmies[enemy][0].set_rotation(x*-1)
                enemy_moves = self.enenmies[enemy][1]
                if enemy_moves != []:
                    self.enenmies[enemy][0].change_position(enemy_moves[0]*self.enemy_speed_multiplier,enemy_moves[1]*self.enemy_speed_multiplier)
                xdist = self.boat.get_pos()[0]-self.enenmies[enemy][0].get_pos()[0]
                ydist = self.boat.get_pos()[1]-self.enenmies[enemy][0].get_pos()[1]
                dist = math.sqrt(xdist*xdist+ydist*ydist)
                self.enenmies[enemy][1] = [xdist/dist,ydist/dist,]
                if self.boat.get_colliding_with(self.enenmies[enemy][0]):
                    self.player_caught = True

            mous_pos = pygame.mouse.get_pos()
            if self.reward_count != False:
                if self.reward_count >= 1:
                    self.reward_count -= 1
                else: 
                    self.reward_count = False
            if self.boat.get_colliding_with(self.home_island):
                self.tutorial_view.set_image("island_tutorial.png")
                self.waiting_tavern_tap = True
            else:
                self.waiting_tavern_tap = False
            if self.boat.get_colliding_with(self.cont1) == True:
                self.boat_speed = self.boat_speed[0]-0.001,self.boat_speed[1]
                if "1" not in self.visited_continents:
                    self.tutorial_view.set_image("continent_tutorial.png")
                    self.waiting_conttap = "1"
            elif self.boat.get_colliding_with(self.cont2) == True:
                self.boat_speed = self.boat_speed[0]-0.001,self.boat_speed[1]
                if "2" not in self.visited_continents:
                    self.tutorial_view.set_image("continent_tutorial.png")
                    self.waiting_conttap = "2"
            elif self.boat.get_colliding_with(self.cont3) == True:
                if "3" not in self.visited_continents:
                    self.tutorial_view.set_image("continent_tutorial.png")
                    self.waiting_conttap = "3"
                    self.boat_speed = self.boat_speed[0]-0.001,self.boat_speed[1]
            elif self.boat.get_colliding_with(self.cont4) == True:
                self.boat_speed = self.boat_speed[0]-0.001,self.boat_speed[1]
                if "4" not in self.visited_continents:
                    self.tutorial_view.set_image("continent_tutorial.png")
                    self.waiting_conttap = "4"
            else:
                counter = 0
                for key in self.inventory:
                    counter += self.inventory[key]
                if self.waiting_tavern_tap != True and counter == 0:
                    self.waiting_conttap = False
                    self.tutorial_view.set_image("freeroam_controls.png")
                elif counter >= 1 and self.waiting_tavern_tap != True and self.waiting_conttap != True:
                    self.tutorial_view.set_image("tutorial_sail_home.png")

            if self.boat.get_colliding_with(self.background) == False:
                self.background.set_position(width/2,height/2)
                self.cont1.set_position(width/2+800,height/2)
                self.cont2.set_position(width/2+2400,height/2+700)
                self.cont3.set_position(-width/2,-500)
                self.cont4.set_position(width+500,-250)
                self.home_island.set_position(-width/2,height/2+800)
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
                        if self.boat_speed[0]+0.095 <= 1.5:
                            self.boat_speed = self.boat_speed[0]+0.095,self.boat_speed[1]
                    if event.key == pygame.K_LEFT:
                        self.boat_speed = self.boat_speed[0],self.boat_speed[1]-1*multiplier
                        self.boat.change_rotation(1*multiplier)
                    if event.key == pygame.K_RIGHT:
                        self.boat_speed = self.boat_speed[0],self.boat_speed[1]+1*multiplier
                        self.boat.change_rotation(-1*multiplier)
                    if event.key == pygame.K_DOWN:
                        if self.boat_speed[0]-0.095 >= -1.5:
                            self.boat_speed = self.boat_speed[0]-0.095,self.boat_speed[1]
                    if event.key == pygame.K_SPACE:
                        multiplier = 1
                        self.boat_speed = 0,self.boat_speed[1]
                #managing the tap on the continent
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.home_island.get_point_collide(mous_pos) and self.waiting_tavern_tap:
                        screen.fill((0,0,0))
                        self.waiting_tavern_tap = False
                        self.taverne()
                    if self.waiting_conttap != False:
                        if self.cont1.get_point_collide(mous_pos) or self.cont2.get_point_collide(mous_pos) or self.cont3.get_point_collide(mous_pos) or self.cont4.get_point_collide(mous_pos):
                            self.visited_continents.append(self.waiting_conttap)
                            self.waiting_conttap = False
                            self.reward_count = 60
                            x = Rectangle((150,100),(random.randint(0,round(width)),random.randint(0,round(height/4))),(0,0,0),"boat.png")
                            x0,y0 = x.get_pos()
                            x1,y1 = self.boat.get_pos()
                            x.change_rotation(math.atan2(y1-y0,x1-x0)-(math.pi/2))
                            self.enenmies[f"enemy{self.enenmy_counter}"] = [x,[0,0]]
                            self.enenmy_counter += 1
                            self.enemy_speed_multiplier += 0.1
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
            self.home_island.change_position(movement[0],movement[1])
            for enemy in self.enenmies:
                self.enenmies[enemy][0].change_position(movement[0],movement[1])
    
            screen.fill((0,130,255))
            self.background.update(screen)
            self.cont1.update(screen)
            self.cont2.update(screen)
            self.cont3.update(screen)
            self.home_island.update(screen)
            self.cont4.update(screen)
            for enemy in self.enenmies:
                self.enenmies[enemy][0].update(screen)

            self.tutorial_view.update(screen)
            self.boat.update(screen)
            self.water_shower.update(screen)
            self.text_surface = self.my_font.render(f"{str(self.score)}$", False, (0, 0, 0))
            screen.blit(self.text_surface, (width/2,120))
            if self.reward_count != False:
                self.reward_shower.update(screen)
            pygame.display.update()
        #player died:
        running = True
        end = time.time()
        self.background = Rectangle((width,height),(width/2,height/2),(255,255,255), "menu.jpg")
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("click")
                    screen.fill((0,0,0))

            screen.fill((255,255,255))
            self.background.update(screen)
            self.my_font = pygame.font.SysFont('Rage Italic', 62)
            text = f" you played for {round(end-self.start_time,3)} seconds before you were caught with {str(self.score)}$ in total!"
            self.text_surface = self.my_font.render(str(text), False, (50,50,50))
            screen.blit(self.text_surface, (150,height/2))
            pygame.display.update()

#main menu:
play_button = Rectangle((width/2,height/4),(width/2,height/2-200),(255,255,255),"play.png")
cr = Rectangle((width,height),(width/2,height/2),(255,255,255),"credits.png")
cr_button = Rectangle((width/2,height/4),(width/2,height/2-200+height/4),(255,255,255),"credits_butoon.png")
background = Rectangle((width,height),(width/2,height/2),(255,255,255), "menu.jpg")
while True:
    running = True
    while running == True:
        clock.tick(30)
        mous_pos = pygame.mouse.get_pos()
        if play_button.get_point_collide(mous_pos):
            play_button.set_transparency(100)
        else:
            play_button.set_transparency(255)

        if cr_button.get_point_collide(mous_pos):
            cr_button.set_transparency(100)
        else:
            cr_button.set_transparency(255)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            #here is the button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.get_point_collide(mous_pos):
                    print("click")
                    screen.fill((0,0,0))
                    running = "play"
                if cr_button.get_point_collide(mous_pos):
                    running = "credits"
                    screen.fill((0,0,0))
                    print(True)
                    r = True
                    while r:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                sys.exit()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                r = False
                                running = True
                        screen.fill((0,0,0))
                        cr.update(screen)
                        pygame.display.update()

        if running == True:
            background.update(screen)
            cr_button.update(screen)
            play_button.update(screen)
            pygame.display.update()

    print(running)
    if running == "play":
        ga = game()
        ga.play_game()