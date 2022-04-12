import io
import re

import requests
from PIL import Image


class Artist:
    def __init__(self, url: str, name: str, mbid: str) -> None:
        self.url = url
        self.name = name
        self.mbid = mbid
        self._image = None

    @property
    def image(self) -> Image.Image:
        if not self._image:
            self._image = self._get_image()

        return self._image

    def _get_image(self) -> Image.Image:
        """Busca imagem do artista no site do last.fm (a API não retorna imagem de artistas).

        Returns:
            Image.Image: Imagem encontrada.
        """

        response = requests.get(self.url + '/+images')
        found = re.search('https://lastfm.freetls.fastly.net/i/u/avatar170s/.*?(?=\")', response.text)

        if found:
            # Altera a URL para conseguir uma imagem com a resolução maior.
            image_url = found.group().replace('avatar170s', '770x0')
            image_content = requests.get(image_url).content

            return Image.open(io.BytesIO(image_content))

        return

    def as_dict(self) -> dict:
        return {
            "url": self.url,
            "name": self.name,
            "mbid": self.mbid
        }
