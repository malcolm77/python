from youtubesearchpython import VideosSearch

videosSearch = VideosSearch('Highlights NFL 2024', limit = 20)

for i in range(10):
    print(videosSearch.result()['result'][i]['link'])
    # title = json['entry']['title']['$t']
    # author = json['entry']['author'][0]['name']
    # print ("id:%s\nauthor:%s\ntitle:%s" % (id, author, title))
