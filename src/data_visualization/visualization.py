from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import numpy as np
import math
from random import Random
import util
import collections
import os

class Visualization:

	def __init__(self):
		self.fonts = []
		self.fonts.append('verdana.ttf')
		self.fonts.append('arial.ttf')
		self.colors = []
		self.colors.append((59,22,216))#Blue
		self.colors.append((186,196,72))#Yellow
		self.colors.append((0,0,0))#Black
		self.colors.append((133,96,168))#Purple
		self.colors.append((236,147,41))#Oranje
	
	"""
		Method used to find all or first avaliable space in a scene. 
		The scene must be a numpy array with zeros. Location already occupied will not be equal to zero.
		This method use integral image to find a avaliable space.
		TODO: Find a avaliable space using polygon and not rectangular items. 
	"""
	def find_avaliable_space(self, integral_image, size, first_only = False, xy_initial = (None, None), xy_final = (None, None)):
		size_x, size_y = size
		y_initial, x_initial = xy_initial
		y_final, x_final = xy_final
		
		if not x_final:
			x_final = integral_image.shape[0] 
		if not y_final:
			y_final = integral_image.shape[1]
			
		if not x_initial or x_initial < 0:
			x_initial = 0
		if not y_initial or y_initial < 0:
			y_initial = 0
			
		if x_final + size_x > integral_image.shape[0]:
			x_final = x_final - size_x
		if y_final + size_y > integral_image.shape[1]:
			y_final = y_final - size_y
		
		
		#Use more memory but less processor:
		if first_only:
			#Check the available locations to insert the rectangular. 
			#For this use the summed table area. Areas already filled will not result in 0. Dont need to check last size_x and last size_y.
			for i in xrange(x_initial, x_final):
				for j in xrange(y_initial, y_final):
					if not integral_image[i, j] + integral_image[i + size_x, j + size_y] - (integral_image[i + size_x, j] + integral_image[i, j + size_y]):
						return (j, i)
		else:
			locations = []
			for i in xrange(x_initial, x_final):
				for j in xrange(y_initial, y_final):
					if not integral_image[i, j] + integral_image[i + size_x, j + size_y] - (integral_image[i + size_x, j] + integral_image[i, j + size_y]):
						locations.append((j, i))
			return locations
	
	"""
		Get size from count.
		Use natural log to multiply by a value not to great. Some count are greater than 3000.
	"""
	def get_font_size(self, word, count, min_size, divisor = 10):
		if not divisor:
			divisor = 10
			
		if count:
			count = int(count)
			#Sum with 10 to log(1) return at least 1 and avoid 0.
			new_size = (4 * count / np.log(count + 10)) / divisor
		else:
			new_size = 1
			
		if new_size < min_size:
			return min_size
		else:
			return int(new_size)
		
	"""
		Get font size using diameter.
	"""
	def get_font_size_on_circle(self, character_length, diameter):
		#Fix character equals 1
		if character_length == 1:
			return diameter / 2
			
		diameter = diameter * 1.5
		return int(diameter/character_length)

	"""
		Method used to get the diameter from the bubble.
	"""
	def get_bubble_size(self, word, count, min_size, divisor = 10):
		if not divisor:
			divisor = 10
		if count:
			count = int(count)
			if count > 2000:
				#c = 12
				c = 50
				#new_size = (5 * count / np.log(count + 100)) / 10
				new_size = (c * count / np.log(count + 10)) / divisor
			else:
				new_size = (13 * count / np.log(count + 10)) / divisor
				
			#new_size = 50 * np.log(count + 100) / 10
		else:
			new_size = 1
			
		print new_size
		if new_size < min_size:
			return min_size
		else:
			return min(700, int(new_size))
	
	"""
		Method used to get at least on font from avaliable fonts.
	"""
	def get_font_used(self, location = None):
		if not location:
			return self.fonts[0]
			
		font_amount = len(self.fonts)
		
		return self.fonts[location % font_amount]
	
	"""
		Method used to get a avaliable color.
	"""
	def get_color(self, random = False):
		lenght = len(self.colors)
		if not random or not lenght:
			return (0,0,0)
			
		random = Random()
		
		return self.colors[random.randint(0, lenght - 1)]
		
	"""
		Convert a pixel position give a angle to other.
	"""
	def translate_pixel(self, pixels, angle):
		x, y = pixels
		#convert to radian
		angle = (math.pi * angle) / 180
		
		new_x = x * math.cos(angle) - y * math.sin(angle)
		new_y = y * math.sin(angle) + y * math.cos(angle)
		
		return (new_x, new_y)
		
		
	############################# Begin of specified methods for data visualization ##############################
	##############################################################################################################

	"""
	canvas_size must be equals to (canvas_width, canvas_height)
	"""
	def find_bubble_position(self, mask_array, canvas_size,	items, random = False, xy_initial = (None, None), xy_final = (None, None), use_all_words = True):
		if items:
			canvas_width, canvas_height = canvas_size
			
			if not mask_array:
				#Create new black scene
				scene = Image.new("L", (canvas_width, canvas_height))
				mask_array = np.array(scene)
				#mask_array = np.zeros((canvas_height, canvas_width), dtype=np.uint32)#need to be integer.
			else:
				scene = Image.fromarray(mask_array)
				scene.convert('L')
			
			draw = ImageDraw.Draw(scene)

			if random:
				first_only = False
				random = Random()
			else:
				first_only = True
				
			bubbles = []
				
			print len(mask_array)
			for item in items:
				#print "Formatting: ", item 
				
				position = None
				diameter = self.get_bubble_size(item[0], item[1], 60)
				#print diameter
				
				#Loop while not find position. Get a small size if 
				while diameter > 1 and not position:
					#Find available position					
					position = self.find_avaliable_space(mask_array, (diameter, diameter), first_only, xy_initial, xy_final)
					if use_all_words:
						#reduce size on pixels.
						diameter -= 10
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
					new_circle['char_length'] = item[2]
					new_circle['text'] = item[0]
					new_circle['items'] = util.convert_to_number(item[1])
					
					#Draw circle.
					draw.ellipse((new_circle['x'], new_circle['y'], new_circle['x'] + diameter, new_circle['y'] + diameter), fill="white", outline="white")
					#Get new array from scene
					mask_array = np.array(scene)
					
					#Save test to know if it is really saving the item on array. Cannot print the array, is too length.
					#new = Image.fromarray(scene)
					scene.save('teste-bubble.png')
					
					#This is the good part, the cumsum will generate the new integral image. Will sum on axis y and x.  
					mask_array = np.cumsum(np.cumsum(mask_array, axis=1),axis=0)
					bubbles.append(new_circle)
					
			return bubbles
		else:
			return []

	def find_word_position(self, mask_array, canvas_size, items, random = False, xy_initial = (None, None), xy_final = (None, None), use_all_words = True):
		if items:
			canvas_width, canvas_height = canvas_size
			
			if not mask_array:
				#Create new black scene
				scene = Image.new("L", (canvas_width, canvas_height))
				mask_array = np.array(scene)
				#mask_array = np.zeros((canvas_height, canvas_width), dtype=np.uint32)#need to be integer.
			else:
				scene = Image.fromarray(mask_array)
				scene.convert('L')
			
			draw = ImageDraw.Draw(scene)

			if random:
				first_only = False
				random = Random()
			else:
				first_only = True
				
			formatted_words = []
			for item in items:
				print "Formatting: ", item 
				
				new_word = {}
				new_word['font_used'] = self.get_font_used()
				
				position = None
				font_size = self.get_font_size(item[0], item[1], 10) + 1
				print font_size
				#Loop while not find position. Get a small size if 
				while font_size > 1 and not position:
					font_size -= 1
					#Find available position
					font = ImageFont.truetype(new_word['font_used'], font_size)
					draw.setfont(font)
					#Get size of resulting text
					box_size = draw.textsize(item[0])
					position = self.find_avaliable_space(mask_array, (box_size[1], box_size[0]), first_only, xy_initial, xy_final)
					
					if not use_all_words:
						break
						
				if position:
					new_word['text'] = item[0]
					if random:
						#random position
						new_word['x'], new_word['y'] = position[random.randint(0, len(position) - 1)]
					else:
						#first position
						new_word['x'], new_word['y'] = position[0]
						
					new_word['color'] = self.get_color(True)
					new_word['font_size'] = font_size
					#Draw word in temporary location
					draw.text((new_word['x'], new_word['y']), item[0], fill="white")
					#Get new array from scene
					mask_array = np.array(scene)
					
					#Save test to know if it is really saving the item on array. Cannot print the array, is too length.
					#new = Image.fromarray(scene)
					#scene.save('teste.png')
					
					#This is the good part, the cumsum will generate the new integral image. Will sum on axis y and x.  
					mask_array = np.cumsum(np.cumsum(mask_array, axis=1),axis=0)
					formatted_words.append(new_word)
			return formatted_words
		else:
			return []

	"""
		Method used to draw a word cloud.
		Initial idea was create a bubble cloud, after know about integral image think of using on word cloud. 
	"""
	def cloud_words(self, filename, words = [], canvas_size = (1920, 1080), background_color = (255, 255, 255), xy_initial = (None, None), xy_final = (None, None), use_first = True, random = True, mask_array = None):
		
		#each words must be a tuple with the text and count.
		formatted_words = self.find_word_position(mask_array, canvas_size, words, random, xy_initial, xy_final)
		
		if formatted_words:
			image = Image.new("RGB", canvas_size, background_color)
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
	def cloud_bubbles(self, filename, collections = [], canvas_size = (1920, 1080), background_color = (255, 255, 255), text = ('{0} items', '{0} item') xy_initial = (None, None), xy_final = (None, None), use_first = False, random = True, mask_array = None):
		#new_scene = np.zeros((canvas_height, canvas_width), dtype=np.uint32)#need to be integer.
		
		formatted_bubbles = self.find_bubble_position(mask_array, canvas_size, collections, random, xy_initial, xy_final)
		
		if formatted_bubbles:
			if os.path.isfile(filename):
				image = Image.open(filename)
				print "Exist"
			else:
				image = Image.new("RGB", canvas_size, background_color)
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
				
				plural, singular = text
				#canvas.text((word['x'] + (word['diameter'] / 2) - (box_size[0] / 2), word['y'] + (word['diameter'] / 2) - (box_size[1] / 2)), word['text'], fill=word['outline'])
				if word['items'] > 1:
					item = plural.format(word['items'])
				else:
					item = singular.format(word['items'])
					
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
					
				canvas.text((x - (text_size[0] / 2), y + box_size[1] + 5), item, fill=word['outline'])

			image.save(filename)
		else:
			print "No words to print"
		
	def cloud_per_year(self, filename, collections = [], size_per_year = 200, amount_years = 35):
		canvas_size = (amount_years*size_per_year+60, 1080)

		for index, collection in enumerate(collections):
			len(collection)
			#print collection
			initial = index * size_per_year
			initial += 20
			final = size_per_year * (index + 1)
			final += 20
			self.cloud_bubbles(filename + ".png", collection, canvas_size, (255, 255, 255), text, (initial, 150), (final, 980))
	
	def spiral(self, collections = []):
		pass
	