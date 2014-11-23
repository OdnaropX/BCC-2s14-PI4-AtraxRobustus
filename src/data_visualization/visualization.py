from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import numpy as np
import math
from random import Random

class Visualization:

	def __init__(self):
		self.fonts = []
		self.fonts.append('verdana.ttf')
		self.fonts.append('arial.ttf')
	
	
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
		Get size from count. 
		Use natural log to multiply by a value not to great. Some count are greater than 3000.
	"""
	def get_font_size(self, word, count, min_size):
		if count:
			#Sum with 10 to log(1) return at least 1 and avoid 0.
			new_size = np.log(count + 10)
		else:
			new_size = 1
			
		return min_size * new_size
		
	def get_font_size_on_circle(self, circle_x, circle_y, radius):
		pass
		
	
	def get_font_used(self, location):
		if not location:
		
		font_amount = len(self.fonts)
		
		return self.fonts[location % font_amount]
		
	"""
		Format words.
		random must be a instance of Random()
	
	"""
	def format_words(self, scene, canvas_width, canvas_height, words, use_all_words = True, random_font = False, random = None):
		if words:
			if not scene:
				scene = Image.new("L", (canvas_width, canvas_height))

			draw = ImageDraw.Draw(scene)
			black_array = np.array(scene)
			
			formatted_words = []
			i = 0
			for word in self.words:
				if random_font: 
					i += 1
				
				new_word = {}
				new_word['font_used'] = self.get_font_used(i)
				
				position = None
				font_size = self.get_font_size(word[1], word[0])
				#Loop while not find position.
				while font_size > 1 and not position:
					#Find available position
					font = ImageFont.truetype(new_word['font_used'], font_size)
					draw.setfont(font)
					#Get size of resulting text
					box_size = draw.textsize(word[1])
					position = self.find_avaliable_space(black_array, box_size[1], box_size[0])
					font_size -= 1
			
				if position:
					new_word['text'] = word[1]
					if random:
						#random position
						new_word['x'], new_word['y'] = position[random.randint(0, len(position) - 1)]
					else:
						#first position
						new_word['x'], new_word['y'] = position[0]
						
					new_word['color'] = 'black'
					
					#Draw word in temporary location
					draw.text((new_word['x'], new_word['y']), word[1], fill="white")

					
					#Save test to know if it is really saving the item on array. Cannot print the array, is too length.
					#new = Image.fromarray(black_scene)
					#new.save('teste{0}.png'.format(i))
					
					#This is the good part, the cumsum will generate the new integral image. Will sum on axis y and x.  
					black_array = np.cumsum(np.cumsum(black_array, axis=1),axis=0)
					formatted_words.append(new_word)
			return formatted_words
		else:
			return []
	
	"""
		Method used to drawn a word cloud.
	"""
	def cloud_words(self, filename, words = [], canvas_width = 1920, canvas_height = 1080, background_color = (255, 255, 255)):
		new_scene = np.zeros((canvas_height, canvas_width), dtype=np.uint32)#need to be integer.
		
		#each words must be a tuple with the text and count.
		formatted_words = self.format_words(None, canvas_width, canvas_height, words)
		if formatted_words:
			image = Image.new("RGB", (self.canvas_width, self.canvas_height), background_color)
			canvas  = ImageDraw.Draw(image)
			
			for word in formatted_words:
				font = ImageFont.truetype(word['font_used'], word['font_size'])
				canvas.setfont(font)
				canvas.text((word['x'],word['y']), word['text'], fill = word['color'])
			
			image.save(filename)
		else:
			print "No words to print"
			
	def bubble(self, collections = []):
		pass
		
	def spiral(self, collections = []):
		pass
	