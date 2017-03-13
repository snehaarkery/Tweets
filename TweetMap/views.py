from django.shortcuts import render
import tweepy
from tweepy import OAuthHandler, StreamListener, Stream
import time
import json
from elasticsearch import Elasticsearch, RequestsHttpConnection
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
import geocoder
import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth

es_host = "search-twittermaps-vruzd4lsovcog62ty5uilg7flm.us-west-2.es.amazonaws.com"
auth = AWSRequestsAuth(aws_access_key="AKIAIUHMGTRSV4R3PC4Q",
                       aws_secret_access_key="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",
                       aws_host=es_host,
                       aws_region="us-west-2",
                       aws_service="es")

es = Elasticsearch(host=es_host,
                          port=80,
                          connection_class=RequestsHttpConnection,
                          http_auth=auth)

# es = Elasticsearch()

consumer_key = '4lu0KBdbkhRhK0zg4HEk9k3Wp'
consumer_secret = 'gowCnsCRUXidVmathcHVnml4c2B2QEuDu6XM5PXs8Tp1HEg7bz'
access_token = '4621122272-vpdd9KBuj0TPUETmBPcLIEfDK7puogaD1T9G6lq'
access_secret = '035CnvnwCdFoXNpMrpfslKGEZOfG7o3hurugofmKoTfMn'

auth = OAuthHandler(consumer_key, consumer_secret)
authAPI = auth.set_access_token(access_token, access_secret)


class listener(StreamListener):
    def __init__(self, time_limit=60):
        self.time = time.time()
        self.limit = time_limit
        self.data = []
        super(listener, self).__init__()


    def on_data(self, data):
        if (time.time() - self.time) < self.limit:
            tweet_data = json.loads(data)
            if tweet_data['place'] is not None:
                try:
                    # self.data.append(tweet_data)
                    # print tweet_data.keys()
                    placecoord = tweet_data['place']['bounding_box']['coordinates'][0][0]
                    print placecoord
                    lat = placecoord[1]
                    longi = placecoord[0]
                    doc = {
                        'title': tweet_data['text'],
                        'location': {
                            'lat': lat,
                            'longi': longi
                        }
                    }
                    # print doc['title']
                    es.index(index="tweetindex", doc_type="Collections", id=tweet_data['id'], body=doc)
                except Exception as e:
                    print "place error ", e
                return True
            elif tweet_data['place'] is None and tweet_data['user'] is not None and tweet_data['user']['location'] is not None:
                try:
                    doc = {
                        'title' : tweet_data["text"],
                        'location' : {
                            'lat': geocoder.google(tweet_data['user']['location']).latlng[0],
                            'longi': geocoder.google(tweet_data['user']['location']).latlng[1],
                        }
                    }
                    # print "user doc", doc['location']['lat'], doc['location']['longi']
                    es.index(index="tweetindex", doc_type="Collections", id=tweet_data['id'], body=doc)
                except Exception as e:
                    print "user error ", e
                return True
            elif tweet_data['place'] is None and tweet_data['user']['location'] is None:
                print "else loop"
                return True
        else:
            # self.appendfile()
            return False

    def appendfile(self):
        with open('./raw_1.json', 'w') as f:
            json.dump(self.data, f)

    def on_error(self, status):
        print("response: %s" % status)
        if status == 420:
            return False

@csrf_protect
def filter(request):
    # print "yes"
    if request.method == "POST":
        try:
            # print request.method
            if 'input' in request.POST:
                query = str(request.POST.get('input', ''))
                # print query
                try:
                    l = listener(time_limit=60)
                    twitter_stream = Stream(auth, l)
                    twitter_stream.filter(track=[query])
                    tweets = es.search(index='tweetindex', body={"from": 0, "size": 1000, "query": {"match": {"title":query}}})
                    # print tweets.keys()
                    latlonginfo = []
                    for tweet in tweets['hits']['hits']:
                        info = {}
                        info['lat'] = tweet['_source']['location']['lat']
                        info['longi'] = tweet['_source']['location']['longi']
                        info['title'] = tweet['_source']['title']
                        latlonginfo.append(info)
                        print (info)
                    # print latlonginfo
                    return JsonResponse({'tweets' : latlonginfo})
                except Exception as e:
                    print e
                    return HttpResponse('Error')
        except Exception as e:
            print e

@csrf_protect
def init(request):
    api = tweepy.API(auth)
    trends = api.trends_place(1)
    trending_topic_names = []
    for vol in (val for item, val in trends[0].iteritems() if item == 'trends'):
        trending_topic_indx = sorted(range(len(vol)), key=lambda k: vol[k]['tweet_volume'])[::-20]
        trending_topic_names = [vol[i]['name'] for i in trending_topic_indx]
    print(trending_topic_names)
    return render(request, 'TweetMap/home.html', {'trendings': trending_topic_names})

if __name__ == '__main__':
    filter('Trump')