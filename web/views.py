from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views import View

from lastfm import LastFM


class IndexView(View):
    lastfm = LastFM(settings.LASTFM_API_KEY)

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'index.html')

    def post(self, request: HttpRequest) -> HttpResponse:
        user = request.POST.get('user')
        category = request.POST.get('category', '').lower()
        period = request.POST.get('period', '').lower()
        # TODO: adicionar limit no front
        limit = request.POST.get('limit', 26)

        if not all([user, category, period, limit]):
            # TODO: criar página de erro
            return HttpResponse('<h1>Parâmetros inválidos</h1>', status=422)

        try:
            if category == 'album':
                collage = self.lastfm.gen_top_albums_collage(user, period, limit)
            elif category == 'artist':
                collage = self.lastfm.gen_top_artists_collage(user, period, limit)
            else:
                return HttpResponse('<h1>Parâmetros inválidos</h1>', status=422)

            response = HttpResponse(content_type='image/png')
            collage.save(response, 'PNG')

            return response
        except Exception as e:
            # TODO: criar página de erro
            return HttpResponse(f'<h1>{e}</h1>', status=500)
