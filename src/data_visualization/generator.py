import visualization as v
import database
from PIL import Image
from PIL import ImageDraw
from scipy.misc import imread

DBNAME = 'te'
DBUSERNAME = 'teste'
DBPASSWORD = '123456'
DBHOST = 'localhost'
DBPORT = '5432'
MUUSERNAME = 'Teste2352'
MUPASSWORD = '=QWZ;=w)WZ;=w)@!)G'
			
dbase = database.Database(DBNAME, DBUSERNAME,DBPASSWORD, DBHOST,DBPORT)
if(dbase.connect() == False):
	raise SystemExit
else:
	print "Initialized database and parse"
	

#search
results = []
'''
sql = 'select collection.name, sum(coalesce(height, 100) * coalesce(width, 100) * coalesce(length, 100))/1000000 as total, char_length(collection.name) from goods join collection on collection.id = collection_id where collection.name not like %s and collection.name not like %s and collection.name not like %s group by collection.name having count(*) > 1 order by total desc;'
where_values = []
where_values.append('_')
where_values.append('__')
where_values.append('___')
if(dbase.change(sql, where_values)):
	result = dbase.cursor.fetchall();
	results.append(result)
	
sql = 'select collection.name, sum(coalesce(height, 100) * coalesce(width, 100) * coalesce(length, 100))/1000000000 as total, char_length(collection.name) from goods join collection on collection.id = collection_id where collection.name not like %s and collection.name not like %s and collection.name not like %s group by collection.name having count(*) > 1 order by total desc;'
where_values = []
where_values.append('_')
where_values.append('__')
where_values.append('___')

if(dbase.change(sql, where_values)):
	result = dbase.cursor.fetchall();
	results.append(result)
	
sql = 'select collection.name, sum(coalesce(height, 100) * coalesce(width, 100))/1000000, char_length(collection.name) as total, char_length(collection.name) from goods join collection on collection.id = collection_id where collection.name not like %s and collection.name not like %s and collection.name not like %s group by collection.name having count(*) > 1 order by total desc;'
where_values = []
where_values.append('_')
where_values.append('__')
where_values.append('___')

if(dbase.change(sql, where_values)):
	result = dbase.cursor.fetchall();
	results.append(result)
	

sql = 'select collection.name, sum(launch_price) * 0.023 as total, char_length(collection.name) from goods inner join goods_launch_country on goods_id = goods.id inner join collection on collection.id = collection_id where launch_price <> 0 and collection.name not like %s and collection.name not like %s and collection.name not like %s group by collection_id, collection.name having count(*) > 1 order by total desc;'
where_values = []
where_values.append('_')
where_values.append('__')
where_values.append('___')

if(dbase.change(sql, where_values)):
	result = dbase.cursor.fetchall();
	results.append(result)
	
sql = 'select collection.name, count(*) as total, char_length(collection.name) FROM (select entity.id, collection_id from entity where collection_id IS NOT NULL UNION ALL select id, collection_id from goods where collection_id IS NOT NULL) as temp_table join collection on collection.id = collection_id where collection.name not like %s and collection.name not like %s and collection.name not like %s group by collection.name having count(*) > 1 order by total desc, collection.name;'
where_values = []
where_values.append('_')
where_values.append('__')
where_values.append('___')

if(dbase.change(sql, where_values)):
	result = dbase.cursor.fetchall();
	results.append(result)
	
		
sql = 'select collection.name, count(*) as total, char_length(collection.name) FROM goods join collection on collection.id = collection_id left join figure on goods_id = goods.id where  goods_id IS NOT NULL and collection.name not like %s and collection.name not like %s and collection.name not like %s group by collection.name having count(*) > 1 order by total desc, collection.name;'
where_values = []
where_values.append('_')
where_values.append('__')
where_values.append('___')

if(dbase.change(sql, where_values)):
	result = dbase.cursor.fetchall();
	results.append(result)
	

sql = 'select entity_type.name, count(*) as total, char_length(entity_type.name) from entity join entity_type on entity_type.id = entity_type_id group by entity_type.name UNION ALL select %s, count(*), char_length(%s) from figure order by total desc;'
where_values = []
where_values.append("Figure")
where_values.append("Figure")

if(dbase.change(sql, where_values)):
	result = dbase.cursor.fetchall();
	results.append(result)
	
sql = 'select trim(name) as new_name, count(*) as total, char_length(trim(name)) from entity_has_tag join tag on tag_id = id join entity on entity_id = entity.id where entity.classification_type_id <> 17 and trim(name) not like %s and trim(name) not like %s and trim(name) not like %s and trim(name) not like %s group by new_name order by total desc;'
where_values = []
where_values.append('Rape')
where_values.append('Incest')
where_values.append('Group Intercourse')
where_values.append('Masturbation')

if(dbase.change(sql, where_values)):
	result = dbase.cursor.fetchall();
	results.append(result)
	
	
sql = 'select genre.name, genre.id, count (*) as total, char_length(genre.name) from entity_has_genre join genre on genre.id = genre_id join entity on entity.id = entity_has_genre.entity_id where genre.id < 39 group by genre.name, genre.id order by total;'

if(dbase.change(sql)):
	result = dbase.cursor.fetchall();
	results.append(result)
	'''	
sql = 'select name, count(*) as total, char_length(name) from (select people_id, create_type.name from people_create_goods join create_type on create_type.id = create_type_id where create_type_id <> 21 UNION select people_id, name from people_produces_entity join produces_type on produces_type_id = id) as temp_table group by name order by total desc;'

if(dbase.change(sql)):
	result = dbase.cursor.fetchall();
	results.append(result)
	
	
#Begin create visualization from results:
	
new_view = v.Visualization()
mask_array = None
#Uncomment this line if you want use mask, the mask must be a png file with 2 color (black and white): 
#mask_array = imread("e-comp-2450.png")

for index, result in enumerate(results):
	if index == 0:
		text = ('{0} litros', '{0} litro')
	elif index == 1:
		text = ('{0} m3', '{0} m3')
	elif index == 2:
		text = ('{0} m2', '{0} m2')
	elif index == 3:
		text = ('R$ {0}', 'R$ {0}')
	else:
		text = ('{0} itens', '{0} item')
		
	#new_view.cloud_words('item_words_{0}.png'.format(index), result, (1920, 1080), (255, 255, 255), (0,200), (None, None), False, True, mask_array)
	#new_view.cloud_bubbles('item_bubbles_{0}.png'.format(index), result, (1920, 1080), (255, 255, 255), text, (0,200), (None, None), False, True, mask_array)
	#new_view.cloud_words_html('item_words_{0}.html'.format(index), result, (1920, 1080), (255, 255, 255), (0,200), (None, None), False, True, mask_array)
	new_view.cloud_bubbles_html('item_bubbles_{0}.html'.format(index), result, (1920, 1080), (255, 255, 255), text, (0,200), (None, None), False, True, mask_array)

		
	
	
	
	
'''
	
############# Year ###############	
results_years = []

sql = 'select collection.name, sum(launch_price) * 0.023 as total, char_length(collection.name), substring( CAST (launch_date  AS varchar) from 0 for 5) as launch_year from goods inner join goods_launch_country on goods_id = goods.id inner join collection on collection.id = collection_id where launch_price <> 0 and collection.name not like %s and collection.name not like %s and collection.name not like %s and CAST( launch_date AS VARCHAR) not like %s group by collection.name, launch_year having count(*) > 1 order by launch_year, total desc;'
where_values = []
where_values.append('_')
where_values.append('__')
where_values.append('___')
where_values.append('%1900%')

if(dbase.change(sql, where_values)):
	result = dbase.cursor.fetchall();
	results_years.append(result)
	
	
sql = 'select collection.name, count(*), char_length(collection.name), year as total FROM (select entity.id, collection_id, substring( entity.launch_year from 0 for 5) as year from entity where collection_id IS NOT NULL and launch_year IS NOT NULL UNION ALL select id, collection_id, substring( CAST (l.launch_date  AS varchar) from 0 for 5) as year from goods join goods_launch_country as l on id = goods_id where collection_id IS NOT NULL) as temp_table join collection on collection.id = collection_id where collection.name not like %s and collection.name not like %s and collection.name not like %s and year <> %s group by collection.name, year having count(*) > 1 order by year, total, collection.name;'
where_values = []
where_values.append('_')
where_values.append('__')
where_values.append('___')
where_values.append('1900')

if(dbase.change(sql, where_values)):
	result = dbase.cursor.fetchall();
	results_years.append(result)
	
		
sql = 'select collection.name, sum(coalesce(height, 100) * coalesce(width, 100) * coalesce(length, 100))/1000000, char_length(collection.name), substring( CAST (launch_date  AS varchar) from 0 for 5) as launch_year from goods inner join goods_launch_country on goods_launch_country.goods_id = goods.id inner join collection on collection.id = collection_id  left join figure on figure.goods_id = goods.id where figure.goods_id IS NOT NULL and collection.name not like %s and collection.name not like %s and collection.name not like %s and CAST( launch_date AS VARCHAR) not like %s group by collection.name, launch_year having count(*) > 1 order by launch_year desc;'
where_values = []
where_values.append('_')
where_values.append('__')
where_values.append('___')
where_values.append('%1900%')

if(dbase.change(sql, where_values)):
	result = dbase.cursor.fetchall();
	results_years.append(result)
	
		
sql = 'select collection.name, sum(coalesce(height, 100) * coalesce(width, 100) * coalesce(length, 100))/1000000000, char_length(collection.name), substring( CAST (launch_date  AS varchar) from 0 for 5) as launch_year from goods inner join goods_launch_country on goods_launch_country.goods_id = goods.id inner join collection on collection.id = collection_id  left join figure on figure.goods_id = goods.id where figure.goods_id IS NOT NULL and collection.name not like %s and collection.name not like %s and collection.name not like %s and CAST( launch_date AS VARCHAR) not like %s group by collection.name, launch_year having count(*) > 1 order by launch_year desc;'
where_values = []
where_values.append('_')
where_values.append('__')
where_values.append('___')
where_values.append('%1900%')

if(dbase.change(sql, where_values)):
	result = dbase.cursor.fetchall();
	results_years.append(result)
	
sql = 'select collection.name, sum(coalesce(height, 100) * coalesce(width, 100))/1000000, char_length(collection.name), substring( CAST (launch_date  AS varchar) from 0 for 5) as launch_year from goods inner join goods_launch_country on goods_launch_country.goods_id = goods.id inner join collection on collection.id = collection_id  left join figure on figure.goods_id = goods.id where figure.goods_id IS NOT NULL and collection.name not like %s and collection.name not like %s and collection.name not like %s and CAST( launch_date AS VARCHAR) not like %s group by collection.name, launch_year having count(*) > 1 order by launch_year desc;'
where_values = []
where_values.append('_')
where_values.append('__')
where_values.append('___')
where_values.append('%1900%')

if(dbase.change(sql, where_values)):
	result = dbase.cursor.fetchall();
	results_years.append(result)
	
sql = 'select collection.name, count(*) as total, char_length(collection.name), substring( CAST (launch_date  AS varchar) from 0 for 5) as launch_year from goods inner join goods_launch_country on goods_launch_country.goods_id = goods.id inner join collection on collection.id = collection_id  left join figure on figure.goods_id = goods.id where figure.goods_id IS NOT NULL and collection.name not like %s and collection.name not like %s and collection.name not like %s and CAST( launch_date AS VARCHAR) not like %s group by collection.name, launch_year having count(*) > 1 order by launch_year, total desc;'
where_values = []
where_values.append('_')
where_values.append('__')
where_values.append('___')
where_values.append('%1900%')

if(dbase.change(sql, where_values)):
	result = dbase.cursor.fetchall();
	results_years.append(result)
		
sql = 'select entity_type.name, count(*) as total, char_length(entity_type.name), substring(launch_year from 0 for 5) as year from entity join entity_type on entity_type.id = entity_type_id where launch_year is not null and launch_year not like %s and launch_year not like %s and launch_year not like %s group by entity_type.name, cast(launch_year as varchar) UNION ALL select %s as item, count(*) as total, char_length(%s), substring( CAST (launch_date  AS varchar) from 0 for 5 ) as year from figure join goods_launch_country as g on g.goods_id = figure.goods_id where substring( CAST (launch_date  AS varchar) from 0 for 5 ) <> %s group by item, year order by year asc, total desc;'
where_values = []
where_values.append('%1900%')
where_values.append('%<%')
where_values.append('T%')
where_values.append('Figure')
where_values.append('Figure')
where_values.append('1900')

if(dbase.change(sql, where_values)):
	result = dbase.cursor.fetchall();
	results_years.append(result)
		
sql = 'select trim(name) as new_name, count(*) as total, char_length(trim(name)), substring(launch_year from 0 for 5) as year from entity_has_tag join tag on tag_id = id join entity on entity_id = entity.id where entity.classification_type_id <> 17 and trim(name) not like %s and trim(name) not like %s and trim(name) not like %s and trim(name) not like %s and launch_year not like %s group by new_name, year order by year, total desc;'
where_values = []
where_values.append('Rape')
where_values.append('Incest')
where_values.append('Group Intercourse')
where_values.append('Masturbation')
where_values.append('<%')

if(dbase.change(sql, where_values)):
	result = dbase.cursor.fetchall();
	results_years.append(result)
		
sql = 'select genre.name, count(*) as total, char_length(genre.name), substring(launch_year from 0 for 5) as year from entity_has_genre join genre on genre_id = genre.id join entity on entity.id = entity_has_genre.entity_id where launch_year is not null and launch_year not like %s and launch_year not like %s and genre.id < 39 group by genre.name, year order by year;'
where_values = []
where_values.append('%<%')
where_values.append('%T%')

if(dbase.change(sql, where_values)):
	result = dbase.cursor.fetchall();
	results_years.append(result)
	
#print len(results_years)
#print len(results)

'''