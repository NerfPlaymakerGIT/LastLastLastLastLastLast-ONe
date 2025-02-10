from save import *
from images import *

class Fighter:
    def __init__(self, name, level):
        self.name, self.level = name, level
        self.state = "Idle"

        #stats
        self.save = load_save()
        self.baseStats = self.save["gameData"]["Characters"][self.name]
        sprite_sheet = SpriteSheet()

        self.frames = {
            "Right" : sprite_sheet.frameImport(self.name, "Images", "Characters", "Fighters"),
            "Left": {}
            }
        
        self.frameIndex = 0

        for key in self.frames["Right"].keys():
            self.frames["Left"][key] = []
            for surface in self.frames["Right"][key]:
                self.frames["Left"][key].append(pygame.transform.flip(surface, True, False))

        


    def animate(self, dt):
        ANIMATION_SPEED = 10
        self.frameIndex += ANIMATION_SPEED * dt
        self.image = self.frames["Right"][self.state][int(self.frameIndex % len(self.frames["Right"][self.state])-1)]
        

    def update(self, dt):
        self.animate(dt)

class Enemy:
    def __init__(self, name, level, dir):
        self.name = name
        self.level = level
        self.direction = dir

        #stats
        self.save = load_save()
        self.baseStats = self.save["gameData"]["Monsters"][self.name]
        self.frames = {}
        self.frameIndex = 0

        sprite_sheet = SpriteSheet()

        self.frames = {
            "Right" : sprite_sheet.frameImport(self.name, "Images", "Characters", "Monsters"),
            "Left": {}
            }
        
        self.frameIndex = 0

        for key in self.frames["Right"].keys():
            self.frames["Left"][key] = []
            for surface in self.frames["Right"][key]:
                self.frames["Left"][key].append(pygame.transform.flip(surface, True, False))
    
    def animate(self, dt):
        ANIMATION_SPEED = 10
        self.frameIndex += ANIMATION_SPEED * dt
        self.image = self.frames[self.direction][self.state][int(self.frameIndex % len(self.frames[self.direction][self.state])-1)]
        

    def update(self, dt):
        self.animate(dt)
        




        


