from django.shortcuts import render

def base(request):
    template = 'base.html'
    return render(request, template, {})
