from django import forms  
from django.forms import ModelForm
from .models import *

class SurgeryForm(ModelForm):
    
    class Meta:
        model = Surgery
        fields = ('client', 'date', 'area', 'quantity', 'implant_type', 'implant_size','obs', 'stage', 'pmu')

        labels = {
            'client': 'Nome',
            'date': 'Data',
            'quantity': 'Quantidade',
            'area': 'Area cirurgica',
            'implant_type': 'Implante',
            'implant_size': 'Size',
            'obs': 'Observações',
            'stage': 'Estágio',
            'pmu': 'Tipo de Prótese'
        }
    
        #CLIENT = Client.objects.all() / choices=CLIENT
        STAGE = ['Espera', 'Andamento', 'Finalizado']
        PMU = [' ', 'Protocolo']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control',},),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'input_formats': 'DATE_FORMATS'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'type': 'number' ,'onchange': 'GetValue()', 'min': '1' ,'max': '8', 'value': '0', }),
            'area': forms.Select(attrs={'class': 'form-control'}),
            'implant_type': forms.Select(attrs={'class': 'form-control',}),
            'implant_size': forms.Select(attrs={'class': 'form-control',}),
            'obs': forms.Textarea(attrs={'class': 'form-control', 'rows': '5','cols': '20'}),
            'stage': forms.Select(attrs={'class': 'form-control'}, choices=STAGE),
            'pmu': forms.Select(attrs={'class': 'form-control'}, choices=PMU),
        }

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ('user', 'full_name', 'birth_date', 'gender', 'phone', 'obs',)

        labels = {
            'user': '',
            'full_name': 'Nome:',
            'birth_date': 'Data de Nascimento:',
            'gender': 'Gênero:',
            'phone': 'Telefone:',
            'obs': 'Obs:',
            
        }

        GENDER = ['Masculino', 'Feminino', 'Outro']

        widgets = {
            'user': forms.TextInput(attrs={'class': 'form-control', 'hidden': True}),
            'full_name': forms.TextInput(attrs={'class': 'form-control',}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date',}),
            'gender': forms.Select(attrs={'class': 'form-control'}, choices=GENDER,),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'obs': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
        }

class ImplantForm(ModelForm):
    imp =[]
    sizes = ['3.5x8','3.5x10','3.5x11.5','3.5x13','3.5x15','4.3x8','4.3x10','4.3x11.5','4.3x13','4.3x15']
    tipos = ['Neodent Alvim CM', 'Neodent Drive CM', 'SIN SWC CM', 'SIN Strong CM', 'SIN Unitite CM']
    for tipo in tipos:
        for size in sizes:
            impl = tipo + ' ' + size
            imp.append(impl)
    
    implantes = []
    for i in imp:
        impla = (str(i), str(i))
        implantes.append(impla)
    class Meta:
        tipos = ['Neodent Alvim CM', 'Neodent Drive CM', 'SIN SWC CM', 'SIN Strong CM', 'SIN Unitite CM']
        sizes = ['3.5x8','3.5x10','3.5x11.5','3.5x13','3.5x15','4.3x8','4.3x10','4.3x11.5','4.3x13','4.3x15']
        
        model = Implant
        fields = ('type', 'size','quantity', 'user')

        labels = {
            'type': 'Implante',
            'size': 'Tamanho',
            'quantity': 'Quantidade',
            'user': '',
        }


        widgets = {
            'type': forms.Select(attrs={'class': 'form-control', }, choices=tipos),
            'size': forms.Select(attrs={'class': 'form-control',}, choices=sizes),
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
            'user' : forms.TextInput(attrs={'class': 'form-control', 'default': 'asd'})
        }

