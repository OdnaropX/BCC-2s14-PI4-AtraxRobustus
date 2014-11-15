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

def get_formatted_date(date):
	if not date:
		return '1900-01-01'
	if '-' in date:
		split_type = '-'
	elif '/' in date:
		split_type = '/'
	else:
		return '1900-01-01'
		
	new_date = date.split(split_type)
	day, month, year = '28', '01', '1900' 
	next = None
	
	if len(new_date) == 2:
		if len(new_date[1]) == 4:
			year = new_date[1]
			next = new_date[0]
			number = convert_to_number(new_date[0])
		else:
			year = new_date[0]
			next = new_date[1]
			number = convert_to_number(new_date[1])
			
		if number > 12:
			month = next
		else:
			day = next
		
	elif len(new_date) == 3:
		month = new_date[1]
		if len(new_date[0]) == 4:
			year = new_date[0]
			day = new_date[2]
		else:
			year = new_date[2]
			day = new_date[0]
		
		if convert_to_number(month) > 12:
			new_day = month
			month = day
			day = new_day
		
	else:#1 date format.
		if len(new_date[0]) == 4:
			year = new_date[0].strip()
		else:
			number = convert_to_number(new_date[0])
			if number < 20:
				year = number + 2000
			else:
				year = number + 1900
			
	n_date = "{0}-{1}-{2}".format(year, month, day)
	
	return n_date
	
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
		new_title = ""
		for item in title:
			if isinstance(item, types.StringTypes):
				new_title = new_title + join_string + item
			else:
				new_title = new_title + join_string + str(item)
		return new_title
		
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
	if name:
		return name.title()
	return None

def convert_to_cm(value):
	return value

def convert_to_kg(value):
	return value

def get_formatted_tag(tag):
	if not tag:
		return None
	
	tag = sanitize_title(tag)
	
	if not tag:
		return None
		
	tag = tag.replace('_', ' ')
	return tag.title()