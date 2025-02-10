import pygame.draw
from settings import *
from save import *
from stateManager import *


class Drututt(pygame.sprite.Sprite):
    def __init__(self, pos, frames,groups, facingDirection, collisionSprites, name, sfx):
        super().__init__(groups)

        self.sfx = sfx


        self.collisionSprites = collisionSprites


        self.save = load_save()
        self.stats = self.save["gameData"]["Characters"][name]
        self.font = pygame.font.Font(join("Fonts", "dpcomic.ttf"), 11)
        self.direction = vector()

        self.facingDirection = facingDirection
        self.frameIndex, self.frames = 0, frames
        self.to = "Idle"
        self.image = self.frames[self.to][0]
        self.rect = self.image.get_frect(center = pos)
        self.hitbox = self.rect.inflate(-self.rect.width/2, -220)

        self.attacking = False
        self.takeHit = False
        self.special = False
        self.special2 = False

        self.attackedDir = None
        self.attackRect = None


        #stats
        self.level = self.stats["Level"]
        self.hp = self.stats["HP"]["Val"]
        self.atk = self.stats["ATK"]["Val"]
        self.ce = self.stats["CE"]["Val"]
        self.ceRegen = self.stats["ceRegen"]["Val"]
        self.counter = 0

        self.cooldown = 0

        self.createHPBar()
        self.createCEBar()

    def createHPBar(self):
        image = pygame.Surface((40, 40))
        image.fill((240, 240, 240))
        self.maxHP = self.stats["HP"]["Val"]
        self.hpBarLen = 250
        self.ratio = self.maxHP / self.hpBarLen

    def baseHP(self):
        text = self.font.render(f"{int((self.hp/self.maxHP)*100)}%", False, (255, 255, 255))
        rect = text.get_frect(topleft = (16, 12))
        pygame.draw.rect(screen, (255, 0, 0), (10, 10, self.hp/self.ratio, 15))
        pygame.draw.rect(screen, (255, 255, 255), (10, 10, self.hpBarLen, 15), 2)
        screen.blit(text, rect)

    def createCEBar(self):
        image = pygame.Surface((40, 40))
        image.fill((240, 240, 240))
        self.maxCE = self.stats["CE"]["Val"]
        self.ceBarLen = 150
        self.ratio2 = self.maxCE / self.ceBarLen

    def baseCE(self):
        text = self.font.render(f"{int((self.ce/self.maxCE)*100)}%", False, (255, 255, 255))
        rect = text.get_frect(topleft = (16, 31))
        pygame.draw.rect(screen, (0, 0, 255), (10, 30, self.ce/self.ratio2, 13))
        pygame.draw.rect(screen, (255, 255, 255), (10, 30, self.ceBarLen, 13), 1)
        screen.blit(text, rect)



    def getState(self):
        moving = bool(self.direction)

        #schmooooovement logic
        if self.attacking == False and self.takeHit == False:
            if moving:
                self.to = "Move"
                if self.direction.x != 0:
                    if self.direction.x < 0:
                        self.facingDirection = "left"
                    else:
                        self.facingDirection = "right"
                    
            else:
                self.to = "Idle"

        if self.attacking == True and self.takeHit == False:
            if int(self.frameIndex % len(self.frames[self.to])-1) == len(self.frames[self.to])-2:
                self.attacking = False

            
            if int(self.frameIndex % len(self.frames[self.to])-1) == len(self.frames[self.to])-4:   
                self.attackRect = self.rect.inflate(-self.rect.width/2 - 40, -250)
                if self.facingDirection == "left":
                    self.attackRect.center = self.attackRect.centerx - 50, self.attackRect.centery
                else:
                    self.attackRect.center = self.attackRect.centerx + 50, self.attackRect.centery
            
                
        if self.takeHit == True and self.attacking == False:
            self.to = "TakeHit"
            #need to figure out a way to make it so only one hit is registerd at a time
            #like some i frames, so if player gets pulled up on
            #he does not end up in another dimension like
            #they are on the zaza
            self.rect.centerx += self.attackedDir.x * 2
            self.checkCollision("horizontal")
            self.rect.centery += self.attackedDir.y * 2
            self.hitbox.centery = self.rect.centery
            self.checkCollision("vertical")
            
            
            if int(self.frameIndex % len(self.frames[self.to])-1) == len(self.frames[self.to])-2:
                self.takeHit = False

        return f"{self.facingDirection}"
    

    def animate(self, dt):
        ANIMATION_SPEED = 14
        self.frameIndex += ANIMATION_SPEED * dt
        

        self.getState()
        self.image = self.frames[self.to][int(self.frameIndex % len(self.frames[self.to])-1)]
        
            
        #ovdje ju samo okrene ako je lijevo, po default je desno, tako da nema potrebe vracati
        if self.facingDirection == "left":
            self.image = pygame.transform.flip(self.image, True, False)

        self.cooldown += dt * 3



    def input(self):
        keys = pygame.key.get_pressed()
        inputVector = vector()

        if keys[self.save["controls"]["Movement"]["Up"]]:
            inputVector.y -= 1

        if keys[self.save["controls"]["Movement"]["Down"]]:
            inputVector.y += 1

        if keys[self.save["controls"]["Movement"]["Left"]]:
            inputVector.x -= 1

        if keys[self.save["controls"]["Movement"]["Right"]]:
            inputVector.x += 1

        if keys[self.save["controls"]["Movement"]["Jump"]]:
            self.special = not self.special

        for key in self.save["controls"]["Movement"].values():
                if keys[key] and self.cooldown >= 1 and self.takeHit == False and self.attacking == False:
                    self.sfx["Walking2"].set_volume(0.3)
                    self.sfx["Walking2"].play()
                    self.cooldown = 0
        


        if keys[pygame.K_LSHIFT]:
            self.special2 = not self.special2

        if pygame.mouse.get_just_pressed()[0] == True and self.attacking == False and self.takeHit == False and self.stats["ATK"]["CE"] <= self.ce: 
            self.ce -= self.stats["ATK"]["CE"]
            self.attacking = True
            self.frameIndex = 0
            self.to = "Attack"

            #TODO prekopiraj ovu klasu za svakog borca i napraviti custom napade za svakog


        self.direction = inputVector.normalize() if inputVector else inputVector

        
    def move(self, dt):
        self.rect.centerx += self.direction.x * 250 * dt
        self.hitbox.centerx = self.rect.centerx
        self.checkCollision("horizontal")
        
        self.rect.centery += self.direction.y * 250 * dt
        self.hitbox.centery = self.rect.centery
        self.checkCollision("vertical")
    
    def regen(self, dt):
        self.counter += dt 
        if self.counter >= 1:
            self.ce += self.ceRegen * 5
            self.counter = 0

        self.ce = min(self.ce, self.stats["CE"]["Val"])

            
    def update(self, dt):
        self.regen(dt)
        self.input()
        if self.attacking == False:
            self.move(dt)
        self.animate(dt)


    def checkCollision(self, axis):
        for sprite in self.collisionSprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if axis == "horizontal":
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                if axis == "vertical":
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    self.rect.centery = self.hitbox.centery


class AriboLOL(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, facingDirection, collisionSprites, name, player):
        super().__init__(groups)

        self.player = player
        self.manager = GameStateManager()
        self.save = load_save()
        self.stats = self.save["gameData"]["Monsters"][name]

        self.name = name
        self.collisionSprites = collisionSprites
        self.frameIndex, self.frames = 0, frames
        self.speed = 5
        self.frames = frames
        self.to = "Move"
        self.playerDirection = vector() # this will be player cords and just need to make it move towards that
        self.facingDirection = facingDirection

        self.takeDmg = False
        self.died = False
        self.death = False

        self.frameStarted = False

        #stats
        self.level = self.stats["Level"] + self.save["gameData"]["Wawe"]
        self.hp = self.stats["HP"] * self.level * 0.5
        self.atk = self.stats["ATK"] * self.level * 0.5


        

        self.image = self.frames[self.facingDirection][self.to][0]
        self.rect = self.image.get_frect(center = pos)

        self.hitbox = self.rect.inflate(-self.rect.width/2, -220)

        self.direction = vector()
        self.attacking = False

        self.animationSpeed = 10

        self.index = 0

        #zvukovi

        self.sounds = {}
        self.importSound()

        sound = self.sounds["Spawn"]
        sound.set_volume(0.5)
        sound.play()

    def importSound(self):
        path = join("sfx", "enemies", self.name)
        for _, _, sounds in walk(path):
            for sound in sounds:
                index = sound.index(".")
                self.sounds[sound[0:index]] = pygame.mixer.Sound(join(path, sound))





    def move(self, dt):
        #self.chase(self.playerPos)
        if self.attacking == False:
            self.rect.centerx += self.direction.x * 120 * dt
            self.hitbox.centerx = self.rect.centerx
            self.checkCollision("horizontal")
            
            self.rect.centery += self.direction.y * 120 * dt
            self.hitbox.centery = self.rect.centery
            self.checkCollision("vertical")



    def checkCollision(self, axis):
        for sprite in self.collisionSprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if axis == "horizontal":
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                if axis == "vertical":
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    self.rect.centery = self.hitbox.centery



    def getState(self, dt):

        if self.death == True:
            if self.frameStarted == False:
                self.frameIndex = 0
                self.frameStarted = True
            self.to = "Death"
            if int(self.frameIndex % len(self.frames[self.facingDirection][self.to])) == len(self.frames[self.facingDirection][self.to])-1:
                self.died = True
                self.frameStarted = False
        else:

        #make the default to be Move since the enemies are always moving
            if self.attacking == False and self.takeDmg == False:
                self.to = "Move"
                """
                #ovo je zvuk njihovog hodanja, radi sve super, samo mi je malo naprono za slusati i ne dodaje bas igrici
                self.index += dt * 5
                if self.index >= 1:
                    self.index = 0
                    sfx = self.sounds["Move"]
                    sfx.set_volume(0.1)
                    sfx.play()
                """
                if self.direction.x != 0:
                    if self.direction.x < 0:
                        self.facingDirection = "Left"
                    else:
                        self.facingDirection = "Right"

            if self.takeDmg == True:
                self.attacking = False
                self.to = "TakeHit"
                #ovo je cisto da prikaze fino cijelu animaciju, ima malo problema
                #bez ovog ovisno kad udari
                if self.frameStarted == False:
                    self.frameIndex = 0
                    self.frameStarted = True
                    self.animationSpeed = 7

                self.rect.centerx += -self.direction.x * 2
                self.checkCollision("horizontal")
                self.rect.centery += -self.direction.y * 2
                self.checkCollision("vertical")
                
                if int(self.frameIndex % len(self.frames[self.facingDirection][self.to])) == len(self.frames[self.facingDirection][self.to])-1:
                    self.takeDmg = False
                    if self.hp <= 0:
                        self.death = True
                    self.frameStarted = False
                    self.animationSpeed = 10
        


            if self.attacking == True and self.takeDmg == False:
                self.to = "Attack"

                if self.frameStarted == False:
                    self.frameIndex = 0
                    self.frameStarted = True
                
                if int(self.frameIndex % len(self.frames[self.facingDirection][self.to])) == len(self.frames[self.facingDirection][self.to])-2:
                    attack = []
                    for key in self.sounds.keys():
                        if "Attack" in key:
                            attack.append(self.sounds[key])

                    sfx = choice(attack)
                    sfx.play()

                if int(self.frameIndex % len(self.frames[self.facingDirection][self.to])) == len(self.frames[self.facingDirection][self.to])-1:
                    self.attacking = False
                    self.frameStarted = False
                    if self.attackRect.collidepoint(self.player.hitbox.center):
                        if self.player.takeHit != True and self.player.attacking != True:
                            self.player.takeHit = True
                            self.player.frameIndex = 0
                            self.player.attackedDir = self.direction

                        
        return f"{self.facingDirection}"

    def animate(self, dt):
        self.frameIndex += self.animationSpeed * dt

        self.getState(dt)
        self.image = self.frames[self.facingDirection][self.to][int(self.frameIndex % len(self.frames[self.facingDirection][self.to])-1)]
        

    def chase(self, playerPos):
        self.playerPos = playerPos
        x = (playerPos[0] - self.rect.centerx)/(abs(playerPos[0] - self.rect.centerx)+1)
        y = (playerPos[1] - self.rect.centery)/(abs(playerPos[1] - self.rect.centery)+1)
        self.playerDirection = vector(x, y)
        self.direction = self.playerDirection
        self.checkAttack()

    def checkAttack(self):
        x = abs(self.playerPos[0] - self.rect.centerx)
        y = abs(self.playerPos[1] - self.rect.centery)

        if abs(x) <= 30 and abs(y) <= 30 :
            self.attacking = True
            self.attackRect = self.rect.inflate(-100, -150)


    
    def update(self, dt):
        if self.attacking == False and self.death == False and self.died == False:
            self.move(dt)
        self.animate(dt)