#!/usr/bin/python3

from youtubesearchpython import VideosSearch
import datetime

videosSearch = VideosSearch('Highlights NFL 2024', limit = 20)

print('<h1>NFL Highlights</h1>', file=open('/var/www/html/nfl.html', 'w'))

for i in range(10):
    # print(videosSearch.result()['result'][i]['link'])

    # title = json['entry']['title']['$t']
    # author = json['entry']['author'][0]['name']
    # print ("id:%s\nauthor:%s\ntitle:%s" % (id, author, title))

    title = videosSearch.result()['result'][i]['title'] 
    link = videosSearch.result()['result'][i]['link'] 
    posted = videosSearch.result()['result'][i]['publishedTime'] 
    print ( "%s %s ( %s )" % (title,link,posted) )

    with open('/var/www/html/nfl.html', 'a') as f:
      print ( "<a href='%s'> %s ( %s ) </a><br>" % (link,title,posted), file=f )

now = datetime.datetime.now()
print("<h6>" + now.strftime("%Y-%m-%d %H:%M:%S") + "</h6>", file=open('/var/www/html/nfl.html', 'a'))
