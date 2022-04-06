from typing import List

import requests

from .types import Album, Artist, Image


class LastFM:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def get_top_albums(self, user: str) -> List[Album]:
        response = requests.get(f"https://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user={user}&api_key={self.api_key}&format=json")
        response_json = response.json()

        albums = []

        for album in response_json['topalbums']['album']:
            artist = Artist(**album['artist'])

            images = []

            for image in album['image']:
                image['url'] = image.pop("#text")
                images.append(Image(**image))

            album.pop('artist')
            album.pop('image')
            album.pop('@attr')

            albums.append(Album(artist=artist, images=images, **album))

        return albums
