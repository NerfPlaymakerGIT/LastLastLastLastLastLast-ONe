from settings import *
from save import *
from stateManager import *
from button import *


#TODO
#Need to render each button individualy from save file and have it be a rect so I can check for mouse collision - #### This has been completed ####
#Due to the way way collision has been implemented just have background of button change color on collision as it being selected
#if a button is selected AND there is a mouse left click, we change game state with stateManager to whatever the button says #### Done #####
#On settings that action will put you in "chage" mode that will let you reset keybinds #### This has been completed ####
#Quit button just ends the game #### This has been completed ####
#Play button should just start the damn game #### This has been completed ####
#Settings button will actually let you edit settings and will basically be this whole file right here #### This works ####
#### everything here has been added, just need to figure out why it wont use the settings live, instead I need to reset the game for it to apply ####

####fixed this as well, needed to reload the save that was loaded into the character object so its movement would be triggered by the right keys ####

class Menu:
    def __init__(self, state):
        self.save = load_save()
        self.button = Button(200, 200, pygame.font.Font("Fonts\dpcomic.ttf", 30))
        self.click = {"Play" : False, "New Game" : False, "Options" : False, "Quit" : False}
        self.mouse = pygame.mouse.get_pos()
        self.buttons = {}
        self.prevState = state
        self.manager = GameStateManager("MainMenu")
        self.options = Options()
            
    def render(self, text, rect):
        screen.blit(text, rect)
        
        
        
    def run(self):
        while self.manager.getState() == "MainMenu":
            self.ind = 0
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 800, 800))
            for butt in self.click.keys():
                self.ind += 1
                self.buttons[butt] = [self.button.CreateButton(butt, (resX/2, resY/8+int(self.ind*70)), (255, 255, 255)), butt]
                self.render(self.buttons[butt][0][0], self.buttons[butt][0][1])
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if pygame.mouse.get_pressed()[0] == True:
                    for butt in self.buttons.values():      
                        if butt[0][1].collidepoint(pygame.mouse.get_pos()):
                            self.manager.setState(butt[1])

                        if self.manager.getState() == "Quit":
                            pygame.quit()
                            sys.exit()

                        if self.manager.getState() == "Options":
                            self.manager.setState("Options")
                            self.options.run()

                        if self.manager.getState() == "Play":
                            self.manager.setState(self.prevState if self.prevState else "Play")

                        if self.manager.getState() == "New Game":
                            self.save = create_save()


                         
            pygame.display.update()

        self.manager.setState("Play")
            
class Options:
    def __init__(self):
        self.save = load_save()
        self.button = Button(200, 200, pygame.font.Font("Fonts\dpcomic.ttf", 30))
        self.mouse = pygame.mouse.get_pos()
        self.buttons = {}
        self.manager = GameStateManager("Options")
            
    def render(self, text, rect):
        screen.blit(text, rect)

    def selected(self, button):
        if button == "Reset Keybinds":
            self.save["controls"]["Movement"] = {
            "Left" : pygame.K_a, "Right" : pygame.K_d, "Up" : pygame.K_w, "Down" : pygame.K_s, "Interact" : pygame.K_f,
            "Jump" : pygame.K_SPACE, "Sprint" : pygame.K_LCTRL, "Crouch" : pygame.K_LSHIFT, "Dash" : pygame.K_v
            }
            write_save(self.save, "Data\save.json")
            self.save = load_save()
            return
        selected = True
        while selected == True:

            butt = self.button.CreateButton("Select a button", (resX/2, resY/2), (255, 255, 255))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 800, 600))
            screen.blit(butt[0], butt[1])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        selected = False
                        return
                
                    if event.key not in self.save["controls"]["Movement"].values():
                        self.save["controls"]["Movement"][button] = event.key
                        selected = False
                        write_save(self.save, "Data\save.json")
                        self.save = load_save()
                        return
                    else:
                        print("Error, key taken")

            pygame.display.update()


        
        
        
    def run(self):
        while self.manager.getState() == "Options":
            self.x = 0
            self.ind = 0
            self.y = -50
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 800, 600))
            for butt in self.save["controls"]["Movement"].keys():
                self.ind += 1
                self.y += 100


                button = self.button.CreateButton(butt, (resX/5 + self.x, self.y), (255, 255, 255))
                self.render(button[0], button[1])


                button = self.button.CreateButton(pygame.key.name(self.save["controls"]["Movement"][butt]), (resX/2.5 + self.x, self.y), (255, 255, 255)), butt

                self.buttons[butt] = button

                self.render(button[0][0], button[0][1])
                pygame.draw.rect(screen, (255, 255, 255), (button[0][1][0]-10, button[0][1][1]-10, button[0][1][2]+20, button[0][1][3]+20), 2, 4)

                if self.ind % 5 == 0:
                    self.x += 300
                    self.y = -50

            button = self.button.CreateButton("Reset Keybinds", (resX/1.5 - 200 + self.x - 50, self.y + 100), (255, 255, 255)), "Reset Keybinds"
            self.render(button[0][0], button[0][1])
            self.buttons["Reset Keybinds"] = button

                
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.manager.setState("MainMenu")

                #This checks for collision on buttons and sends that keybind to change to the function that well, changes the keybind
                if pygame.mouse.get_pressed()[0] == True:
                    for butt in self.buttons.values():  
                        if butt[0][1].collidepoint(pygame.mouse.get_pos()):
                            self.selected(butt[1])


            pygame.display.update()