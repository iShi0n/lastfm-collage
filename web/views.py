from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render

from lastfm import LastFM


def index(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user = request.POST.get('user', '')

        if not user:
            # TODO: criar página de erro
            return HttpResponseBadRequest('<h1>Parâmetros inválidos</h1>')

        lastfm = LastFM(settings.LASTFM_API_KEY)

        collage = lastfm.gen_top_albums_collage(user)
        response = HttpResponse(content_type='image/png')
        collage.save(response, 'PNG')

        return response
    elif request.method == 'GET':
        return render(request, 'index.html')
    else:
        return HttpResponse('Método não permitido.', status=405)
