
Example:
````
import mwclient, mwcats
site = mwclient.Site('en.wikipedia.org')
a = mwcats.Article(site, 'Cake')
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
