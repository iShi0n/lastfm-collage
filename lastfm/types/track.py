import io
import re

import requests
from PIL import Image

from . import Artist


class Track:
    def __init__(self, mbid: str, name: str, artist: Artist, url: str) -> None:
        self.mbid = mbid
        self.name = name
        self.artist = artist
        self.url = url
        self.image = self._get_image()

    def _get_image(self) -> Image.Image:
        """Busca imagem da música no site do lastfm (API não retorna.)

        obs: caso a música não tenha imagem, será retornada uma imagem do artista.

        Returns:
            Image.Image: Imagem encontrada.
        """

        response = requests.get(self.url)
        # https://stackoverflow.com/a/19511971/13030478
        found = re.search(r'(?s)<span class=\"cover-art\"*?>.*?<img.*?src=\"([^\"]+)\"', response.text)

        if found:
            image_url = found.groups()[0]
            image_content = requests.get(image_url).content

            return Image.open(io.BytesIO(image_content))

        return self.artist.image
