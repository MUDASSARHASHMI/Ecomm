from django.shortcuts import render

def template2(request):
    template = 'base.html'
    return render(request, template, {})
