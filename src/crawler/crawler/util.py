import sys
import linecache
import re
import collections
import types
from scrapy import log
from itertools import groupby

pattern_last_newline = re.compile(ur'\n$')
pattern_last_bracket = re.compile(ur'\[$')
pattern_first_newline = re.compile(ur'^\n')
pattern_number_range = re.compile(ur'^[^a-zA-Z .][0-9-]{1,}$')
pattern_replace_name = re.compile(ur'(:.*|\bdj\b.*|\(.*\)|\[.*\]|- .*)')

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
	
	new_name = {}
	
	if not isinstance(names, types.StringTypes):
		if name_first:
			new_name['name'] = names.pop(0)
		else:
			new_name['name'] = names.pop()
		
		if names:
			new_name['lastname'] = " ".join(names)
		else:
			new_name['lastname'] = "NO LAST NAME"
	else:
		new_name['name'] = names
		new_name['lastname'] = "NO LAST NAME"
	
	return new_name;
	
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
	
def Log(url, message, print_exception = True):
	#Save Log
	message = url + ": " +  str(message)
	if print_exception:
		message = "Error on " + message
	
	if print_exception:
		message += " " + get_line_exception()
		
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
	#remove first newline with sub
	title = re.sub(pattern_first_newline, '', title)
	
	title = title.strip()
	if 'N/A' in title or '\r\n' == title or not title:
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
	#remove first newline with sub
	description = re.sub(pattern_first_newline, '', description)
	description = description.strip()
	
	
	if description == 'N/A' or not description:
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
		
"""
	By Alex Martelli on stackoverflow.
"""
def most_common_oneliner(L):
	result = max(groupby(sorted(L)), key=lambda(x, v):(len(list(v)),-L.index(x)))
	if result:
		return result[0]
	return None
	
def normalize_collection_name(name):
	if not name:
		return None
	name = re.sub(pattern_replace_name,'',name)
	return name

def convert_to_cm(value):
	return value

def convert_to_kg(value):
	return value
