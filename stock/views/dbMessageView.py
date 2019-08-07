from django.shortcuts import render


def db_message(request):
    context = {'hello': 'hello world'}
    return render(request, 'hello.html', context)
