from django.http import HttpRequest, JsonResponse


def generate(request: HttpRequest) -> JsonResponse:
    # TODO
    return JsonResponse({
        "todo": True,
    })
