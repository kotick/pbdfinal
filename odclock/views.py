# -*- encoding: utf-8 -*-

# Core
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
 
# Forms
from forms import *
 
# Decorators
from django.contrib.auth.decorators import login_required
 
# Messages, Login, Logout and User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
 
# Models
from odclock.models import *
 
# JSON
from django.utils import simplejson
from django.utils.safestring import SafeString
 
# Data Structures
from django.utils.datastructures import SortedDict
 
# CACHE
from django.core.cache import cache
 
# CSV output
from django.template import loader, Context
import datetime


def index(request):
    title = 'Clinica Odontologica'
    return render_to_response(
        
        'index.html',
        {
            'title': title,
        },
        context_instance=RequestContext(request)
    )

def ubicacion(request):    
    title = 'Clinica Odontologica'
    return render_to_response(
        'ubicacion.html',
        {
            'title': title,
        },
        context_instance=RequestContext(request)
    )

def iniciosesionpaciente(request):
    title = 'Clinica Odontologica'    
    login_form = LoginForm()
    regis_form = RegisForm()
    return render_to_response(        
        'iniciosesionpaciente.html',
        {
            'title': title,            
            'login_form': login_form,
            'regis_form': regis_form,
        },
        context_instance=RequestContext(request)
    )

def iniciosesionpersonal(request):
    title = 'Clinica Odontologica'
    login_form = LoginForm()
    return render_to_response(        
        'iniciosesionpersonal.html',
        {
            'title': title,
            'login_form': login_form,
        },
        context_instance=RequestContext(request)
    )

def quienessomos(request):
    title = 'Clinica Odontologica'
    return render_to_response(
        'quienessomos.html',
        {
            'title': title,
        },
        context_instance=RequestContext(request)
    )

def login_view(request):
    if not request.user.is_anonymous():
        messages.error(request, 'Usted ya se encuentra dentro del sistema')
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if not form.is_valid():
            messages.error(request,"Formulario invalido")
            return HttpResponseRedirect("/")
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                usuario = User.objects.get(username=user)
                if usuario.first_name =='Paciente':
                    if usuario.paciente.desabilitado:
                        logout(request)
                        messages.warning(request, 'Tu cuenta ha sido eliminada.')
                        return HttpResponseRedirect('/')
                    else:
                        return HttpResponseRedirect('/paciente')
                else:
                    if usuario.first_name =='Dentista':
                        if usuario.dentista.desabilitado:
                            logout(request)
                            messages.warning(request, 'Tu cuenta ha sido eliminada.')
                            return HttpResponseRedirect('/')
                        else:
                            return HttpResponseRedirect('/dentista')

                    if usuario.first_name =='Secretaria':
                        if usuario.secretaria.desabilitado:
                            logout(request)
                            messages.warning(request, 'Tu cuenta ha sido eliminada.')
                            return HttpResponseRedirect('/')
                        else:
                            return HttpResponseRedirect('/secretaria')
            else:                
                messages.warning(request, 'Tu cuenta ha sido desactivada.')
                return HttpResponseRedirect('/')
        else:
            messages.error(request, 'Nombre de usuario o contraseña errónea.')
            return HttpResponseRedirect('/')
    else:
        messages.error(request, 'Error esta intentando acceder de forma indebida')
        return HttpResponseRedirect('/')

def paciente(request):
    if request.user.is_anonymous():
        messages.error(request, 'Por favor ingrese al sistema')
        return HttpResponseRedirect('/')

    title = 'Clinica Odontologica'
    usuario = User.objects.get(username=request.user)

    if request.user.first_name =='Dentista':
        messages.error(request, 'Usted no es un paciente')
        return HttpResponseRedirect('/')

    if request.user.first_name =='Secretaria':
        messages.error(request, 'Usted no es un paciente')
        return HttpResponseRedirect('/')

    if Paciente.objects.filter(user=usuario):
        agendamientos = Agendamiento.objects.filter(paciente= usuario.paciente)
        modificarp_form = ModificarP()
        modificare_form = ModificarE()
        modificartc_form = ModificarTc()
        modificartf_form = ModificarTf()
        verhorarioe_form=VerhorariosE()
        verhorariod_form=VerhorariosD()
        error = False
        return render_to_response(        
            'paciente.html',
            {
                'title': title,
                'agendamientos': agendamientos,
                'modificarp_form':modificarp_form,
                'modificare_form':modificare_form,
                'modificartc_form':modificartc_form,
                'modificartf_form':modificartf_form,
                'verhorarioe_form':verhorarioe_form,
                'verhorariod_form':verhorariod_form,
                'error':error,
            },
            context_instance=RequestContext(request)
        )
    else:
        messages.error(request, 'Lo sentimos, ocurrio un error')
        return HttpResponseRedirect('/sesionpaciente')

def dentista(request):
    if request.user.is_anonymous():
        messages.error(request, 'Por favor ingrese al sistema')
        return HttpResponseRedirect('/')
    title = 'Clinica Odontologica'
    usuario = User.objects.get(username=request.user)
    agendamientos=Agendamiento.objects.filter(dentista=usuario.dentista)
    verficha_form=Verficha()
    atencion_form=IngresarAtencion()
    modificarp_form = ModificarP()
    modificare_form = ModificarE()
    modificartc_form = ModificarTc()
    modificartf_form = ModificarTf()
    return render_to_response(
        'dentista.html',
        {
            'title': title,
            'atencion_form':atencion_form,
            'agendamientos':agendamientos,
            'verficha_form':verficha_form,
            'modificarp_form':modificarp_form,
            'modificare_form':modificare_form,
            'modificartc_form':modificartc_form,
            'modificartf_form':modificartf_form,
        },
        context_instance=RequestContext(request)
    )

def secretaria(request):
    if request.user.is_anonymous():
        messages.error(request, 'Por favor ingrese al sistema')
        return HttpResponseRedirect('/')

    title = 'Clinica Odontologica'
    return render_to_response(
        'secretaria.html',
        {
            'title': title,
        },
        context_instance=RequestContext(request)
    )
    
def administrador(request):
    if request.user.is_anonymous():
        messages.error(request, 'Por favor ingrese al sistema')
        return HttpResponseRedirect('/')
    if request.user.first_name =='Dentista':
        if request.user.last_name !='Administrador':
            messages.error(request, 'Usted no es un administrador')
            return HttpResponseRedirect('/dentista')
    if request.user.first_name =='Secretaria':
        if request.user.last_name !='Administrador':
            messages.error(request, 'Usted no es un administrador')
            return HttpResponseRedirect('/secretaria')    
    if request.user.first_name =='Paciente':
        messages.error(request, 'Usted no es un administrador')
        return HttpResponseRedirect('/')

    else:
        Adentista_form=AgregarDentista()
        Edentista_form=EliminarDentista()
        Ingresar_form=IngresarOferta()
        Borrar_form=BorrarOferta()
        Asignar_form=AsignarEspecialidad()
        Desasignar_form=DesasignarEspecialidad()
        Aespecialidad_form=AgregarEspecialidad()
        Eespecialidad_form=EliminarEspecialidad()
        Abox_form=AgregarBox()
        Ebox_form=EliminarBox()
        Asecretaria_form=AgregarSecretaria()
        Esecretaria_form=EliminarSecretaria()
        nombraradministrador_form=NombrarAdministrador()
        title = 'Clinica Odontologica'
        login_form = LoginForm()
        return render_to_response(        
            'administrador.html',
            {
                'title': title,
                'Adentista_form':Adentista_form,
                'Edentista_form':Edentista_form,
                'Ingresar_form':Ingresar_form,
                'Borrar_form':Borrar_form,
                'Asignar_form':Asignar_form,
                'Aespecialidad_form':Aespecialidad_form,
                'Eespecialidad_form':Eespecialidad_form,
                'Abox_form':Abox_form,
                'Ebox_form':Ebox_form,
                'nombraradministrador_form':nombraradministrador_form,
                'Asecretaria_form':Asecretaria_form,
                'Esecretaria_form':Esecretaria_form,
                'Desasignar_form':Desasignar_form,

            },
            context_instance=RequestContext(request)
        )

def crear_usuario(request):
    if not request.method == 'POST':
        messages.error(request, 'Error, esta intentando acceder de forma indebida')
        return HttpResponseRedirect('/')
    form = RegisForm(request.POST)
    if not form.is_valid():
        messages.error(request, 'Formulario malo, por favor revise los campos')
        return HttpResponseRedirect('/sesionpaciente')

    rut = form.cleaned_data['username']
    c=['1','2','3','4','5','6','7','8','9','0','k']
    if '-' in rut:
        lista=rut.split('-')    
        if len(lista[0])<7 or lista[1] not in c or len(lista[0])>8:
            messages.error(request, 'Rut invalido')
            return HttpResponseRedirect('/sesionpaciente')
        try:
            h=int(lista[0])
        except:
            messages.error(request, 'Rut invalido')
            return HttpResponseRedirect('/sesionpaciente')
    else:
        if len(rut)>9 or len(rut)<8:
            messages.error(request, 'Rut invalido')
            return HttpResponseRedirect('/sesionpaciente')
        if rut[-1]!='k':
            try:
                int (rut)
            except:
                messages.error(request, 'Rut invalido')
                return HttpResponseRedirect('/sesionpaciente')
    
    nombres = form.cleaned_data['nombres']
    apellidop = form.cleaned_data['apellidop']
    apellidom = form.cleaned_data['apellidom']
    pass1 = form.cleaned_data['password1']
    pass2 = form.cleaned_data['password2']
    email1 = form.cleaned_data['email1']
    email2 = form.cleaned_data['email2']


    if pass1 != pass2:
        messages.error(request, 'Las contraseñas ingresadas no coinciden')
        return HttpResponseRedirect('/sesionpaciente')

    if email2 != email1:
        messages.error(request, 'Los correos ingresados no coinciden')
        return HttpResponseRedirect('/sesionpaciente')

    existe = False
    usuarios = User.objects.all()
    for usuario in usuarios:
        if usuario ==rut:
            existe = True

    if existe:
        messages.error(request, 'Lo sentimos pero ese rut ya se encuentra registrado')
        return HttpResponseRedirect('/sesionpaciente')

    new_user = User(username=rut,email=email1,first_name="Paciente")
    new_user.set_password(pass1)
    new_user.save()
    new_paciente = Paciente(user=new_user,nombres=nombres,apellido_p=apellidop,apellido_m=apellidom)
    new_paciente.save()
    user = authenticate(username=rut, password=pass1)
    login(request, user)
    messages.success(request, 'Se ha registrado exitosamente, Bienvenido')
    return HttpResponseRedirect('/paciente')

def logout_view(request):
    if request.user.is_anonymous():
        messages.error(request, 'Por favor ingrese al sistema') 
        return HttpResponseRedirect('/')   
    logout(request)
    return HttpResponseRedirect('/')



def cambiarpass(request):
    if request.user.is_anonymous():
        messages.error(request, 'Por favor ingrese al sistema')
        return HttpResponseRedirect('/')
    if not request.method == 'POST':
        messages.error(request, 'Error, esta intentando acceder de forma indebida')
        return HttpResponseRedirect('/')
    form = ModificarP(request.POST)

    if not form.is_valid():
        messages.error(request, 'Formulario malo, por favor revise los campos')
        if usuario.first_name =="Paciente":
            return HttpResponseRedirect('/paciente')
        if usuario.first_name =="Dentista":
            return HttpResponseRedirect('/dentista')
        if usuario.first_name =="Secretaria":
            return HttpResponseRedirect('/secretaria')
    usuario =User.objects.get(username=request.user)
    pass1= form.cleaned_data['contrasena1']
    if not usuario.check_password(pass1):
        messages.error(request, 'Contraseña actual incorrecta')
        if usuario.first_name =="Paciente":
            return HttpResponseRedirect('/paciente')
        if usuario.first_name =="Dentista":
            return HttpResponseRedirect('/dentista')
        if usuario.first_name =="Secretaria":
            return HttpResponseRedirect('/secretaria')
    pass2 =form.cleaned_data['contrasena2']
    pass3 = form.cleaned_data['contrasena3']


    if pass2 != pass3:
        messages.error(request, 'Las contraseñas ingresadas no coinciden')
        if usuario.first_name =="Paciente":
            return HttpResponseRedirect('/paciente')
        if usuario.first_name =="Dentista":
            return HttpResponseRedirect('/dentista')
        if usuario.first_name =="Secretaria":
            return HttpResponseRedirect('/secretaria')

    usuario.set_password(pass3)
    usuario.save()
    messages.success(request, 'Se ha modificado la contraseña exitosamente')
    if usuario.first_name =="Paciente":
        return HttpResponseRedirect('/paciente')
    if usuario.first_name =="Dentista":
        return HttpResponseRedirect('/dentista')
    if usuario.first_name =="Secretaria":
        return HttpResponseRedirect('/secretaria')
    return HttpResponseRedirect('/')

def cambiaremail(request):
    if request.user.is_anonymous():
        messages.error(request, 'Por favor ingrese al sistema')
        return HttpResponseRedirect('/')
    if not request.method == 'POST':
        messages.error(request, 'Error, esta intentando acceder de forma indebida')
        return HttpResponseRedirect('/')
    form = ModificarE(request.POST)
    if not form.is_valid():
        messages.error(request, 'Formulario malo, por favor revise los campos')
        if user.first_name =="Paciente":
            return HttpResponseRedirect('/paciente')
        if user.first_name =="Dentista":
            return HttpResponseRedirect('/dentista')
        if user.first_name =="Secretaria":
            return HttpResponseRedirect('/secretaria')
    usuario =User.objects.get(username=request.user)

    email1 =form.cleaned_data['correo1']
    email2 = form.cleaned_data['correo2']

    if email1 != email2:
        messages.error(request, 'Los correos ingresados no coinciden')
        if usuario.first_name =="Paciente":
            return HttpResponseRedirect('/paciente')
        if usuario.first_name =="Dentista":
            return HttpResponseRedirect('/dentista')
        if usuario.first_name =="Secretaria":
            return HttpResponseRedirect('/secretaria')

    usuario.email= email1
    usuario.save()
    messages.success(request, 'Se ha modificado el correo exitosamente')    
    if usuario.first_name =="Paciente":
        return HttpResponseRedirect('/paciente')
    if usuario.first_name =="Dentista":
        return HttpResponseRedirect('/dentista')
    if usuario.first_name =="Secretaria":
        return HttpResponseRedirect('/secretaria')
    return HttpResponseRedirect('/')

def cambiartelefonoc(request):
    if request.user.is_anonymous():
        messages.error(request, 'Por favor ingrese al sistema')
        return HttpResponseRedirect('/')
    if not request.method == 'POST':
        messages.error(request, 'Error, esta intentando acceder de forma indebida')
        return HttpResponseRedirect('/')
    form = ModificarTc(request.POST)
    if not form.is_valid():
        messages.error(request, 'Formulario malo, por favor revise los campos')
        if user.first_name =="Paciente":
            return HttpResponseRedirect('/paciente')
        if user.first_name =="Dentista":
            return HttpResponseRedirect('/dentista')
        if user.first_name =="Secretaria":
            return HttpResponseRedirect('/secretaria')

    usuario =User.objects.get(id=request.user.id)
    telefonoc1 =form.cleaned_data['telefonoc1']
    telefonoc2 = form.cleaned_data['telefonoc2']

    if telefonoc1 != telefonoc2:
        messages.error(request, 'Los telefonos ingresados no coinciden')
        if user.first_name =="Paciente":
            return HttpResponseRedirect('/paciente')
        if user.first_name =="Dentista":
            return HttpResponseRedirect('/dentista')
        if user.first_name =="Secretaria":
            return HttpResponseRedirect('/secretaria')
    if usuario.first_name =="Paciente":
        paciente = Paciente.objects.get(user = usuario)
        paciente.telefono_c= telefonoc1
        paciente.save()
        messages.success(request, 'Se ha modificado el numero de telefono celular exitosamente')
        return HttpResponseRedirect('/paciente')
    if usuario.first_name =="Dentista":
        dentista = Dentista.objects.get(user = usuario)
        dentista.telefono_c= telefonoc1
        dentista.save()
        messages.success(request, 'Se ha modificado el numero de telefono celular exitosamente')        
        return HttpResponseRedirect('/dentista')
    if usuario.first_name =="Secretaria":
        secretaria = Secretaria.objects.get(user = usuario)
        secretaria.telefono_c= telefonoc1
        secretaria.save()
        messages.success(request, 'Se ha modificado el numero de telefono celular exitosamente')
        return HttpResponseRedirect('/secretaria')
    return HttpResponseRedirect('/')

def cambiartelefonof(request):
    if request.user.is_anonymous():
        messages.error(request, 'Por favor ingrese al sistema')
        return HttpResponseRedirect('/')

    if not request.method == 'POST':
        messages.error(request, 'Error, esta intentando acceder de forma indebida')
        return HttpResponseRedirect('/')

    form = ModificarTf(request.POST)
    if not form.is_valid():
        messages.error(request, 'Formulario malo, por favor revise los campos')
        if user.first_name =="Paciente":
            return HttpResponseRedirect('/paciente')
        if user.first_name =="Dentista":
            return HttpResponseRedirect('/dentista')
        if user.first_name =="Secretaria":
            return HttpResponseRedirect('/secretaria')

    usuario =User.objects.get(username=request.user)
    telefonof1 =form.cleaned_data['telefonof1']
    telefonof2 = form.cleaned_data['telefonof2']

    if telefonof1 != telefonof2:
        messages.error(request, 'Los telefonos ingresados no coinciden')
        if user.first_name =="Paciente":
            return HttpResponseRedirect('/paciente')
        if user.first_name =="Dentista":
            return HttpResponseRedirect('/dentista')
        if user.first_name =="Secretaria":
            return HttpResponseRedirect('/secretaria')
    if usuario.first_name =="Paciente":
        paciente = Paciente.objects.get(user = usuario)
        paciente.telefono_f= telefonof1
        paciente.save() 
        messages.success(request, 'Se ha modificado el numero de telefono fijo exitosamente')       
        return HttpResponseRedirect('/paciente')
    if usuario.first_name =="Dentista":
        dentista = Dentista.objects.get(user = usuario)
        dentista.telefono_f= telefonof1
        dentista.save()
        messages.success(request, 'Se ha modificado el numero de telefono fijo exitosamente')
        return HttpResponseRedirect('/dentista')
    if usuario.first_name =="Secretaria":
        secretaria = Secretaria.objects.get(user = usuario)
        secretaria.telefono_f= telefonof1
        secretaria.save()
        messages.success(request, 'Se ha modificado el numero de telefono fijo exitosamente')
        return HttpResponseRedirect('/secretaria')
    return HttpResponseRedirect('/')


def agregardentista(request):
    if request.user.is_anonymous():
        messages.error(request, 'Por favor ingrese al sistema')
        return HttpResponseRedirect('/')

    if not request.method == 'POST':
        messages.error(request, 'Error, esta intentando acceder de forma indebida')
        return HttpResponseRedirect('/')
    form = AgregarDentista(request.POST)

    if not form.is_valid():
        messages.error(request, 'Formulario malo, por favor revise los campos')
        return HttpResponseRedirect('/administrador')

    rut = form.cleaned_data['username']
    nombres = form.cleaned_data['nombres']
    apellidop = form.cleaned_data['apellidop']
    apellidom = form.cleaned_data['apellidom']
    password = form.cleaned_data['password']
    email = form.cleaned_data['email']
    telefonoc = form.cleaned_data['telefonoc']
    telefonof = form.cleaned_data['telefonof']
    run_colegio = form.cleaned_data['run_colegio']

    existe = False
    usuarios = User.objects.all()
    for usuario in usuarios:
        if usuario ==rut:
            existe = True

    if existe:
        messages.error(request, 'Lo sentimos pero ese rut ya se encuentra registrado')
        return HttpResponseRedirect('/administrador')
   
    new_user = User(username=rut,email=email,first_name="Dentista")
    new_user.set_password(password)
    new_user.save()
    new_dentista = Dentista(user=new_user,nombres=nombres,apellido_p=apellidop,apellido_m=apellidom,telefono_c=telefonoc,telefono_f=telefonof,run_colegio=run_colegio,administrador=False)
    new_dentista.save()
    messages.success(request,'Se ha ingresado un nuevo dentista')
    return HttpResponseRedirect('/administrador')


def agregarsecretaria(request):
    if request.user.is_anonymous():
        messages.error(request, 'Por favor ingrese al sistema')
        return HttpResponseRedirect('/')

    if not request.method == 'POST':
        messages.error(request, 'Error, esta intentando acceder de forma indebida')
        return HttpResponseRedirect('/')

    form = AgregarSecretaria(request.POST)
    if not form.is_valid():
        messages.error(request, 'Formulario malo, por favor revise los campos')
        return HttpResponseRedirect('/administrador')

    rut = form.cleaned_data['username']
    nombres = form.cleaned_data['nombres']
    apellidop = form.cleaned_data['apellidop']
    apellidom = form.cleaned_data['apellidom']
    password = form.cleaned_data['password']
    email = form.cleaned_data['email']
    telefonoc = form.cleaned_data['telefonoc']
    telefonof = form.cleaned_data['telefonof']

    existe = False
    usuarios = User.objects.all()
    for usuario in usuarios:
        if usuario ==rut:
            existe = True

    if existe:
        messages.error(request, 'Lo sentimos pero ese rut ya se encuentra registrado')
        return HttpResponseRedirect('/administrador')

    new_user = User(username=rut,email=email,first_name="Secretaria")
    new_user.set_password(password)
    new_user.save()
    new_secretaria = Secretaria(user=new_user,nombres=nombres,apellido_p=apellidop,apellido_m=apellidom,telefono_c=telefonoc,telefono_f=telefonof,administrador= False)
    new_secretaria.save()
    messages.success(request,'Se ha ingresado una nueva secretaria')
    return HttpResponseRedirect('/administrador')

def agregarespecialidad(request):
    if request.user.is_anonymous():
        messages.error(request, 'Por favor ingrese al sistema')
        return HttpResponseRedirect('/')

    if not request.method == 'POST':
        messages.error(request, 'Error, esta intentando acceder de forma indebida')
        return HttpResponseRedirect('/')

    form = AgregarEspecialidad(request.POST)

    if not form.is_valid():
        messages.error(request, 'Formulario malo, por favor revise los campos')
        return HttpResponseRedirect('/administrador')

    nombre = form.cleaned_data['nombre']
    cantidad = form.cleaned_data['cantidad']

    existe = False
    especialidades = Especialidad.objects.all()
    for especialidad in especialidades:
        if especialidad ==nombre:
            existe = True
    if existe:
        messages.error(request, 'Lo sentimos pero ya exite una especialidad con ese nombre y por politicas de la clinica esto no se puede hacer')
        return HttpResponseRedirect('/administrador')

    new_especialidad= Especialidad(nombre=nombre,cantidad_b=cantidad,desabilitado=False)
    new_especialidad.save()
    messages.success(request,'Se ha ingresado una nueva especialidad exitosamente')
    return HttpResponseRedirect('/administrador')

def agregarbox(request):
    if request.user.is_anonymous():
        messages.error(request, 'Por favor ingrese al sistema')
        return HttpResponseRedirect('/')

    if not request.method == 'POST':
        messages.error(request, 'Error, esta intentando acceder de forma indebida')
        return HttpResponseRedirect('/')
    form = AgregarBox(request.POST)

    if not form.is_valid():
        messages.error(request, 'Formulario malo, por favor revise los campos')
        return HttpResponseRedirect('/administrador')
    
    nombre = form.cleaned_data['nombre']

    existe = False
    boxes = Box.objects.all()
    for box in boxes:
        if box ==nombre:
            existe = True
    if existe:
        messages.error(request, 'Lo sentimos pero ya exite una box con ese nombre y por politicas de la clinica esto no se puede hacer')
        return HttpResponseRedirect('/administrador')

    new_box= Box(nombre=nombre,desabilitado=False)
    new_box.save()
    messages.success(request,'Se ha ingresado un nuevo box exitosamente')
    return HttpResponseRedirect('/administrador')
    

def eliminardentista(request):
    if request.user.is_anonymous():
        messages.error(request, 'Por favor ingrese al sistema')
        return HttpResponseRedirect('/')

    if not request.method == 'POST':
        messages.error(request, 'Error, esta intentando acceder de forma indebida')
        return HttpResponseRedirect('/')

    form = EliminarDentista(request.POST)

    if not form.is_valid():
        messages.error(request, 'Formulario malo, por favor revise los campos')
        return HttpResponseRedirect('/administrador')
    
    dentista = form.cleaned_data['username']
    dentista.desabilitado=True
    dentista.save()
    messages.success(request,'Se ha eliminado exitosamente')
    return HttpResponseRedirect('/administrador')

def eliminarsecretaria(request):
    if request.user.is_anonymous():
        messages.error(request, 'Por favor ingrese al sistema')
        return HttpResponseRedirect('/')

    if not request.method == 'POST':
        messages.error(request, 'Error, esta intentando acceder de forma indebida')
        return HttpResponseRedirect('/')
    form = EliminarSecretaria(request.POST)

    if not form.is_valid():
        messages.error(request, 'Formulario malo, por favor revise los campos')
        return HttpResponseRedirect('/administrador')

    secretaria = request.POST['username']
    secretaria.desabilitado=True
    secretaria.save()
    messages.success(request,'Se ha eliminado exitosamente')
    return HttpResponseRedirect('/administrador')


def eliminarespecialidad(request):
    if request.user.is_anonymous():
        messages.error(request, 'Por favor ingrese al sistema')
        return HttpResponseRedirect('/')

    if not request.method == 'POST':
        messages.error(request, 'Error, esta intentando acceder de forma indebida')
        return HttpResponseRedirect('/')

    form = EliminarEspecialidad(request.POST)

    if not form.is_valid():
        messages.error(request, 'Formulario malo, por favor revise los campos')
        return HttpResponseRedirect('/administrador')

    
    especialidad = form.cleaned_data['identificador']
    especialidad.desabilitado=True
    especialidad.save()
    messages.success(request,'Se ha eliminado exitosamente')
    return HttpResponseRedirect('/administrador')


def eliminarbox(request):
    if request.user.is_anonymous():
        messages.error(request, 'Por favor ingrese al sistema')
        return HttpResponseRedirect('/')

    if not request.method == 'POST':
        messages.error(request, 'Error, esta intentando acceder de forma indebida')
        return HttpResponseRedirect('/')

    form = EliminarBox(request.POST)

    if not form.is_valid():
        messages.error(request, 'Formulario malo, por favor revise los campos')
        return HttpResponseRedirect('/administrador')
    
    box = form.cleaned_data['identificador']
    box.desabilitado=True
    box.save()
    messages.success(request,'Se ha eliminado exitosamente')
    return HttpResponseRedirect('/administrador')


def asignarespecialidad(request):
    if request.user.is_anonymous():
        messages.error(request, 'Por favor ingrese al sistema')
        return HttpResponseRedirect('/')

    if not request.method == 'POST':
        messages.error(request, 'Error, esta intentando acceder de forma indebida')
        return HttpResponseRedirect('/')
    form = AsignarEspecialidad(request.POST)
    if not form.is_valid():
        messages.error(request, 'Formulario malo, por favor revise los campos')
        return HttpResponseRedirect('/administrador')
    
    especialidad = form.cleaned_data['especialidad']
    username = form.cleaned_data['username']

    union = Dentista_especialidad(dentista=username,especialidad=especialidad)
    union.save()
    messages.success(request,'Se ha asignado la especialidad exitosamente')
    return HttpResponseRedirect('/administrador')

def desasignarespecialidad(request):
    if request.user.is_anonymous():
        messages.error(request, 'Por favor ingrese al sistema')
        return HttpResponseRedirect('/')

    if not request.method == 'POST':
        messages.error(request, 'Error, esta intentando acceder de forma indebida')
        return HttpResponseRedirect('/')

    form = DesasignarEspecialidad(request.POST)
    if not form.is_valid():
        messages.error(request, 'Formulario malo, por favor revise los campos')
        return HttpResponseRedirect('/administrador')
    
    especialidad = form.cleaned_data['especialidad']
    username = form.cleaned_data['username']

    union = Dentista_especialidad.objects.get(dentista=username,especialidad=especialidad)
    messages.success(request,'Se ha desasignado la especialidad exitosamente')
    union.delete()
    
    return HttpResponseRedirect('/administrador')


def atencion(request):
    if request.user.is_anonymous():
        messages.error(request, 'Por favor ingrese al sistema')
        return HttpResponseRedirect('/')

    if not request.method == 'POST':
        messages.error(request, 'Error, esta intentando acceder de forma indebida')
        return HttpResponseRedirect('/')
    form = IngresarAtencion(request.POST)
    if not form.is_valid():
        messages.error(request, 'Formulario malo, por favor revise los campos')
        return HttpResponseRedirect('/administrador')

    return HttpResponseRedirect('/dentista')


def eliminaroferta(request):
    if request.user.is_anonymous():
        messages.error(request, 'Por favor ingrese al sistema')
        return HttpResponseRedirect('/')

    if not request.method == 'POST':
        messages.error(request, 'Error, esta intentando acceder de forma indebida')
        return HttpResponseRedirect('/')
    messages.warning(request,'Lo sentimos pero esta opcion se encuentra desabilitado por el momento, esperamos su comprension')
    return HttpResponseRedirect('/administrador')


def verficha(request):
    if request.user.is_anonymous():
        messages.error(request, 'Por favor ingrese al sistema')
        return HttpResponseRedirect('/')

    if not request.method == 'POST':
        messages.error(request, 'Error, esta intentando acceder de forma indebida')
        return HttpResponseRedirect('/')

    return HttpResponseRedirect('/dentista')

def nombraradministrador(request):
    if request.user.is_anonymous():
        messages.error(request, 'Por favor ingrese al sistema')
        return HttpResponseRedirect('/')

    if not request.method == 'POST':
        messages.error(request, 'Error, esta intentando acceder de forma indebida')
        return HttpResponseRedirect('/')


    form = NombrarAdministrador(request.POST)
    if not form.is_valid():
        messages.error(request, 'Formulario malo, por favor revise los campos')
        return HttpResponseRedirect('/administrador')

    new_administrador = form.cleaned_data['username']
    new_administrador.last_name = "Administrador" 
    new_administrador.save()
    messages.success(request,'Se designado exitosamente un nuevo administrador')
    return HttpResponseRedirect('/administrador')



def dameoferta(request):
    if request.user.is_anonymous():
        messages.error(request, 'Por favor ingrese al sistema')
        return HttpResponseRedirect('/')

    if not request.method == 'POST':
        messages.error(request, 'Error, esta intentando acceder de forma indebida')
        return HttpResponseRedirect('/')
    a=request.POST['a']
    lista=[]
    usuario =User.objects.get(username=request.user)
    oferta = Oferta_horaria.objects.filter(dentista=usuario.dentista)
    for ofer in oferta:
        if ofer.calendario.mes == a:
            lista.append(ofer.calendario.mes)
            lista.append(ofer.calendario.dia)
            lista.append(ofer.calendario.Bloque_horario)
    data = simplejson.dumps(lista)
    return HttpResponse(data, mimetype='application/json')

def ingresaroferta(request):
    hoy=datetime.datetime.now()
    mes=hoy.month+1
    usuario = User.objects.get(username=request.user)
    clicks=request.POST.keys()
    for click in clicks:
        if click == request.POST[click]:
            if click =="11":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="2",Bloque_horario=1)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="9",Bloque_horario=1)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="16",Bloque_horario=1)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="23",Bloque_horario=1)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="30",Bloque_horario=1)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
            if click =="21":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="2",Bloque_horario=2)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="9",Bloque_horario=2)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="16",Bloque_horario=2)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="23",Bloque_horario=2)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="30",Bloque_horario=2)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="31":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="2",Bloque_horario=3)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="9",Bloque_horario=3)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="16",Bloque_horario=3)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="23",Bloque_horario=3)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="30",Bloque_horario=3)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="41":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="2",Bloque_horario=4)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="9",Bloque_horario=4)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="16",Bloque_horario=4)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="23",Bloque_horario=4)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="30",Bloque_horario=4)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="51":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="2",Bloque_horario=5)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="9",Bloque_horario=5)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="16",Bloque_horario=5)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="23",Bloque_horario=5)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="30",Bloque_horario=5)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="61":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="2",Bloque_horario=6)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="9",Bloque_horario=6)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="16",Bloque_horario=6)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="23",Bloque_horario=6)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="30",Bloque_horario=6)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="71":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="2",Bloque_horario=7)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="9",Bloque_horario=7)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="16",Bloque_horario=7)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="23",Bloque_horario=7)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="30",Bloque_horario=7)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="81":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="2",Bloque_horario=8)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="9",Bloque_horario=8)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="16",Bloque_horario=8)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="23",Bloque_horario=8)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="30",Bloque_horario=8)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="91":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="2",Bloque_horario=9)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="9",Bloque_horario=9)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="16",Bloque_horario=9)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="23",Bloque_horario=9)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="30",Bloque_horario=9)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="101":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="2",Bloque_horario=10)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="9",Bloque_horario=10)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="16",Bloque_horario=10)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="23",Bloque_horario=10)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="30",Bloque_horario=10)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="111":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="2",Bloque_horario=11)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="9",Bloque_horario=11)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="16",Bloque_horario=11)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="23",Bloque_horario=11)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="30",Bloque_horario=11)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="121":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="2",Bloque_horario=12)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="9",Bloque_horario=12)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="16",Bloque_horario=12)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="23",Bloque_horario=12)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="30",Bloque_horario=12)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="131":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="2",Bloque_horario=13)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="9",Bloque_horario=13)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="16",Bloque_horario=13)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="23",Bloque_horario=13)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="30",Bloque_horario=13)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="141":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="2",Bloque_horario=14)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="9",Bloque_horario=14)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="16",Bloque_horario=14)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="23",Bloque_horario=14)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="30",Bloque_horario=14)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="151":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="2",Bloque_horario=15)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="9",Bloque_horario=15)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="16",Bloque_horario=15)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="23",Bloque_horario=15)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="30",Bloque_horario=15)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="161":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="2",Bloque_horario=16)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="9",Bloque_horario=16)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="16",Bloque_horario=16)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="23",Bloque_horario=16)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="30",Bloque_horario=16)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="12":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="3",Bloque_horario=1)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="10",Bloque_horario=1)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="17",Bloque_horario=1)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="24",Bloque_horario=1)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="22":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="3",Bloque_horario=2)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="10",Bloque_horario=2)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="17",Bloque_horario=2)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="24",Bloque_horario=2)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="32":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="3",Bloque_horario=3)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="10",Bloque_horario=3)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="17",Bloque_horario=3)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="24",Bloque_horario=3)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="42":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="3",Bloque_horario=4)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="10",Bloque_horario=4)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="17",Bloque_horario=4)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="24",Bloque_horario=4)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="52":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="3",Bloque_horario=5)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="10",Bloque_horario=5)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="17",Bloque_horario=5)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="24",Bloque_horario=5)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="62":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="3",Bloque_horario=6)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="10",Bloque_horario=6)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="17",Bloque_horario=6)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="24",Bloque_horario=6)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="72":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="3",Bloque_horario=7)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="10",Bloque_horario=7)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="17",Bloque_horario=7)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="24",Bloque_horario=7)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="82":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="3",Bloque_horario=8)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="10",Bloque_horario=8)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="17",Bloque_horario=8)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="24",Bloque_horario=8)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="92":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="3",Bloque_horario=9)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="10",Bloque_horario=9)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="17",Bloque_horario=9)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="24",Bloque_horario=9)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="102":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="3",Bloque_horario=10)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="10",Bloque_horario=10)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="17",Bloque_horario=10)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="24",Bloque_horario=10)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="112":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="3",Bloque_horario=11)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="10",Bloque_horario=11)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="17",Bloque_horario=11)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="24",Bloque_horario=11)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="122":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="3",Bloque_horario=12)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="10",Bloque_horario=12)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="17",Bloque_horario=12)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="24",Bloque_horario=12)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="132":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="3",Bloque_horario=13)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="10",Bloque_horario=13)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="17",Bloque_horario=13)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="24",Bloque_horario=13)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="142":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="3",Bloque_horario=14)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="10",Bloque_horario=14)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="17",Bloque_horario=14)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="24",Bloque_horario=14)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="152":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="3",Bloque_horario=15)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="10",Bloque_horario=15)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="17",Bloque_horario=15)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="24",Bloque_horario=15)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="162":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="3",Bloque_horario=16)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="10",Bloque_horario=16)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="17",Bloque_horario=16)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="24",Bloque_horario=16)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="13":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="4",Bloque_horario=1)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="11",Bloque_horario=1)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="18",Bloque_horario=1)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="25",Bloque_horario=1)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="23":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="4",Bloque_horario=2)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="11",Bloque_horario=2)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="18",Bloque_horario=2)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="25",Bloque_horario=2)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="33":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="4",Bloque_horario=3)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="11",Bloque_horario=3)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="18",Bloque_horario=3)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="25",Bloque_horario=3)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="43":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="4",Bloque_horario=4)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="11",Bloque_horario=4)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="18",Bloque_horario=4)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="25",Bloque_horario=4)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="53":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="4",Bloque_horario=5)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="11",Bloque_horario=5)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="18",Bloque_horario=5)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="25",Bloque_horario=5)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="63":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="4",Bloque_horario=6)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="11",Bloque_horario=6)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="18",Bloque_horario=6)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="25",Bloque_horario=6)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="73":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="4",Bloque_horario=7)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="11",Bloque_horario=7)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="18",Bloque_horario=7)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="25",Bloque_horario=7)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="83":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="4",Bloque_horario=8)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="11",Bloque_horario=8)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="18",Bloque_horario=8)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="25",Bloque_horario=8)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="93":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="4",Bloque_horario=9)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="11",Bloque_horario=9)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="18",Bloque_horario=9)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="25",Bloque_horario=9)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="103":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="4",Bloque_horario=10)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="11",Bloque_horario=10)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="18",Bloque_horario=10)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="25",Bloque_horario=10)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="113":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="4",Bloque_horario=11)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="11",Bloque_horario=11)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="18",Bloque_horario=11)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="25",Bloque_horario=11)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="123":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="4",Bloque_horario=12)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="11",Bloque_horario=12)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="18",Bloque_horario=12)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="25",Bloque_horario=12)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="133":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="4",Bloque_horario=13)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="11",Bloque_horario=13)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="18",Bloque_horario=13)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="25",Bloque_horario=13)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="143":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="4",Bloque_horario=14)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="11",Bloque_horario=14)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="18",Bloque_horario=14)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="25",Bloque_horario=14)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="153":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="4",Bloque_horario=15)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="11",Bloque_horario=15)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="18",Bloque_horario=15)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="25",Bloque_horario=15)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="163":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="4",Bloque_horario=16)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="11",Bloque_horario=16)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="18",Bloque_horario=16)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="25",Bloque_horario=16)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="14":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="5",Bloque_horario=1)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="12",Bloque_horario=1)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="19",Bloque_horario=1)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="26",Bloque_horario=1)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="24":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="5",Bloque_horario=2)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="12",Bloque_horario=2)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="19",Bloque_horario=2)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="26",Bloque_horario=2)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="34":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="5",Bloque_horario=3)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="12",Bloque_horario=3)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="19",Bloque_horario=3)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="26",Bloque_horario=3)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="44":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="5",Bloque_horario=4)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="12",Bloque_horario=4)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="19",Bloque_horario=4)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="26",Bloque_horario=4)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="54":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="5",Bloque_horario=5)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="12",Bloque_horario=5)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="19",Bloque_horario=5)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="26",Bloque_horario=5)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="64":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="5",Bloque_horario=6)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="12",Bloque_horario=6)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="19",Bloque_horario=6)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="26",Bloque_horario=6)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="74":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="5",Bloque_horario=7)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="12",Bloque_horario=7)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="19",Bloque_horario=7)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="26",Bloque_horario=7)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="84":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="5",Bloque_horario=8)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="12",Bloque_horario=8)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="19",Bloque_horario=8)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="26",Bloque_horario=8)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="94":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="5",Bloque_horario=9)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="12",Bloque_horario=9)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="19",Bloque_horario=9)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="26",Bloque_horario=9)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="104":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="5",Bloque_horario=10)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="12",Bloque_horario=10)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="19",Bloque_horario=10)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="26",Bloque_horario=10)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="114":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="5",Bloque_horario=11)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="12",Bloque_horario=11)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="19",Bloque_horario=11)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="26",Bloque_horario=11)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="124":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="5",Bloque_horario=12)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="12",Bloque_horario=12)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="19",Bloque_horario=12)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="26",Bloque_horario=12)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="134":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="5",Bloque_horario=13)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="12",Bloque_horario=13)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="19",Bloque_horario=13)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="26",Bloque_horario=13)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="144":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="5",Bloque_horario=14)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="12",Bloque_horario=14)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="19",Bloque_horario=14)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="26",Bloque_horario=14)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="154":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="5",Bloque_horario=15)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="12",Bloque_horario=15)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="19",Bloque_horario=15)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="26",Bloque_horario=15)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="164":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="5",Bloque_horario=16)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="12",Bloque_horario=16)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="19",Bloque_horario=16)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="26",Bloque_horario=16)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
            if click =="15":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="6",Bloque_horario=1)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="13",Bloque_horario=1)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="20",Bloque_horario=1)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="27",Bloque_horario=1)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="25":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="6",Bloque_horario=2)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="13",Bloque_horario=2)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="20",Bloque_horario=2)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="27",Bloque_horario=2)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="35":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="6",Bloque_horario=3)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="13",Bloque_horario=3)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="20",Bloque_horario=3)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="27",Bloque_horario=3)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="45":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="6",Bloque_horario=4)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="13",Bloque_horario=4)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="20",Bloque_horario=4)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="27",Bloque_horario=4)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="55":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="6",Bloque_horario=5)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="13",Bloque_horario=5)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="20",Bloque_horario=5)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="27",Bloque_horario=5)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="65":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="6",Bloque_horario=6)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="13",Bloque_horario=6)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="20",Bloque_horario=6)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="27",Bloque_horario=6)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="75":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="6",Bloque_horario=7)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="13",Bloque_horario=7)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="20",Bloque_horario=7)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="27",Bloque_horario=7)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="85":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="6",Bloque_horario=8)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="13",Bloque_horario=8)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="20",Bloque_horario=8)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="27",Bloque_horario=8)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="95":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="6",Bloque_horario=9)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="13",Bloque_horario=9)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="20",Bloque_horario=9)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="27",Bloque_horario=9)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="105":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="6",Bloque_horario=10)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="13",Bloque_horario=10)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="20",Bloque_horario=10)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="27",Bloque_horario=10)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="115":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="6",Bloque_horario=11)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="13",Bloque_horario=11)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="20",Bloque_horario=11)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="27",Bloque_horario=11)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="125":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="6",Bloque_horario=12)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="13",Bloque_horario=12)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="20",Bloque_horario=12)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="27",Bloque_horario=12)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="135":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="6",Bloque_horario=13)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="13",Bloque_horario=13)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="20",Bloque_horario=13)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="27",Bloque_horario=13)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="145":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="6",Bloque_horario=14)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="13",Bloque_horario=14)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="20",Bloque_horario=14)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="27",Bloque_horario=14)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="155":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="6",Bloque_horario=15)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="13",Bloque_horario=15)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="20",Bloque_horario=15)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="27",Bloque_horario=15)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
            if click =="165":
                a=Calendario.objects.get(ano=2013,mes=mes,dia="6",Bloque_horario=16)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()
                a=Calendario.objects.get(ano=2013,mes=mes,dia="13",Bloque_horario=16)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="20",Bloque_horario=16)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()                
                a=Calendario.objects.get(ano=2013,mes=mes,dia="27",Bloque_horario=16)
                b= Oferta_horaria(disponible=True,dentista=usuario.dentista,calendario=a)
                b.save()

    return HttpResponseRedirect('/dentista')

def ajaxespecialidad(request):
    a = request.POST['a']
    c = Especialidad.objects.get(nombre=a)
    b= Dentista_especialidad.objects.filter(especialidad=c)
    lista = []
    for u in b:
        lista.append(u.dentista.nombres)
    data = simplejson.dumps(lista)
    return HttpResponse(data, mimetype='application/json')

def ajaxdentista(request):
    a = request.POST['p']
    c = Especialidad.objects.get(nombre=a)
    b= Dentista_especialidad.objects.filter(especialidad=c)
    lista = []
    for u in b:
        lista.append(u.dentista)
        lista.append(",")
    lista.append("pico")
    return HttpResponse(lista)


def ajaxoferta(request):
    a = request.POST['a']
    lista = []
    b = Dentista.objects.get(nombres=a)
    oferta = Oferta_horaria.objects.filter(dentista=b).exclude(disponible=False)
    for hora in oferta:
        lista.append(hora.calendario.mes)
        lista.append(hora.calendario.dia)
        lista.append(hora.calendario.Bloque_horario)
    data = simplejson.dumps(lista)
    return HttpResponse(data, mimetype='application/json')

def tomarhora(request):
    usuario =User.objects.get(username=request.user)
    yo2= Paciente.objects.get(user=usuario)
    a = request.POST['idd']
    b = request.POST['esp']
    c = request.POST['den']
    a2 = a.split("-")
    a3 = Calendario.objects.get(dia=a2[1],mes=a2[0],Bloque_horario=a2[2])
    b2= Especialidad.objects.get(nombre=b)
    c3= Dentista.objects.get(nombres=c)
    final =Agendamiento(dentista=c3,especialidad=b2,calendario=a3,paciente=yo2)
    final.save()
    y = Oferta_horaria.objects.get(dentista=c3,calendario=a3)
    y.disponible = False
    y.save()
    messages.success(request,'Se reservado exitosamente la hora')
    data = simplejson.dumps(a2)
    return HttpResponse(data, mimetype='application/json')


def borrar_hora(request,id_in):
    if request.user.is_anonymous():
        messages.error(request, 'Por favor ingrese al sistema')   
        return HttpResponseRedirect('/')
    if not request.method == 'POST':
        messages.error(request, 'Error, esta intentando acceder de forma indebida')
        return HttpResponseRedirect('/')
    hora = Agendamiento.objects.get(id=id_in)
    hora.desabilitado = True
    hora.save()
    messages.success(request,'Se ha eliminado el agendamiento correctamente')
    return HttpResponseRedirect('/paciente')

def cancelarhoradelpaciente(request):
    if request.user.is_anonymous():
        messages.error(request, 'Por favor ingrese al sistema')   
        return HttpResponseRedirect('/')
    if not request.method == 'POST':
        messages.error(request, 'Error, esta intentando acceder de forma indebida')
        return HttpResponseRedirect('/')

    form = EliminarBox(request.POST)
    if not form.is_valid():
        messages.error(request, 'Formulario malo, por favor revise los campos')
        return HttpResponseRedirect('/administrador')