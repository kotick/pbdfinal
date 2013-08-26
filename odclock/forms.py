# -*- encoding: utf-8 -*-
from django import forms
from odclock.models import *

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Rut'}),label= 'RUN',)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}),label= 'Contraseña')

class RegisForm(forms.Form):
	username =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'RUN'}),label= 'RUN')
	nombres =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Nombre'}),label= 'Nombres')
	apellidop =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Apellido'}),label= 'Apellidos')
	apellidom =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Apellido'}),label= 'Apellidos')
	email1 =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Correo Electronico'}),label= 'Correo Electronico')
	email2 =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Correo Electronico'}),label= 'Nuevamente el correo electronico')
	password1 =forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Contraseña'}),label= 'Contraseña')
	password2 =forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Contraseña'}),label= 'Nuevamente la contraseña')


class ModificarP(forms.Form):
	contrasena1=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}),label= 'Contraseña Actual')
	contrasena2=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}),label= 'Nueva Contraseña')
	contrasena3=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}),label= 'Nueva Contraseña')

class ModificarE(forms.Form):
	correo1=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Correo Electronico'}),label= 'Nuevo Correo Electronico')
	correo2=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Correo Electronico'}),label= 'Nuevo Correo Electronico')

class ModificarTc(forms.Form):
	telefonoc1=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Telefono Celular'}),label= 'Nuevo telefono Celular')
	telefonoc2=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Telefono Celular'}),label= 'Nuevo telefono Celular')

class ModificarTf(forms.Form):
	telefonof1=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Telefono Fijo'}),label= 'Nuevo telefono Fijo')
	telefonof2=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Telefono Fijo'}),label= 'Nuevo telefono Fijo')

class AgregarDentista(forms.Form):
	username =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'RUN'}),label= 'RUN')
	nombres =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Nombre'}),label= 'Nombres')
	apellidop =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Apellido'}),label= 'Apellidos')
	apellidom =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Apellido'}),label= 'Apellidos')
	email =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Correo Electronico'}),label= 'Correo Electronico')
	password =forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Contraseña'}),label= 'Contraseña')
	telefonof =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Telefono Fijo'}),label= 'Telefono')
	telefonoc =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Telefono Celular'}),label= 'Telefono')
	run_colegio = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Telefono Celular'}),label= 'Telefono')

class EliminarDentista(forms.Form):
	username =forms.ModelChoiceField(queryset=Dentista.objects.all().filter(desabilitado=False),widget=forms.Select(),label= 'RUN')

class NombrarAdministrador(forms.Form):
	username =forms.ModelChoiceField(queryset=User.objects.all(),widget=forms.Select(),label= 'RUN')

class IngresarOferta(forms.Form):
	usernameio =forms.ModelChoiceField(queryset=Dentista.objects.all().filter(desabilitado=False),widget=forms.Select(),label= 'RUN')

class BorrarOferta(forms.Form):
	username =forms.ModelChoiceField(queryset=Dentista.objects.all().filter(desabilitado=False),widget=forms.Select(),label= 'RUN')

class AsignarEspecialidad(forms.Form):
	username =forms.ModelChoiceField(queryset=Dentista.objects.all().filter(desabilitado=False),widget=forms.Select(),label= 'RUN')
	especialidad = forms.ModelChoiceField(queryset=Especialidad.objects.all().filter(desabilitado=False),widget=forms.Select(),label= 'RUN')

class DesasignarEspecialidad(forms.Form):
	username =forms.ModelChoiceField(queryset=Dentista.objects.all().filter(desabilitado=False),widget=forms.Select(),label= 'RUN')
	especialidad = forms.ModelChoiceField(queryset=Especialidad.objects.all().filter(desabilitado=False),widget=forms.Select(),label= 'RUN')

class AgregarEspecialidad(forms.Form):
    nombre = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Nombre'}),label= 'Nombre')
    cantidad = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Numero de Bloques estimada'}),label= 'N°')

class EliminarEspecialidad(forms.Form):
	identificador =forms.ModelChoiceField(queryset=Especialidad.objects.all().filter(desabilitado=False),widget=forms.Select(),label= 'Nombre de  la especialidad')

class AgregarBox(forms.Form):
    nombre = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Nombre'}),label= 'Nombre')

class EliminarBox(forms.Form):
	identificador =forms.ModelChoiceField(queryset=Box.objects.all().filter(desabilitado=False),widget=forms.Select(),label= 'Numero de Box')

class AgregarSecretaria(forms.Form):
	username =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'RUN'}),label= 'RUN')
	nombres =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Nombre'}),label= 'Nombres')
	apellidop =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Apellido'}),label= 'Apellidos')
	apellidom =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Apellido'}),label= 'Apellidos')
	email =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Correo Electronico'}),label= 'Correo Electronico')
	password =forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Contraseña'}),label= 'Contraseña')
	telefonof =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Telefono Fijo'}),label= 'Telefono')
	telefonoc =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Telefono Celular'}),label= 'Telefono')

class EliminarSecretaria(forms.Form):
	username =forms.ModelChoiceField(queryset=Secretaria.objects.all().filter(desabilitado=False),widget=forms.Select(),label= 'RUN')

class Verficha(forms.Form):
	username =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'RUN'}),label= 'RUN')

class VerhorariosE(forms.Form):
	especialidad =forms.ModelChoiceField(queryset=Especialidad.objects.all().filter(desabilitado=False),widget=forms.Select(),label= 'Seleccione una especialidad')

tipo_choice=(('Agendada','Agendada'),('Urgencia','Urgencia'))

class VerhorariosD(forms.Form):
	dentista =forms.ChoiceField(widget=forms.Select(),label= 'Ahora seleccione un dentista')

class IngresarAtencion(forms.Form):
	Tipo = forms.ChoiceField(choices=tipo_choice)
	paciente= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Rut del paciente'}),label= 'Paciente atendido')
	plan = forms.ModelChoiceField(queryset=Plan_tratamiento.objects.all().filter(desabilitado=False),widget=forms.Select(),label= 'Plan de Tratamiento')
	box = forms.ModelChoiceField(queryset=Box.objects.all().filter(desabilitado=False),widget=forms.Select(),label= 'Box utilizado')
	detalles = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Detalles'}),label= 'Detalles de la atención')

class CancelarHora(forms.Form):
	paciente= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Rut del paciente'}),label= 'Paciente atendido')