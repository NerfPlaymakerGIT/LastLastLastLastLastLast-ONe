from settings import *
from os import walk
from os.path import join
from PIL import Image


#This obviously wont work since im trying to sort letters by number and letters dont have number you dum dum
#Need to get every image in a folder, import it, and (if they are a spritesheet and that can be a different func) split it into every frame with TILE SIZE in settings

def import_image(*path, alpha = True, format = 'png'):
	full_path = join(*path) + f'.{format}'
	surf = pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()
	return surf

def importFolder(*path):
	frames = []
	for folder_path, sub_folders, image_names in walk(join(*path)):
		for image_name in image_names:
			full_path = join(folder_path, image_name)
			surf = pygame.image.load(full_path).convert_alpha()
			frames.append(surf)

	return frames

def import_tilemap(cols, rows, *path):
	frames = {}
	surf = import_image(*path)
	cell_width, cell_height = surf.get_width() / cols, surf.get_height() / rows
	for col in range(cols):
		for row in range(rows):
			cutout_rect = pygame.Rect(col * cell_width, row * cell_height,cell_width,cell_height)
			cutout_surf = pygame.Surface((cell_width, cell_height))
			cutout_surf.fill('green')
			cutout_surf.set_colorkey('green')
			cutout_surf.blit(surf, (0,0), cutout_rect)
			frames[(col, row)] = cutout_surf
	return frames

def frameImporter(col, row, *path):
	frameDict = import_tilemap(col, row, *path)
	newDict = {}
	for row, direction in enumerate(("down", "left", "UpL", "Up", "UpR", "right")):
		newDict[direction] = [frameDict[(column, row)] for column in range(col)]

	return newDict
	
def characterImport(*path):

	d = {}

	for _, _, image_names in walk(join(*path)):
		for image in image_names:
			imageName = image.split(".")[0]
			d[imageName] = frameImporter(8, 6, *path, imageName)
	return d

#funckije za igru

def checkConnections(radius, entity, target, tolerance = 30):
	relation = vector(target.rect.center) - vector(entity.rect.center)
	if relation.length() < radius:
		#horizontal
		if entity.facingDirection == "left" and relation.x < 0 and abs(relation.y) < tolerance:
			return True
		
		if entity.facingDirection == "right" and relation.x > 0 and abs(relation.y) < tolerance:
			return True
		#vertical
		if (entity.facingDirection == "Up" or entity.facingDirection == "UpR" or entity.facingDirection == "UpL") and relation.y < 0 and abs(relation.x) < tolerance:
			return True
		if entity.facingDirection == "down" and relation.y > 0 and abs(relation.x) < tolerance:
			return True
		
	


#this class is how im gonna import 
class SpriteSheet():
	def __init__(self):
		self.sheet = None

	def get_image(self, frame, width, height, scale, colour):
		image = pygame.Surface((width, height)).convert_alpha()
		image.set_colorkey(colour)
		image.blit(self.sheet, (0, 0), (frame*width, 0, width, height))
		image = pygame.transform.scale(image, (width * scale, height * scale))

		return image
	
	#the getImage func will get me the actual frame and I will give amount of columns as well as image dimension(so each frame will basicaly be at imageWidth / col)
	
	def imageImport(self, cols, width, height, scale, *path):
		frames = []
		self.sheet = pygame.image.load(join(*path)).convert_alpha()
		for col in range(1, cols+1):
			image = self.get_image(col, height, height, scale, (0, 0, 0))
			frames.append(image)

		return frames
	
	def frameImport(self, name, *path):
		self.frames = {}
		for folder, subFolder, image in walk(join(*path, name)):
			for im in image:
				for i in range(len(str(im))):
					if im[i] == ",":
						directory = join(*path, name, im)
						sheet = Image.open(directory)
						cols = int(im[i+1])
						if int(im[i+1]) == 1:
							cols = int(im[i+1])*10 + int(im[i+2])	
						self.frames[im[0:i]] = self.imageImport(cols, sheet.width, sheet.height, 2, directory)

		return self.frames