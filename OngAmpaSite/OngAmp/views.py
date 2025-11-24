from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def sobre(request):
    return render(request, 'sobre.html')


def contato(request):
    return render(request, 'contato.html')


def transp(request):
    return render(request, 'transparencia.html')