from django.shortcuts import render
from django.http import HttpResponse


def index(request, ):
    return render(request, 'TweetMap/map.html')

def contact(request):
    return render(request, 'TweetMap/basic.html', {'content' : ['contact me at shaivi']})

# class StreamListener(tweepy.StreamListener):
#
#     def on_status(self, status):
#         print(status.user.location)
#
#     def on_error(self, status_code):
#         if status_code == 420:
#             return False

#TODO use get method with id=1 to take 50 trending topics and then display any 10
#TODO use that quesry to search tweets relevent to that name ,
#extract the location and display the marker on it trens available se karna hga




