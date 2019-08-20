from django.shortcuts import render


def index(request):
    context = {'hello': 'stock'}
    return render(request, 'index.html', context)
