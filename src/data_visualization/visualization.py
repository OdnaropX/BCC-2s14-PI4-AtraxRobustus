from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import numpy as np
import math
from random import Random

class Visualization:

	"""
		Method used to find all or first avaliable space in a scene. 
		The scene must be a numpy array with zeros. Location already occupied will not be equal to zero.
		This method use integral image to find a avaliable space.
		TODO: Find a avaliable space using polygon and not rectangular items. 
	"""
	def find_avaliable_space(self, scene, size_x, size_y, first_only = False):
		if scene:
			x = scene.shape[0]
			y = scene.shape[1]
			
			find = False
			locations = []
			#Check the available locations to insert the rectangular. 
			#For this use the summed table area. Areas already filled will not result in 0.
			for i in xrange(x - size_x):
				for j in xrange(y - size_y):
					#print i, j
					#Used not because scene can be 0.0 instead of 0. Not really sure if == x (x = 0) will have the same result when x = 0.0
					if not scene[i, j] + scene[i + size_x, j + size_y] - (scene[i + size_x, j] + scene[i, j + size_y]):
						locations.append((j, i))
						if first_only:
							find = True
							break
				if find and first_only:
					break
					
			return locations
	
	def cloud_words(self, words = [], canvas_width = 1920, canvas_height = 1080):
		new_scene = np.zeros((canvas_height, canvas_width), dtype=np.uint32)
		
		if words:
			black_scene = grey_scale = Image.new("L", (canvas_width, canvas_height))
			draw = ImageDraw.Draw(grey_scale)
		
		
		pass
	
	def spiral(self, collections = []):
		pass
	