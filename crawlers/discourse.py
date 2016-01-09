# may factor into generic crawler interface + processor
import requests
from iso8601 import parse_date

class Discourse():
    def __init__(self,url,api_user,api_key):
        self.url = url.strip('/')
        self.api_key = api_key
        self.api_user = api_user

    def get(self,path):
        'get an API URL where list path is transformed into a JSON request and parsed'

        path = [str(p) for p in path]

        parts = [self.url] + path
        url = '/'.join(parts) + '.json'

        response = requests.get(
                url,
                params={
                    'api_user':self.api_user,
                    'api_key':self.api_key,
                }
        )
        response.raise_for_status()

        return response.json()

    #def list_category(name='Blog'):
    def list_articles(self,name='Facility Automation'):
        # find cetegory ID
        for cat in self.get(['categories'])['category_list']['categories']:
            id = cat['id']
            if name.lower() == cat['name'].lower():
                break
        else:
            raise IOError('Could not find category: %s'%name)

        # list topic IDs, collect usernames
        ids = list()
        for t in self.get(['c',id])['topic_list']['topics']:
            ids.append(t["id"])

        # load topics (containing posts: article then comments)
        #usernames = set()
            #usernames.add(t['username'])
        articles = list()
        for id in ids:
            topic = self.get(['t',id])
            articles.append({
                "title":topic['title'],
                "url": '/'.join([self.url,topic['slug'],str(id)]),
                #"image":"https://placeimg.com/710/100/tech",
                "content":topic['post_stream']['posts'][0]['cooked'],
                "author_image":"https://placeimg.com/100/100/tech",
                "author_name":"Callan Bryant",
                "published":parse_date(topic['post_stream']['posts'][0]['created_at']),
            })

        return articles

import os
# TODO decide on an interface
articles = Discourse(
    url="http://localhost:8099",
    api_user="naggie",
    api_key=os.environ['API_KEY'],
).list_articles()
