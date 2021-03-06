import io
import re

import requests
from PIL import Image, ImageDraw, ImageFont

from . import Artist


class Track:
    def __init__(self, mbid: str, name: str, artist: Artist, url: str) -> None:
        self.mbid = mbid
        self.name = name
        self.artist = artist
        self.url = url
        self._image = None

    @property
    def image(self) -> Image.Image:
        if not self._image:
            self._image = self._get_image()
            self._image = self._image.resize((200, 200))
            font = ImageFont.truetype('framd.ttf', 12)
            ImageDraw.Draw(self._image).text((2, 2), self.name, font=font, stroke_fill=(0, 0, 0), stroke_width=1)

        return self._image

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

        return self.artist._get_image()
