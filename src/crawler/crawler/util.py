import sys
import linecache
import re
import collections
import types
from scrapy import log

pattern_last_newline = re.compile(ur'\n$')
pattern_last_bracket = re.compile(ur'\[$')
pattern_number_range = re.compile(ur'^[^a-zA-Z .][0-9-]{1,}$')
		
"""
	Class for connection and manipulation of database.
	Have methods for delete, update and insert on any table. 
	Have also methods for insert on specified table following it own logic.
"""

"""
	Method used to format the name.
"""
def get_formatted_name(name, name_first = False):
	name = sanitize_title(name)
	
	if(not name):
		return None
		
	names = name.split(" ")
	
	name = {}
	name['name'] = ""
	name['lastname'] = ""
			
	length_names = len(names)
	if(length_names > 1):
		if(name_first):
			name['name'] = names[0] 
			names.remove[0]
			name['lastname'] = " ".join(names) 
		else:
			name['name'] = names.pop()
			name['lastname'] = " ".join(names)
	elif(length_names == 1):
		name['name'] = names[0]
		name['lastname'] = "NO LAST NAME"
		
	name['name'] = name['name'].strip()
	name['lastname'] = name['lastname'].strip()
	return name;
	
def get_line_exception():
	exc_type, exc_obj, tb = sys.exc_info()
	f = tb.tb_frame
	lineno = tb.tb_lineno
	filename = f.f_code.co_filename
	linecache.checkcache(filename)
	line = linecache.getline(filename, lineno, f.f_globals)
	return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
	
def PrintException():
	print get_line_exception()
	
def Log(url, message):
	#Save Log
	message = "Error on " + url + ": " +  str(message) + " " + get_line_exception()
	log.msg(message, level=log.INFO)
	
def concatene_content(title, join_string = ' '):
	if not title:
		return None
		
	if(isinstance(title, collections.Iterable) and not isinstance(title, types.StringTypes)):
		title = join_string.join(title)
		
	return title
	
def sanitize_title(title):
	#remove type from title.
	
	title = concatene_content(title)
	if not title:
		return None
		
	#remove last newline with sub
	title = re.sub(pattern_last_newline, '', title)
	title = title.strip()
	if 'N/A' in title:
		return None
	if '\r\n' == title:
		return None
	return title
			
def sanitize_content(description):
	description = concatene_content(description, "\n")	

	if not description:
		return None
		
	#remove extra space. 
	description = description.strip()
	#remove last \n with sub.
	description = re.sub(pattern_last_newline, '', description)
	description = re.sub(pattern_last_bracket, '', description)
			
	if(description == 'N/A'):
		return None
	return description
	
def get_formatted_number(number):
	numbers = []
	#if is number or number range:
	if(re.search(pattern_number_range, number) != None):
		range = number.split("-", 1)
		if not isinstance(range, types.StringTypes) and len(range) > 1:
			try:
				for n in range(convert_to_number(range[0]), convert_to_number(range[1])):
					numbers.append(n)
			except:
				numbers.append(number)
		else:
			numbers.append(range[0])
	else:#if is text return text
		numbers.append(number)
	return numbers

def convert_to_number(string):
	try:
		new_number = int(string)
		return new_number
	except ValueError as e:
		new_number = float(string)
		return new_number
		
		