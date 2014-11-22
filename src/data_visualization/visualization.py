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
	
	"""
		Format words.
		random must be a instance of Random()
	
	"""
	def format_words(self, words, random = None):
		if words:
			black_scene = Image.new("L", (canvas_width, canvas_height))
			draw = ImageDraw.Draw(grey_scale)
			
			formatted_words = []
			for word in self.words:
				new_word = {}
				i += 1
				#Find avaliable position
				new_word['font_size'] = self.get_font_size(word[1], word[0])
				font = ImageFont.truetype(self.font_used, new_word['font_size'])
				draw.setfont(font)
				# get size of resulting text
				box_size = draw.textsize(word[1])
				position = self.find_avaliable_space(box_size[1], box_size[0])
			
				if position:
					new_word['text'] = word[1]
					if random:
						new_word['x'], new_word['y'] = position[random.randint(0, len(position) - 1)]
					else:
						new_word['x'], new_word['y'] = position[0]
						
					new_word['color'] = 'black'
					
					#Draw word in temporary location
					draw.text((new_word['x'], new_word['y']), word[1], fill="white")

					black_array = np.array(black_scene)
					#Save test to know if it is really saving the item on array. Cannot print the array, is too length.
					#new = Image.fromarray(black_scene)
					#new.save('teste{0}.png'.format(i))
					
					#This is the good part, the cumsum will generate the new integral image. Will sum on axis y and x.  
					self.integral_image = np.cumsum(np.cumsum(black_array, axis=1),axis=0)
					formatted_words.append(new_word)
			return formatted_words
		else:
			return []
	
	def cloud_words(self, words = [], canvas_width = 1920, canvas_height = 1080):
		new_scene = np.zeros((canvas_height, canvas_width), dtype=np.uint32)#need to be integer.
		
		
		
		
		pass
	
	def spiral(self, collections = []):
		pass
	