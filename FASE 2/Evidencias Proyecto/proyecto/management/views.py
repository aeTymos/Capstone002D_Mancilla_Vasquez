from django.shortcuts import render
from .forms import CustomUserCreationForm
from django.shortcuts import redirect
from .models import Acreditador
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404

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
            return redirect('l_acreditadores')
        else:
            for error in formulario.errors.values():
                messages.error(request, error)
            data["form"] = formulario
    else:
        formulario = CustomUserCreationForm()

    return render(request, 'management/r_acreditadores.html', data)

def listado_acreditadores(request):

    acreditadores = Acreditador.objects.all()
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(acreditadores, 10)
        acreditadores = paginator.page(page)
    except:
        raise Http404    

    data = {
        'entity': acreditadores,
        'paginator': paginator,
    }

    return render(request, 'management/l_acreditadores.html', data)