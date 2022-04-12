from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from lastfm import LastFM
from web.models import Size


class IndexView(View):
    lastfm = LastFM(settings.LASTFM_API_KEY)

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'index.html')

    def post(self, request: HttpRequest) -> HttpResponse:
        user = request.POST.get('user')
        category = request.POST.get('category', '').lower()
        period = request.POST.get('period', '').lower()
        size_name = request.POST.get('size', '5x5')

        if not all([user, category, period, size_name]):
            # TODO: criar página de erro
            return HttpResponse('<h1>Parâmetros inválidos</h1>', status=422)

        try:
            size = Size.objects.get(size=size_name)
        except ObjectDoesNotExist:
            return HttpResponse('<h1>Tamanho inválido</h1>', status=422)

        options = {
            'album': self.lastfm.gen_top_albums_collage,
            'artist': self.lastfm.gen_top_artists_collage,
            'track': self.lastfm.gen_top_tracks_collage
        }

        if category not in options.keys():
            return HttpResponse('<h1>Categoria inválida</h1>', status=422)

        try:
            category_function = options[category]
            collage = category_function(user, period, size.items, art_width=size.art_width, art_height=size.art_height, collage_width=size.collage_width, collage_height=size.collage_height)

            response = HttpResponse(content_type='image/png')
            collage.save(response, 'PNG')

            return response
        except Exception as e:
            # TODO: criar página de erro
            return HttpResponse(f'<h1>{e}</h1>', status=500)
