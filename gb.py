# coding=utf-8
""" 
Google books search

Usage:
    gb <search> [-t=<title> | --title=<title>] [-a=<auth> | --auth=<auth>] [-e | --exact] [-d | --details] [-m=<integer> | --max=<integer>]
    gb <search> [-a=<auth> | --auth=<auth>] [-t=<title> | --title=<title>] [-e | --exact] [-d | --details] [-m=<integer> | --max=<integer>]
    gb title <title> [-a=<auth> | --auth=<auth>] [-d | --details] [-m=<integer> | --max=<integer>]
    gb auth <auth> [-t=<title> | --title=<title>] [-d | --details] [-m=<integer> | --max=<integer>]

Options:
    -h --help                           Show this screen.
    -t=<title>, --title=<title>         Search in title.
    -a=<auth>, --auth=<auth>            Search in author
    -m=<integer>, --max=<integer>       Number of results [default: 10].
    -d, --details                       Bibliographic details [default: False].
    -e, --exact                         Search exact phrase [default: False].

Commands:
    title       Search in title [default: False].
    auth        Search in author [default: False].

 """
import requests
import docopt
import sys
from textwrap import wrap
import os
import config

class gbooks():
    
    googleapikey=config.api_key # insert your own google books api key here

    def search(self, search=None, title=None, auth=None, exact=False, maxResults=10):
        value = ""
        if search:
            value = search
            if exact: value = '"' + value + '"'
            value += ' '
        if title:
            value += f'intitle:"{title}" '
        if auth:
            value += f'inauthor:"{auth}"'
        if value[-1] == ' ': value = value[:-1]

        params = {'q':value, 'key':self.googleapikey, 'maxResults': maxResults}
        r = requests.get(url='https://www.googleapis.com/books/v1/volumes', params=params)
        rj = r.json()
        global items_returned
        items_returned = len(rj.get('items', ""))
        if items_returned == 0:
            print("\nNo results\n")
            sys.exit()
        global total_items
        total_items = rj['totalItems']
        l = []
        d = {}
        for i in range(0, int(maxResults) + 1):
            try:
                l.append({'title': rj['items'][i]['volumeInfo'].get('title'),
                 'author': rj['items'][i]['volumeInfo'].get('authors'),
                 'isbn': rj['items'][i]['volumeInfo'].get('industryIdentifiers'),
                 'access': rj['items'][i]['accessInfo'].get('accessViewStatus'),
                 'date': rj['items'][i]['volumeInfo'].get('publishedDate'),
                 'link': rj['items'][i]['volumeInfo'].get('canonicalVolumeLink'),
                 'snipp': self.cleanText(rj['items'][i]['searchInfo'].get('textSnippet'))})
            except:
                pass
        return l

    def cleanText(self, textString):
        textString = textString.replace("&quot;", "")
        textString = textString.replace("<b>", "")
        textString = textString.replace("<br>", "")
        textString = textString.replace("</b>", "")
        textString = textString.replace("&nbsp;", "")
        textString = textString.replace("&#39;", "'")
        return textString

def main():
    try:
        args = docopt.docopt(__doc__,)
    except docopt.DocoptExit:
        print(__doc__)
        sys.exit()
    search = args['<search>']; auth = (args['<auth>'] or args['--auth']); title = (args['<title>'] or args['--title'])
    maxResults=args['--max']
    gbs = gbooks()
    result = gbs.search(search=search, title=title, auth=auth, exact=args['--exact'], maxResults=maxResults)
    print("\r")
    print("".join((["~"]*70)))
    for i in range(0, len(result)):
        print("\r")
        print("\n".join(wrap(result[i]['snipp'], width=70)))
        if args['--details']:
            print("\n".join(wrap(str([result[i][key] for key in ('title', 'author', 'date')]), width=70)), "\n")
        else:
            print("\r")
        print("".join((["~"]*70)), "\r")
    if items_returned > 1:
        print(f"{items_returned} results of {total_items}")
    elif items_returned == 1:
        print(f"{items_returned} result of {total_items}")

    print("\n")

if __name__ == '__main__':
    main()
  