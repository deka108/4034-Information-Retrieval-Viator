import urllib


def search_by_field(core_name, query, *args):
    URL_NAME = "http://localhost:8983/solr/{core}/select?q=" + query
    
    if (len(args)>0):
        URL_NAME += "&fl="
        for i in range(len(args)):
            URL_NAME += args[i]
    URL_NAME = URL_NAME.format(core=core_name)
    urllib.urlopen(URL_NAME)

def search_with_facet(core_name, query, *args):
    #*args:
    #
    URL_NAME = "http://localhost:8983/solr/{core}/select?q=" + query + "&facet=true"
    if (len(args)>0):
        for i in range(len(args)):
            URL_NAME += "&" + args[i]
    URL_NAME = URL_NAME.format(core=core_name)
    urllib.urlopen(URL_NAME)

def group_by_field(core, query, group_field, *args):
    URL_NAME = "http://localhost:8983/solr/{core}/select?q=" + query + "&group=true"
    URL_NAME += "group.field=" + group_field
    if (len(args)>0):
        for i in range(len(args)):
            URL_NAME += "&" + args[i]
    URL_NAME = URL_NAME.format(core=core_name)
    urllib.urlopen(URL_NAME)
    
    
    
