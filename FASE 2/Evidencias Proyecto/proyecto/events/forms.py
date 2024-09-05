from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from management.models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nom_evento', 'fec_inicio', 'fec_termino', 'imagen']  # Add 'imagen' here
    
    def __init__(self, *args, **kwargs):
        super(EventoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Guardar'))