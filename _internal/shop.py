from settings import *
from save import *
from PIL import Image
from os.path import join
from images import SpriteSheet
from button import *

class TalkTuah:
    def __init__(self, fighters, font):

        self.screen = pygame.display.get_surface()
        self.font = font
        self.fighters = fighters

        self.button = Button(100, 50, self.font)

        self.frameGenerator = SpriteSheet()

        self.save = load_save()
        self.coins = self.save["gameData"]["Coins"]

        self.stats = {}

        self.d = {
            3 : "LiuKang",
            2 : "Wizard", 
            1 : "Vergil"
        }




        self.tintSurface = pygame.Surface((resX, resY))
        self.tintSurface.set_alpha(200)

        #dimenzije

        self.mainRect = pygame.FRect(0, 0, resX*0.8, resY*0.8).move_to(center = (resX/2, resY/2))

        #liste svih likova
        self.visibleItems = 3
        self.listWidth = self.mainRect.width * 0.3
        self.itemHeight = self.mainRect.height / self.visibleItems
        self.index = 1

        self.selectedIndex = None

    def displayList(self):
        ind = 0
        vOffset = 0 if self.index < self.visibleItems else -(self.index - self.visibleItems) * self.itemHeight
        for index, fighter in self.fighters.items():
            ind += 1
            #boje
            bgColor = (25, 25, 25) if ind != self.index else (90, 90, 90)
            txtColor = (255, 255, 255) if self.selectedIndex != ind else (255, 215, 0)
            top = self.mainRect.top + ind * self.itemHeight - 125 + vOffset
            itemRect = pygame.FRect(self.mainRect.left, top, self.listWidth, self.itemHeight)

            textSurf = self.font.render(index, True, txtColor)
            textRect = textSurf.get_frect(midleft = itemRect.midleft + vector(45, 0))

            if itemRect.colliderect(self.mainRect):
                #added the +3 in the vector because they would not collide since the drawing is a bit weird i guess
                if itemRect.collidepoint(self.mainRect.topleft + vector(0, 3)):
                    pygame.draw.rect(self.screen, bgColor, itemRect, 0, 0, 12)
                elif itemRect.collidepoint(self.mainRect.bottomleft + vector(1, -1)):
                    pygame.draw.rect(self.screen, bgColor, itemRect, 0, 0, 0, 0, 12, 0)

            #crtanje
                else:
                    pygame.draw.rect(self.screen, bgColor, itemRect)
                self.screen.blit(textSurf, textRect)

                if itemRect.collidepoint(pygame.mouse.get_pos()):
                    self.index = ind
                    if pygame.mouse.get_just_pressed()[0] == True and self.save["gameData"]["Characters"][self.d[self.index]]["Obtained"]["Val"] == True:
                        self.selectedIndex = self.index

        for i in range(min(self.visibleItems, len(self.fighters))):
            if i == 0:
                pygame.draw.line(self.screen, (100, 100, 100), (self.mainRect.left + 8, (self.mainRect.top + self.itemHeight * i + 3)), (self.mainRect.left + self.listWidth, self.mainRect.top + self.itemHeight * i + 3))
            else:
                pygame.draw.line(self.screen, (100, 100, 100), (self.mainRect.left + 0, (self.mainRect.top + self.itemHeight * i + 3)), (self.mainRect.left + self.listWidth, self.mainRect.top + self.itemHeight * i + 3))

        
        shadowSurf = pygame.Surface((4, self.mainRect.height + 3))
        shadowSurf.set_alpha(25)
        self.screen.blit(shadowSurf, (self.mainRect.left + self.listWidth, self.mainRect.top))      

    def input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_w]:
            if self.index <= 0:
                self.index = 2
            else:
                self.index -= 1 

        if keys[pygame.K_s]:
            if self.index == 3:
                self.index = 1
            else:
                self.index += 1


        if keys[self.save["controls"]["Navigation"]["Start"]] and self.save["gameData"]["Characters"][self.d[self.index]]["Obtained"]["Val"] == True:
            self.selectedIndex = self.index

    def displayMain(self, dt):
        color = (0, 0, 0)
        #borac
        if self.index == 0:
            self.index = 3
        fighter = self.fighters[self.d[self.index]]
        if fighter.name == "LiuKang":
            color = (45, 45, 45)

        if fighter.name == "Wizard":
            color = (227, 90, 77)

        if fighter.name == "Vergil":
            color = (190, 3, 252)



        #pozadina
        rect = pygame.FRect(self.mainRect.left + self.listWidth, self.mainRect.top+3, self.mainRect.width - self.listWidth, self.mainRect.height)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 0, 12, 0, 12, 0)

        topRect = pygame.FRect(rect.topleft, (rect.width, rect.height * 0.338))
        pygame.draw.rect(self.screen, color, topRect, 0, 0, 0, 12, 0)


        fighter.update(dt)
        fighterSurf = fighter.image
        fighterRect = fighterSurf.get_frect(center = (topRect.centerx - 10, self.mainRect.top + rect.height*0.20))
        self.screen.blit(fighterSurf, fighterRect)

        LevelSurf = self.font.render(f"Level: {fighter.level}", False, (255, 255, 255))
        LevelRect = LevelSurf.get_frect(bottomleft = topRect.bottomleft + vector(10, -10))
        self.screen.blit(LevelSurf, LevelRect)


        #stats display

        stats = self.save["gameData"]["Characters"][fighter.name]
        coins = self.coins
        sheet = Image.open(join("Images", "Loading screens", "coin.png"))
        self.coinFrames = self.frameGenerator.imageImport(9, sheet.height, sheet.height, 1, "Images", "Loading screens", "coin.png")
        if stats["Obtained"]["Val"] == False:
            price = stats["Obtained"]["Price"]
            sheet = Image.open(join("Images", "Loading screens", "coin.png"))
            coinRect = self.coinFrames[0].get_frect(center = LevelRect.center + vector(150, 150))

            priceColor = (255, 255, 255) if coins >= price else (255, 100, 100)

            priceSurf = self.font.render(f"{price}", False, priceColor)
            priceRect = priceSurf.get_frect(center = LevelRect.center + vector(100, 150))

            buy = self.button.CreateButton("Acquire", priceRect.center - vector(-15, -50), priceColor)
            buySurf = buy[0]
            buyRect = buy[1]
            
            self.screen.blit(self.coinFrames[0], coinRect)
            self.screen.blit(priceSurf, priceRect)
            self.screen.blit(buySurf, buyRect)


            if pygame.mouse.get_just_pressed()[0]:
                if buyRect.collidepoint(pygame.mouse.get_pos()):
                    if self.coins < price:
                        print("Can't purchase")
                    else:
                        pygame.mixer.Sound(join("sfx", "Shop", "Acquire.wav")).play()
                        self.coins -= price
                        self.save["gameData"]["Coins"] = self.coins
                        self.save["gameData"]["Characters"][fighter.name]["Obtained"]["Val"] = True
                        write_save(self.save, join("Data", "save.json"))
                        self.save = load_save()
        else:
            for i, key in enumerate(stats):
                if key == "Level" or key == "Obtained":
                    continue


                statSurf = self.font.render(f"{key}: {stats[key]["Val"]}", False, (255, 255, 255))
                statsRect = statSurf.get_frect(bottomleft = LevelRect.bottomleft + vector(0, 50*(i+1)))
                self.screen.blit(statSurf, statsRect)

                coinRect = self.coinFrames[0].get_frect(bottomleft = LevelRect.bottomleft + vector(300, 50*(i+1)-2))

                priceColor = (255, 255, 255) if coins >= stats[key]["Price"] else (255, 100, 100)

                priceSurf = self.font.render(f"{stats[key]["Price"]}", False, priceColor)
                priceRect= priceSurf.get_frect(bottomleft = LevelRect.bottomleft + vector(275, 50*(i+1)))

                self.screen.blit(self.coinFrames[0], coinRect)
                self.screen.blit(priceSurf, priceRect)

                if pygame.mouse.get_just_pressed()[0]:
                    if priceRect.collidepoint(pygame.mouse.get_pos()):
                        if self.coins >= stats[key]["Price"]:
                            pygame.mixer.Sound(join("sfx", "Shop", "Purchase.wav")).play()
                            self.coins -=  stats[key]["Price"]
                            self.save["gameData"]["Coins"] = self.coins
                            self.save["gameData"]["Characters"][fighter.name][key]["Val"] += 2
                            self.save["gameData"]["Characters"][fighter.name][key]["Price"] += int(self.save["gameData"]["Characters"][fighter.name][key]["Price"]/10)
                            write_save(self.save, join("Data", "save.json"))
                            self.save = load_save()
                        else:
                            print("Can't purchase")



    def update(self, dt):
       self.input()
       self.screen.blit(self.tintSurface, (0, 0))
       self.displayList()
       self.displayMain(dt)


    




