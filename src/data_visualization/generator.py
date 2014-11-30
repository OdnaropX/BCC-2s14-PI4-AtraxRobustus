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
where_values = []
where_values.append('_Re')
where_values.append('_re')
where_values.append('__')
where_values.append('01 ')
where_values.append('0 ')
where_values.append('2 ')
where_values.append(' R')

collections = dbase.select('(select collection_id from entity where collection_id IS NOT NULL UNION ALL select collection_id from goods where collection_id IS NOT NULL ) as temp_table', ['count(*) as total', 'collection.name', 'char_length(collection.name)'], "collection.name not like '__' and collection.name not like ' 'and collection.name not like '___' group by collection.name having count(*) > 1 order by total desc, collection.name limit 400", [], ['collection'], ['collection.id = collection_id'])
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
Autores
Editoras

Volume de Tags, Volume de Franquias, Itens de Franquias

Autores, Tradutores, Editores, 

Volume produtos, valor das franquias
'''
