from settings import *

class Button:
    def __init__(self, width, height, font):
        self.font = font
        self.size = (width, height)

        
    def CreateButton(self, text, pos, color):
        self.words = text
        self.pos = pos
        self.color = color
        
        #sam sadrzaj
        self.text = self.font.render(self.words, False, self.color)
        self.textRect = self.text.get_rect(center = pos)
        
        return self.text, self.textRect
    
