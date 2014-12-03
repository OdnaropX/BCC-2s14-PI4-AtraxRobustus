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
	

#Tags most used.
#tags = dbase.select('entity_has_tag', ['count(*) as total', 'name'], "entity.classification_type_id <> 17 group by name order by total desc limit 300", [], ['tag', 'entity'], ['tag_id = id', 'entity_id = entity.id'])

#new_view = v.Visualization()
#new_view.cloud_words('teste1.png', tags)

#collections = dbase.select()

#Collection with most items
'''
#collections = dbase.select('(select collection_id from entity where collection_id IS NOT NULL UNION ALL select collection_id from goods where collection_id IS NOT NULL ) as temp_table', ['count(*) as total', 'collection.name', 'char_length(collection.name)'], "collection.name not like '__' and collection.name not like ' 'and collection.name not like '___' group by collection.name having count(*) > 1 order by total desc, collection.name limit 400", [], ['collection'], ['collection.id = collection_id'])
new_view = v.Visualization()

mask = Image.new("L", (2450, 1440))
draw = ImageDraw.Draw(mask)
draw.rectangle([0,0,2450,240], fill='white', outline='white')
#mask = Image.open("base-2450.jpg")

#new_view.cloud_words('teste-mask-e-comp2.png', collections, 2450, 1440, (255, 255, 255), mask, False)

#mask = Image.new("L", (2450, 1440))
mask = imread("e-comp-2450.png")
#mask.convert('L')
#draw = ImageDraw.Draw(mask)
#draw.rectangle([0,0,2450,240], fill='white', outline='white')

new_view.cloud_words('teste-mask-comp-text3.png', collections, 2450, 1440, (255, 255, 255), None,mask, False)
'''


'''
Autores
Editoras

Volume de Tags, Volume de Franquias, Itens de Franquias

Autores, Tradutores, Editores, 

Volume produtos, valor das franquias
'''
new_view = v.Visualization()


#search
results = []



sql = 'select collection.name, sum(coalesce(height, 100) * coalesce(width, 100) * coalesce(length, 100))/1000000 as total, char_length(collection.name) from goods join collection on collection.id = collection_id where collection.name not like %s and collection.name not like %s and collection.name not like %s group by collection.name having count(*) > 1 order by total desc;'
where_values = []
where_values.append('_')
where_values.append('__')
where_values.append('___')

if(dbase.change(sql, where_values)):
	result = dbase.cursor.fetchall();
	results.append(result)
	new_view.cloud_bubbles('item_bubbles_1.png', result, (2450, 1440), (255, 255, 255), (0,200))
	new_view.cloud_words('item_words_1.png', result, (2450, 1440), (255, 255, 255), (0,200))

#print len(results_years)
#print len(results)