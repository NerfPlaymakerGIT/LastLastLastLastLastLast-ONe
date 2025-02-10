from settings import *
from save import *
from timer import Timer

ShopkeeperData = {
    "Initial" : "Hello, what would you like to purchase?",
}

class DialogueTree:
    def __init__(self, character, player, allSprites, fonts, endDialog):
        self.save = load_save()
        self.data = ShopkeeperData
        self.player = player
        self.chararcter = character
        self.sprites = allSprites
        self.font = fonts
        self.choice = "Initial"
        self.endDialog = endDialog

        self.dialog = character.getDialogue()
        self.dialogLen = len(self.dialog)
        self.dialogIndex = 0

        self.currDialog = DialogSprite(self.dialog, self.chararcter, self.sprites, self.font)

        self.arr = [key for key in self.dialog.keys()]

    def input(self):
        keys = pygame.key.get_just_pressed()
        if keys[self.save["controls"]["Movement"]["Interact"]]:
            self.currDialog.kill()
            self.dialogIndex += 1
            if self.dialogIndex < self.dialogLen-1:
                self.currDialog = DialogSprite(self.dialog[self.arr[self.dialogIndex]], self.chararcter, self.sprites, self.font)
            else:
                self.dialogIndex = -1
                self.endDialog(self.chararcter)


    def update(self):
        self.input()

        
        

class DialogSprite(pygame.sprite.Sprite):
    def __init__(self, message, person, groups, fonts):
        super().__init__(groups)

        #text
        message = str(message)
        textSurf = fonts.render(message, False, (255, 255, 255))
        padding = 5
        width = max(textSurf.get_width() + padding * 2, 30)
        height = textSurf.get_height() + padding * 2

        #background
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 0))
        pygame.draw.rect(surf, (0, 0, 0), surf.get_frect(topleft = (0, 0)), 0, 4)
        surf.blit(textSurf, textSurf.get_frect(center = (width/2, height/2)))

        self.image = surf
        self.rect = self.image.get_frect(midbottom = person.rect.midtop + vector(0, -10))