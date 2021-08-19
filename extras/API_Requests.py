import json
import requests as r
import random

class animals:
    @classmethod
    def fox(self):
        res = r.get('https://randomfox.ca/floof/')
        res = res.content
        res = res.decode('utf-8').replace("'", '"')
        res = json.loads(res)
        return res['image']
    @classmethod
    def cat(self):
        res = r.get('https://aws.random.cat/meow?ref=apilist.fun')
        res = res.content
        res = res.decode('utf-8').replace("'", '"')
        res = json.loads(res)
        return res['file']
    @classmethod
    def dog(self):
        res = r.get('https://dog.ceo/api/breeds/image/random')
        res = res.content
        res = res.decode('utf-8').replace("'", '"')
        res = json.loads(res)
        return res['message']

class others:
    @classmethod
    def joke(self, safe=True):
        if safe is False:
            res = r.get('https://v2.jokeapi.dev/joke/Any?format=txt').content
            res = res.decode('utf-8')
            return res
        if safe is True:
            res = r.get('https://v2.jokeapi.dev/joke/Any?format=txt&safe-mode').content
            res = res.decode('utf-8')
            return res
    @classmethod 
    def dog_facts(self):
        res = r.get(f'https://dog-facts-api.herokuapp.com/api/v1/resources/dogs?index={random.randint(0, 434)}')
        res = res.content
        res = res.decode('utf-8').replace("'", '"')
        res = json.loads(res)
        res = res[0]['fact']
        return res
    @classmethod
    def cat_facts(self):
        res = r.get(f'https://catfact.ninja/fact')
        res = res.content
        res = res.decode('utf-8').replace("'", '"')
        res = json.loads(res)
        return res['fact']
