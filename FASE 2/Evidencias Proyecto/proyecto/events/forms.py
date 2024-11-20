from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from management.models import Evento
from bootstrap_datepicker_plus.widgets import DatePickerInput

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nom_evento', 'fec_inicio', 'fec_termino', 'imagen', 'accmin', 'accmax', 'activo']  # Add 'imagen' here

        widgets = {
            'fec_inicio': DatePickerInput(options={"format": "DD/MM/YYYY"}),
            'fec_termino': DatePickerInput(options={"format": "DD/MM/YYYY"}, range_from='fec_inicio'),
        }
    
    def __init__(self, *args, **kwargs):
        super(EventoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Guardar'))