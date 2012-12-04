#encoding=utf-8

from copy import copy

class CategoryLoopError(Exception):

    def __init__(self, catpath):
        self.catpath = catpath

class Article:

    def __init__(self, site, article):
        self.site = site
        self.titles = [article]
        self.maxdepth = 8
        self.fetchcats()

    def fetchcats(self):
        """ Fetches categories an overcategories for a set of articles """
        debug = False
        site = self.site
        titles = self.titles
        
        # Make a list of the categories of a given article, with one list for each level
        # > cats[article_key][level] = [cat1, cat2, ...]

        cats = { p: [[] for n in range(self.maxdepth)] for p in titles }

        # Also, for each article, keep a list of category parents, so we can build 
        # a path along the category tree from any matched category to the article
        # > parents[article_key][category] = parent_category
        #
        # Example:
        #                   /- cat 2
        #             /- cat1 -|
        # no:giraffe -|        \-
        #             \- 
        #
        # parents['no:giraffe']['cat2'] = 'cat1'
        # parents['no:giraffe']['cat1'] = 'giraffe'
        #
        # We could also build full category trees for each article from the available 
        # information, but they can grow quite big and slow to search
        
        parents = { p: {} for p in titles }

        #ctree = Tree()
        #for p in pages:
        #    ctree.add_child( name = p.encode('utf-8') )
            
        if 'bot' in site.rights:
            requestlimit = 500
            returnlimit = 5000
        else:
            requestlimit = 50
            returnlimit = 500
        
        #log(' ['+site_key+':'+str(len(titles))+']', newline = False)
        #.flush()
        if len(titles) > 0:
    
            for level in range(self.maxdepth):

                titles0 = copy(titles)
                titles = [] # make a new list of titles to search
                nc = 0
                nnc = 0
        
                for s0 in range(0, len(titles0), requestlimit):
                    if debug:
                        print
                        print "[%d] > Getting %d to %d of %d" % (level, s0, s0+requestlimit, len(titles0))
                    ids = '|'.join(titles0[s0:s0+requestlimit])

                    cont = True
                    clcont = ''
                    while cont:
                        #print clcont
                        if clcont != '':
                            q = site.api('query', prop = 'categories', titles = ids, cllimit = returnlimit, clcontinue = clcont)
                        else:
                            q = site.api('query', prop = 'categories', titles = ids, cllimit = returnlimit)
                        
                        if 'warnings' in q:
                            raise StandardError(q['warnings']['query']['*'])

                        for pageid, page in q['query']['pages'].iteritems():
                            fulltitle = page['title']
                            shorttitle = fulltitle.split(':',1)[-1]
                            article_key = fulltitle
                            if 'categories' in page:
                                for cat in page['categories']:
                                    cat_title = cat['title']
                                    cat_short= cat_title.split(':',1)[1]
                                    follow = True
                                    #for d in self.ignore:
                                    #    if re.search(d, cat_short):
                                    #        if self.verbose:
                                    #            log(' - Ignore: "%s" matched "%s"' % (cat_title, d))
                                    #        follow = False
                                    if follow:
                                        nc += 1
                                        titles.append(cat_title)
                                        if level == 0:
                                            cats[article_key][level].append(cat_short)
                                            parents[article_key][cat_short] = fulltitle
                                            #print cat_short 
                                            # use iter_search_nodes instead?
                                            #ctree.search_nodes( name = fulltitle.encode('utf-8') )[0].add_child( name = cat_short.encode('utf-8') )
                                        else:
                                            for article_key, ccc in cats.iteritems():
                                                if shorttitle in ccc[level-1]:
                                                    ccc[level].append(cat_short)
                                                    parents[article_key][cat_short] = shorttitle

                                                    #for node in ctree.search_nodes( name = shorttitle.encode('utf-8') ):
                                                    #    if not cat_short.encode('utf-8') in [i.name for i in node.get_children()]:
                                                    #        node.add_child(name = cat_short.encode('utf-8'))
                                    else:
                                        nnc += 1
                        if 'query-continue' in q:
                            clcont = q['query-continue']['categories']['clcontinue']
                        else:
                            cont = False
                titles = list(set(titles)) # to remove duplicates (not order preserving)
                #if level == 0:
                #    cattree = [p for p in titles]
                #if self.verbose:
                #log(' %d' % (len(titles)), newline = False)
                #.stdout.flush()
                #print "Found %d unique categories (%d total) at level %d (skipped %d categories)" % (len(titles), nc, level, nnc)


        #return cats, parents 
        self.cats = cats
        self.parents = parents
        

    def in_cat(self, catname):
        """ Checks if article_cats contains any of the cats given in self.include """
        # loop over levels
        for cats in self.cats[self.titles[0]]:
            if catname in cats:
                return True
        return False

    def get_path(self, catname):
        if not self.in_cat(catname):
            return ''
   
        cat_path = [catname]
        try:
            i = 0
            article_key = self.titles[0]
            while not catname == self.titles[0]:
                #print ' [%d] %s' % (i,catname)
                if not self.parents[article_key][catname] == article_key:
                    cat_path.append(self.parents[article_key][catname])
                catname = self.parents[article_key][catname]
                i += 1
                if i > 50:
                    raise CategoryLoopError(cat_path)
        except CategoryLoopError as e:
            print u'Havnet i en endeløs kategorisløyfe : ' + u' → '.join([u'[[:Kategori:%s|%s]]' % (c,c) for c in e.catpath])
        
        return cat_path
