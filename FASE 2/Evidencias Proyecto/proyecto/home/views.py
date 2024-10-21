from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactoForm

def index(request):
    return render(request, 'home/index.html')

@csrf_exempt  # This allows POST requests without CSRF token in case it's not passed
def qr(request):
 
    access_list = {
        "105272": "AAA ACCESS",
        "105260": "A ACCESS",
        "105259": "AA ACCESS",
        "105258": "AA ACCESS",
    }  
 
    if request.method == 'POST':
        qr_data = request.POST.get('qr_data')
        
        if qr_data:
            print(f"QR Code Data: {qr_data}")
            # Return a JSON response with the QR data
 
            if qr_data in access_list:
                result = access_list[qr_data]
            else:
                result = "No Autorizado"
 
            return JsonResponse({'success': True, 'qr_data': f"Nivel de Acceso: {result}"})
 
 
        return JsonResponse({'success': False, 'message': 'Error en el envio.'})
 
    # If GET request, just render the HTML template
    return render(request, 'home/qr.html')

def contacto(request):

    data = {
        'form': ContactoForm()
    }

    return render(request, 'home/contacto.html', data)

def events(request):
    return render(request, 'events/crear_evento.html')
