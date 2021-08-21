import requests
import json


class Errors:
    class InvalidArgument(Exception):
        pass


class References:
    def __init__(self, references):
        self.group = references.get('group')


class Myxbitly:
    def __init__(self, key) -> str:
        self.key = key

    def shorten(self, url: str, **kwargs):
        for argument in [i.lower() for i in kwargs.keys()]:
            if not argument in ('long_url', 'domain', 'group_guid'):
                raise Errors.InvalidArgument(
                    f'Invalid argument: "{argument}".')
        if url.startswith(('http://', 'https://')) is False:
            raise Errors.InvalidArgument(
                f'URL must begin with either "http://" or "https://".')
        req = requests.post(url="https://api-ssl.bitly.com/v4/shorten",
                            data=json.dumps({
                                'long_url': url,
                                **kwargs
                            }),
                            headers={
                                'Authorization': self.key
                            }).json()
        self.created_at = req['created_at']
        self.id = req['id']
        self.link = req['link']
        self.custom_bitlinks = req['custom_bitlinks']
        self.long_url = req['long_url']
        self.archived = req['archived']
        self.tags = req['tags']
        self.deeplinks = req['deeplinks']
        self.references = References(req['references'])
        return self