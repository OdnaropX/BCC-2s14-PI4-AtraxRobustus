from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import numpy as np
import math
from random import Random
import util
import collections

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
	def find_avaliable_space(self, scene, size_x, size_y, first_only = False, use_first = False):
		x = scene.shape[0]
		y = scene.shape[1]
			
		find = False
		locations = []
		#Check the available locations to insert the rectangular. 
		#For this use the summed table area. Areas already filled will not result in 0. Dont need to check last size_x and last size_y.
		for i in xrange(x - size_x):
			for j in xrange(y - size_y):
				#print i, j
				#Used not because scene can be 0.0 instead of 0. Not really sure if == x (x = 0) will have the same result when x = 0.0
				#Image (0,0) start on left top. 
			
				if use_first:
					area = scene[i, j][0] + scene[i + size_x, j + size_y][0] - (scene[i + size_x, j][0] + scene[i, j + size_y][0])
				else:
					area = scene[i, j] + scene[i + size_x, j + size_y] - (scene[i + size_x, j] + scene[i, j + size_y])
					
				if not area:
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
			new_size = (4 * count / np.log(count + 10)) / 10
		else:
			new_size = 1
			
		if new_size < min_size:
			return min_size
		else:
			return int(new_size)
		
	def get_font_size_on_circle(self, character_length, diameter):
		diameter = diameter * 1.5
		return int(diameter/character_length)


		
	"""
		Method used to get the diameter from the bubble.
	"""
	def get_bubble_size(self, word, count, min_size):

		if count:
			if count > 2000:
				#new_size = (5 * count / np.log(count + 100)) / 10
				new_size = (12 * count / np.log(count + 10)) / 10
			else:
				new_size = (13 * count / np.log(count + 10)) / 10
				
			#new_size = 50 * np.log(count + 100) / 10
		else:
			new_size = 1
			
			
		if new_size < min_size:
			return min_size
		else:
			return min(700, int(new_size))
	
	
	def get_font_used(self, location = None):
		if not location:
			return self.fonts[0]
			
		font_amount = len(self.fonts)
		
		return self.fonts[location % font_amount]
		
	def format_bubbles(self, scene, canvas_width, canvas_height, words, use_all_words = True, random = None, use_first = True, mask_array = None):
		if words:
			if not mask_array == None:
				black_array = mask_array
				scene = Image.fromarray(black_array)
				scene.convert('L')
			else:
				if scene == None:
					#Create new black scene
					scene = Image.new("L", (canvas_width, canvas_height))
					use_first = False

				black_array = np.array(scene)
			draw = ImageDraw.Draw(scene)

			
			if random:
				first_only = False
			else:
				first_only = True
				
			bubbles = []
			for word in words:
				print "Formatting: ", word 
				font = ImageFont.truetype('verdana.ttf', 37)
				draw.setfont(font)
				#Get size of resulting text
				box_size = draw.textsize(word[1])
				print box_size
				
				position = None
				diameter = self.get_bubble_size(word[1], word[0], 60)
				print diameter
				
				#Loop while not find position. Get a small size if 
				while diameter > 1 and not position:
					#Find available position					
					position = self.find_avaliable_space(black_array, diameter, diameter, first_only, use_first)
					if use_all_words:
						diameter -= 1
					else:
						break
				
				if position:
					new_circle = {}
					new_circle['diameter'] = diameter
					if random:
						#random position
						new_circle['x'], new_circle['y'] = position[random.randint(0, len(position) - 1)]
					else:
						#first position
						new_circle['x'], new_circle['y'] = position[0]
					
					new_circle['fill'] = "white"
					new_circle['outline'] = self.get_color(True)
					new_circle['char_length'] = word[2]
					new_circle['text'] = word[1]
					new_circle['items'] = util.convert_to_number(word[0])
					
					#Draw circle.
					draw.ellipse((new_circle['x'], new_circle['y'], new_circle['x'] + diameter, new_circle['y'] + diameter), fill="white", outline="white")
					#Get new array from scene
					black_array = np.array(scene)
					
					#Save test to know if it is really saving the item on array. Cannot print the array, is too length.
					#new = Image.fromarray(scene)
					scene.save('teste-bubble.png')
					
					#This is the good part, the cumsum will generate the new integral image. Will sum on axis y and x.  
					black_array = np.cumsum(np.cumsum(black_array, axis=1),axis=0)
					bubbles.append(new_circle)
					
			return bubbles
		else:
			return []
		
	def get_color(self, random = False):
		if not random:
			return (0,0,0)
		random = Random()
		colors = []
		colors.append((59,22,216))#Blue
		colors.append((186,196,72))#Yellow
		colors.append((0,0,0))#Black
		colors.append((133,96,168))#Purple
		colors.append((236,147,41))#Oranje
		
		return colors[random.randint(0, len(colors) - 1)]
		
		
		
	"""
		Format words.
		random must be a instance of Random()
	
	"""
	def format_words(self, scene, canvas_width, canvas_height, words, use_all_words = True, random_font = False, random = None, use_first = True, mask_array = None):
		if words:
			if not mask_array == None:
				black_array = mask_array
				scene = Image.fromarray(black_array)
				scene.convert('L')
			else:
				if scene == None:
					#Create new black scene
					scene = Image.new("L", (canvas_width, canvas_height))
					use_first = False

				black_array = np.array(scene)
			draw = ImageDraw.Draw(scene)
			
			if random:
				first_only = False
			else:
				first_only = True
				
			formatted_words = []
			i = 0
			for word in words:
				print "Formatting: ", word 
				if random_font: 
					i += 1
				
				new_word = {}
				new_word['font_used'] = self.get_font_used(i)
				
				position = None
				font_size = self.get_font_size(word[1], word[0], 10) + 1
				print font_size
				#Loop while not find position. Get a small size if 
				while font_size > 1 and not position:
					font_size -= 2
					#Find available position
					font = ImageFont.truetype(new_word['font_used'], font_size)
					draw.setfont(font)
					#Get size of resulting text
					box_size = draw.textsize(word[1])
					position = self.find_avaliable_space(black_array, box_size[1], box_size[0], first_only, use_first)
					
					if not use_all_words:
						break
						
				if position:
					new_word['text'] = word[1]
					if random:
						#random position
						new_word['x'], new_word['y'] = position[random.randint(0, len(position) - 1)]
					else:
						#first position
						new_word['x'], new_word['y'] = position[0]
						
					new_word['color'] = self.get_color(True)
					new_word['font_size'] = font_size
					#Draw word in temporary location
					draw.text((new_word['x'], new_word['y']), word[1], fill="white")
					#Get new array from scene
					black_array = np.array(scene)
					
					#Save test to know if it is really saving the item on array. Cannot print the array, is too length.
					#new = Image.fromarray(scene)
					scene.save('teste--{0}.png'.format(i))
					
					#This is the good part, the cumsum will generate the new integral image. Will sum on axis y and x.  
					black_array = np.cumsum(np.cumsum(black_array, axis=1),axis=0)
					formatted_words.append(new_word)
			return formatted_words
		else:
			return []
	
	"""
		Method used to draw a word cloud.
		Initial idea was create a bubble cloud, after know about integral image think of using on word cloud. 
	"""
	def cloud_words(self, filename, words = [], canvas_width = 1920, canvas_height = 1080, background_color = (255, 255, 255), mask = None, mask_array = None, use_first = True):
		#new_scene = np.zeros((canvas_height, canvas_width), dtype=np.uint32)#need to be integer.
		
		#each words must be a tuple with the text and count.
		formatted_words = self.format_words(mask, canvas_width, canvas_height, words, True, False, Random(), use_first, mask_array)
		if formatted_words:
			image = Image.new("RGB", (canvas_width, canvas_height), background_color)
			canvas  = ImageDraw.Draw(image)
			
			for word in formatted_words:
				font = ImageFont.truetype(word['font_used'], word['font_size'])
				canvas.setfont(font)
				canvas.text((word['x'],word['y']), word['text'], fill = word['color'])
			
			image.save(filename)
		else:
			print "No words to print"
	
	"""
		Method used to draw bubbles cloud.
	"""
	def bubbles(self, filename, collections = [], canvas_width = 1920, canvas_height = 1080, background_color = (255, 255, 255), mask = None, mask_array = None, use_first = True):
		#new_scene = np.zeros((canvas_height, canvas_width), dtype=np.uint32)#need to be integer.
		
		formatted_bubbles = self.format_bubbles(mask, canvas_width, canvas_height, collections, False, Random(), use_first, mask_array)
		
		if formatted_bubbles:
			image = Image.new("RGB", (canvas_width, canvas_height), background_color)
			canvas  = ImageDraw.Draw(image)
			
			for word in formatted_bubbles:
				canvas.ellipse((word['x'], word['y'], word['x'] + word['diameter'], word['y'] + word['diameter']), word['fill'], word['outline'])
				#Draw text inside ellipse.
				font_used = self.get_font_used()
				font_size = self.get_font_size_on_circle(word['char_length'], word['diameter'])
				font = ImageFont.truetype(font_used, font_size)
				canvas.setfont(font)
				box_size = canvas.textsize(word['text'])
				
				while box_size[0] >= word['diameter'] - 10:
					font_size -= 1
					font = ImageFont.truetype(font_used, font_size)
					canvas.setfont(font)
					box_size = canvas.textsize(word['text'])
				
				
				#canvas.text((word['x'] + (word['diameter'] / 2) - (box_size[0] / 2), word['y'] + (word['diameter'] / 2) - (box_size[1] / 2)), word['text'], fill=word['outline'])
				if word['items'] > 1:
					item = '{0} itens'.format(word['items'])
				else:
					item = '{0} item'.format(word['items'])
					
				x = word['x'] + (word['diameter'] / 2)
				y = word['y'] + (word['diameter'] / 2) - (box_size[1] / 2) - (word['diameter']  * 0.1)
				canvas.text((x - (box_size[0] / 2), y), word['text'], fill=word['outline'])
					
				font_size = self.get_font_size_on_circle(len(item), word['diameter'])
				font = ImageFont.truetype(font_used, font_size)
				canvas.setfont(font)
				text_size = canvas.textsize(item)
				
				while text_size[0] >= word['diameter'] - 10:
					font_size -= 1
					font = ImageFont.truetype(font_used, font_size)
					canvas.setfont(font)
					text_size = canvas.textsize(item)
					
				print text_size
				canvas.text((x - (text_size[0] / 2), y + box_size[1] + 5), item, fill=word['outline'])

			image.save(filename)
		else:
			print "No words to print"
		
	def spiral(self, collections = []):
		pass
	