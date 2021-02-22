from django.shortcuts import HttpResponse


def index(request):
    if request.user.is_authenticated:
        return HttpResponse('index.')
    else:
        return HttpResponse('index. log in.')
