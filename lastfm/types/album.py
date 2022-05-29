import io
from typing import List

import requests
from PIL import Image, ImageDraw, ImageFont

from .artist import Artist
from .image import AlbumImage


class Album:
    def __init__(self, artist: Artist, images: List[AlbumImage], mbid: str, url: str, playcount: str, name: str) -> None:
        self.artist = artist
        self.images = images
        self.mbid = mbid
        self.url = url
        self.playcount = int(playcount)
        self.name = name
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
        """Busca imagem do álbum.

        obs: caso a música não tenha imagem, será retornada uma imagem do artista.

        Returns:
            Image.Image: Imagem encontrada.
        """

        image_content = requests.get(self.images[-1].url).content

        return Image.open(io.BytesIO(image_content))

    def as_dict(self) -> dict:
        return {
            "artist": self.artist.name,
            "name": self.name,
            # Último item = maior qualidade.
            "art": self.images[-1].url
        }
