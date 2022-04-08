from django.conf import settings
from django.http import HttpRequest, JsonResponse

from lastfm import LastFM


def generate(request: HttpRequest) -> JsonResponse:
    last = LastFM(settings.LASTFM_API_KEY)
    albums = last.get_top_albums('guibszin')

    return JsonResponse({
        "albums": [album.as_dict() for album in albums],
    })

    # TODO
