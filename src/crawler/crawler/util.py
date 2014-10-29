import sys
import linecache
import re
import collections

pattern_last_newline = re.compile(ur'\n$')
pattern_last_bracket = re.compile(ur'\[$')
		
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
	
def PrintException():
	exc_type, exc_obj, tb = sys.exc_info()
	f = tb.tb_frame
	lineno = tb.tb_lineno
	filename = f.f_code.co_filename
	linecache.checkcache(filename)
	line = linecache.getline(filename, lineno, f.f_globals)
	print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)

def LogFail():
	print "Error"
	
def sanitize_title(title):
	#remove type from title.
			
	#remove last newline with sub
	title = re.sub(pattern_last_newline, '', title)
	title = title.strip()
	if(title == 'N/A'):
		return None
	return title
			
def sanitize_content(description):
	if not description:
		return None
		
	#if description is list join.
	if(isinstance(description, collections.Iterable)):
		description = "\n".join(description)
	#remove extra space. 
	description = description.strip()
	#remove last \n with sub.
	description = re.sub(pattern_last_newline, '', description)
	description = re.sub(pattern_last_bracket, '', description)
			
	if(description == 'N/A'):
		return None
	return description