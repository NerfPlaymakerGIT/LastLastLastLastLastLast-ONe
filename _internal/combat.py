from settings import *
from stateManager import *
from menu import *
from save import *
from images import *
from characters import *
from sprites import *
from groups import AllSprites
from fighting import *

class Combat:             
    def __init__(self, fighter, level, fonts, wawe):
        pygame.init()  
        self.clock = pygame.time.Clock()
        self.manager = GameStateManager("Combat")
        self.save = load_save()
        self.menu = Menu("Combat")

        self.wawe = wawe
        self.endWawe = wawe + 10
        self.counter = 0


        self.name = fighter
        self.monsterLevel = level
        self.fonts = fonts

        #coins
        self.coins = self.save["gameData"]["Coins"]


        #groups
        self.allSprites = AllSprites()
        self.collisionSprites = pygame.sprite.Group()
        self.characterSprites = pygame.sprite.Group()
        self.monsterSprites = pygame.sprite.Group()
        self.transitionSprites = pygame.sprite.Group()

        self.takeDmg = False
        self.DealtDamage = False


        #monsters and levels

        self.sheets = SpriteSheet()
        self.monsters = {
            "Goblin" : Enemy("Goblin", self.monsterLevel, "Right"),
            "Flying eye" : Enemy("Flying eye", self.monsterLevel, "Right"),
            "Mushroom" : Enemy("Mushroom", self.monsterLevel, "Right"),
            "Skeleton" : Enemy("Skeleton", self.monsterLevel, "Right")
        }

        self.enemies = []
        self.spawnPoints = {}

        self.currTimer = 0

        self.importAssets()
        self.IAMNOTMUSIC()
        self.IAMMUSIC(join("sfx", "IAMMUSIC", "music5 combat.mp3"))



    def IAMMUSIC(self, *path):
        pygame.mixer.music.load(*path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0, 1000)

    def IAMNOTMUSIC(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()



    def importAssets(self):
        self.tmxMap =  {
            "combat" : load_pygame(join("Map","CombatArena.tmx"))
        }

        self.fighterFrames = self.sheets.frameImport(self.name, "Images", "Characters", "Fighters")

        self.sfx = {
            "Walking" : pygame.mixer.Sound(join("sfx", "walking", "walking1.mp3")),
            "Walking2": pygame.mixer.Sound(join("sfx", "walking", "walking2.mp3")),
            "EnteringCombat" : pygame.mixer.Sound(join("sfx", "transitions", "EnterCombat.wav")),
            "ExitingCombat" : pygame.mixer.Sound(join("sfx", "transitions", "ExitCombat.wav"))
            }



        self.LoadLevel(self.tmxMap["combat"], "PlayerSpawn")

    def LoadLevel(self, tmxMap, playerStartPos):
        for group in (self.allSprites, self.collisionSprites, self.characterSprites, self.transitionSprites):
                group.empty()

        for obj in tmxMap.get_layer_by_name("Collisions"):
            BorderSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collisionSprites)

        for x, y, surf in tmxMap.get_layer_by_name("Floor").tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), surf, self.allSprites)

        for x, y, surf in tmxMap.get_layer_by_name("Decor").tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), surf, self.allSprites)

        #TODO
        #Need to have a spawning "rate" and the rate is increased per wawe by growth rate(0.2) * 5 meaning it will scale slowly 
        #so new rate = growth rate * 5 + prev rate
        #then I need it to pick between 1-36 randomly and that will be the spawn point
        #OR i can give it a range with all the posible spawn chords(picks rand x and ranad y) that is not on top of the player and we gucci
        #The enemies will be spawned at intervals
        #Hopefully about 20% per idk 30 seconds or sum until the whole wawe spawns
        #Hopefully it is not too whacky
        #Also every monster kill will grant you 1 coin and that will scale somehow so I can scale the prices in the shop as well


        #TODO
        #implement actual player stats so that the stats from the save actually do something
        #Like I gain ce back at like ceRegen * 1sec or something and I need it for special abilities that can idk crit or do more dmg or sum
        #Also I forgor to add the buy lvl option, that is just gonna scale all the stats by like 1 or 2 upgrades and reduce the base price by like 20%
        #that way buying levels will make it more worth the more stats you buy so it kinda balances out
        #The actual stat prices need to scale a bit more than linearly so it works out a bit better
        for obj in tmxMap.get_layer_by_name("SpawnPoints"):
            if "EnemySpawn" in obj.name:
                self.spawnPoints[obj.name] = [obj.x, obj.y]
            if obj.name == playerStartPos:
                self.currFigther = Drututt(
                    pos = (obj.x, obj.y), 
                    frames = self.fighterFrames,
                    groups = (self.allSprites),
                    facingDirection = "Right",
                    collisionSprites = self.collisionSprites,
                    name = self.name,
                    sfx = self.sfx
                )
    def createEnemy(self, dt):
        if self.currTimer >= 1:
            a = randint(1, 32)
            enemy = choice(["Flying eye", "Goblin", "Mushroom", "Skeleton"])
            x, y = self.spawnPoints[f"EnemySpawn{a}"][0], self.spawnPoints[f"EnemySpawn{a}"][1]
            self.enemies.append(AriboLOL(
                        pos = (x, y),
                        frames = self.monsters[enemy].frames,
                        groups = (self.monsterSprites, self.allSprites),
                        facingDirection = "Right",
                        collisionSprites = self.collisionSprites,
                        name = enemy,
                        player = self.currFigther
                        ))
            self.currTimer = 0
            self.counter += 1
        else:
            self.currTimer += dt * 10

    def displayWawe(self):
        waweText = self.fonts.render(f"Wawe: {self.wawe}", False, (255, 255, 255))
        waweRect = waweText.get_frect(center = (350, 20))
        screen.blit(waweText, waweRect)






    def run(self):
        while self.manager.getState() == "Combat":
            screen.fill("black")
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                #ovo je ako bas izadje iz igrice
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu = Menu("Combat")
                        self.menu.run()
                        #mora ici oba dva zato jer se liku atributi nece sami azurirati
                        self.save = load_save()
                        self.currFigther.save = load_save()


            if self.counter <= int(self.wawe/2)+1:
                self.createEnemy(dt)

            
            for enemy in self.enemies:
                if enemy and enemy.death == False:
                    enemy.chase(self.currFigther.rect.center)
                    #ovja takeDmg je potreban zato jer ce lik primiti stetu svaki
                    #puta kad se frame generira, ovako ce primiti jednom kad ga udari
                    #i onda nece moci dok se taj hitac ne zavrsi
                    #ubiti samo da ne prima vise stete od istog udarca
                    if self.currFigther.takeHit == True:
                        if self.takeDmg == False:
                            self.currFigther.hp -= enemy.atk
                            self.takeDmg = True

                    else:
                        self.takeDmg = False

                    if self.currFigther.hp <= 0:
                        self.save["gameData"]["Wawe"] = self.endWawe - 10
                        write_save(self.save, join("Data", "save.json"))
                        self.manager.setState("Play")
            
            for enemy in self.enemies:
                if self.currFigther.attackRect != None:
                    if enemy.hitbox.colliderect(self.currFigther.attackRect):
                        enemy.takeDmg = True
                        if enemy.death == False:
                            self.DealtDamage = True
                        enemy.hp -= self.currFigther.atk
                
                if enemy.died == True:
                    enemy.kill()
                    self.coins += int(self.wawe*0.2)+1
                    enemy.died = False


            if self.DealtDamage == True:
                self.DealtDamage = False
                sound = pygame.mixer.Sound(join("sfx", "enemies", "Goblin", "TakeHit.aiff"))
                sound.set_volume(0.5)
                sound.play()

            self.currFigther.attackRect = None
            

            if self.monsterSprites.sprites() == [] and self.counter != 0:
                if self.wawe == self.endWawe:
                    self.save["gameData"]["Coins"] = self.coins
                    self.save["gameData"]["Wawe"] = self.endWawe
                    write_save(self.save, join("Data", "save.json"))
                    self.currFigther.takeHit = False
                    self.currFigther.attacking = False
                    self.currFigther.rect.center = (660, 1200)
                    self.manager.setState("Play")
                    break
                else:
                    self.counter = 0
                    self.wawe += 1
                    if self.wawe >= self.endWawe:
                        self.wawe = self.endWawe

            
           
            #crtanje
            self.allSprites.update(dt)
            self.allSprites.draw(self.currFigther.rect.center)
            self.displayWawe()
            self.currFigther.baseCE()
            self.currFigther.baseHP()
            pygame.display.update()

