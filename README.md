
Example:
````
import mwclient, mwcats
a = mwcats.Article(site, 'Norway')
site = mwclient.Site('en.wikipedia.org')
a = mwcats.Article(site, 'Norway')
a.get_path('Space technology')
ls
hist
a.parents
a.get_path('Wars involving Iran')
hist
a.parents
a.get_path('Structural geology')
a.get_path('Life skills')
a.get_path('Hazards')
a = mwcats.Article(site, 'Cake')
a.parents
a.get_path('Subjects taught in medical school')
````
returns
````
['Subjects taught in medical school',
 u'Neurology',
 u'Intelligence',
 u'Skills',
 u'Food and drink preparation',
 u'Cooking',
 u'Cooking techniques',
 u'Foods by cooking technique',
 u'Baked goods',
 u'Cakes']
````
