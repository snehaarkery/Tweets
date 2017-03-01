from django.db import models
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream

try:
    import json
except ImportError:
    import simplejson as json

consumer_key = '4lu0KBdbkhRhK0zg4HEk9k3Wp'
consumer_secret = 'gowCnsCRUXidVmathcHVnml4c2B2QEuDu6XM5PXs8Tp1HEg7bz'
access_token = '4621122272-vpdd9KBuj0TPUETmBPcLIEfDK7puogaD1T9G6lq'
access_secret = '035CnvnwCdFoXNpMrpfslKGEZOfG7o3hurugofmKoTfMn'

auth = OAuthHandler(consumer_key, consumer_secret)
l = auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)
# store trends in dict
trends = api.trends_place(1)
for vol in (val for item, val in trends[0].iteritems() if item == 'trends'):
    trending_topic_indx = sorted(range(len(vol)), key=lambda k: vol[k]['tweet_volume'])[::-10]
    trending_topic_names = [vol[i]['name'] for i in trending_topic_indx]

trending = models.CharField(('Trending'), max_length=10, choices=trending_topic_names, default=trending_topic_names[0])