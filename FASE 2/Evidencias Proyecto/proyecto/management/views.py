from django.shortcuts import render
from .forms import CustomUserCreationForm
from django.shortcuts import redirect
from .models import Acreditador
from django.contrib import messages

# Create your views here.
def dashboard(request):
    return render(request, 'management/dashboard.html')

def registro(request):

    data = {
        'form': CustomUserCreationForm()    
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            user = formulario.save()
            messages.success(request, f'Usuario para {user.first_name} {user.last_name} creado correctamente')
            return redirect('dashboard')
        else:
            for error in formulario.errors.values():
                messages.error(request, error)
    else:
        formulario = CustomUserCreationForm()

    return render(request, 'management/acreditadores.html', data)