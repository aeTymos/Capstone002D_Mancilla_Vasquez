from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def qr(request):
    return render(request, 'home/qr.html')

def events(request):
    return render(request, 'events/crear_evento.html')