from settings import *
from save import *


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, facingDirection):
        super().__init__(groups)

        self.frameIndex, self.frames = 0, frames

        self.to = "idle"
        self.direction = vector()
        self.facingDirection = facingDirection
        self.blocked = False

        self.image = self.frames[self.to][self.getState()][self.frameIndex]
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_frect(center = pos)







    def getState(self):
        moving = bool(self.direction)

        #schmooooovement logic
        if moving:
            self.to = "walk"
            if self.direction.x != 0 and self.direction.y == 0:
                if self.direction.x < 0:
                    self.facingDirection = "left"
                else:
                    self.facingDirection = "right"
            if self.direction.y != 0 and self.direction.x == 0:
                if self.direction.y > 0:
                    self.facingDirection = "down"
                else:
                    self.facingDirection = "Up"
            if self.direction.y != 0 and self.direction.x != 0:
                if self.direction.y < 0:
                    if self.direction.x > 0:
                        self.facingDirection = "UpR"
                    else:
                        self.facingDirection = "UpL"
                if self.direction.y > 0:
                    if self.direction.x > 0:
                        self.facingDirection = "down"
                    else:
                        self.facingDirection = "down"
            
        else:
            self.to = "idle"

        return f"{self.facingDirection}"

    def animate(self, dt):
        ANIMATION_SPEED = 11
        self.frameIndex += ANIMATION_SPEED * dt
        self.image = self.frames[self.to][self.getState()][int(self.frameIndex % len(self.frames[self.to][self.getState()]))]
        self.image = pygame.transform.scale2x(self.image)

    def block(self):
        self.blocked = True
        self.direction = vector(0, 0)
    
    def unblock(self):
        self.blocked = False



class Player(Entity):
    def __init__(self, pos, frames,groups, facingDirection, collisionSprites, sfx):
        super().__init__(pos, frames, groups, facingDirection)
        self.sfx = sfx
        self.collisionSprites = collisionSprites
        self.facingDirection = facingDirection

        self.save = load_save()
        self.direction = vector()

        self.hitbox = self.rect.inflate(-self.rect.width/2, -120)

        self.cooldown = 0

    def input(self):
        if self.blocked != True:
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

            for key in self.save["controls"]["Movement"].values():
                if keys[key] and self.cooldown >= 1:
                    self.sfx["Walking"].set_volume(0.3)
                    self.sfx["Walking"].play()
                    self.cooldown = 0

            self.direction = inputVector.normalize() if inputVector else inputVector

    def move(self, dt):
        self.rect.centerx += self.direction.x * 250 * dt
        self.hitbox.centerx = self.rect.centerx
        self.checkCollision("horizontal")
        
        self.rect.centery += self.direction.y * 250 * dt
        self.hitbox.centery = self.rect.centery
        self.checkCollision("vertical")

    def update(self, dt):
        if not self.blocked:
            self.input()
            self.move(dt)
            self.animate(dt)
        self.cooldown += dt * 3

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


class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, frames,groups, facingDirection, characterData, name, sfx):
        super().__init__(groups)

        self.name = name
        self.sfx = sfx

        self.screen = pygame.display.get_surface()
        self.frameIndex, self.frames = 0, frames
        self.direction = vector()
        self.facingDirection = facingDirection
        self.blocked = False
        #dialog
        self.data = characterData
        self.interactable = False
        self.radius = 250


        self.image = self.frames["idle"]["down"][0]
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_frect(center = pos)



    def block(self):
        self.blocked = True
        self.direction = vector(0, 0)
    
    def unblock(self):
        self.blocked = False

    def getDialogue(self):
        return self.data

    def animate(self, dt):
        ANIMATION_SPEED = 7
        self.frameIndex += ANIMATION_SPEED * dt
        self.image = self.frames["idle"][self.facingDirection][int(self.frameIndex % len(self.frames["idle"][self.facingDirection]))]
        self.image = pygame.transform.scale2x(self.image)

    def changeFacingDirection(self, target):
        relation = vector(target.rect.center) - vector(self.rect.center)
        if abs(relation.y) < 30:
            self.facingDirection = "right" if relation.x > 0 else "left"
        else:
            self.facingDirection = "down" if relation.y > 0 else "Up"

    def update(self, dt):
        self.animate(dt)





