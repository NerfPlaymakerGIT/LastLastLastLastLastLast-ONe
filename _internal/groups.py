from settings import *
from entities import *
from images import import_image

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = vector(-150, -120)

    def draw(self, playerCenter):
        self.offset.x = -(playerCenter[0] - resX / 2)
        self.offset.y = -(playerCenter[1] - resY / 2)
        
        for sprite in self:
            if isinstance(sprite, Entity) or isinstance(sprite, NPC):
                self.shadow = import_image("Images", "Characters", "MainChar", "Shadow")
                self.shadow = pygame.transform.scale2x(self.shadow)
                self.shadowRect = self.shadow.get_frect(center = sprite.rect.topleft + self.offset + (46, 65))
                screen.blit(self.shadow, self.shadowRect)

            screen.blit(sprite.image, sprite.rect.topleft + self.offset)


            
