# -*- encoding: utf-8 -*-
from django.db import models

from django.contrib.auth.models import User

class Paciente(models.Model):
    user = models.OneToOneField(User,primary_key=True)
    nombres = models.CharField(max_length=100)
    apellido_p = models.CharField(max_length=100)
    apellido_m = models.CharField(max_length=100)
    telefono_c = models.CharField(max_length=100)
    telefono_f = models.CharField(max_length=100)
    administrador = models.BooleanField()
    ficha = models.TextField()
    prevision = models.CharField(max_length=100)
    contrasena = models.CharField(max_length=100)
    desabilitado = models.BooleanField()

    def __unicode__(self):
        return self.nombres


class Dentista(models.Model):
    user = models.OneToOneField(User,primary_key=True)
    nombres = models.CharField(max_length=100)
    apellido_p = models.CharField(max_length=100)
    apellido_m = models.CharField(max_length=100)
    telefono_c = models.CharField(max_length=100)
    run_colegio = models.CharField(max_length=100)
    telefono_c = models.CharField(max_length=100)
    telefono_f = models.CharField(max_length=100)
    administrador = models.BooleanField()
    contrasena = models.CharField(max_length=100)
    desabilitado = models.BooleanField()
    entregohorario=models.BooleanField()
    def __unicode__(self):
        return self.nombres


class Secretaria(models.Model):
    user = models.OneToOneField(User,primary_key=True)
    nombres = models.CharField(max_length=100)
    apellido_p = models.CharField(max_length=100)
    apellido_m = models.CharField(max_length=100)    
    telefono_c = models.CharField(max_length=100)
    telefono_f = models.CharField(max_length=100)
    administrador = models.BooleanField()
    contrasena = models.CharField(max_length=100)
    desabilitado = models.BooleanField()
    def __unicode__(self):
        return self.nombres


class Box(models.Model):
    desabilitado = models.BooleanField()
    nombre = models.CharField(max_length=100)
    def __unicode__(self):
        return self.nombre


class Calendario(models.Model):
    dia=models.CharField(max_length=100)
    mes=models.CharField(max_length=100)
    ano=models.CharField(max_length=100)
    feriado = models.BooleanField()
    Bloque_horario = models.IntegerField(max_length=32)

class Prestacion(models.Model):
    nombre = models.CharField(max_length=100)
    detalles = models.TextField()
    desabilitado = models.BooleanField()

class Especialidad(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad_b = models.IntegerField(max_length=100)
    desabilitado = models.BooleanField()
    def __unicode__(self):
        return self.nombre

class Plan_tratamiento(models.Model):
    especialidad=models.ForeignKey(Especialidad)
    nombre = models.CharField(max_length=100)
    sesiones = models.IntegerField(max_length=100)
    bloques = models.IntegerField(max_length=100)
    detalles = models.TextField()
    desabilitado = models.BooleanField()
    def __unicode__(self):
        return self.nombre

class Atencion(models.Model):
    tipo = models.IntegerField(max_length=100)
    dentista=models.ForeignKey(Dentista)
    plan_tratamiento= models.ForeignKey(Plan_tratamiento)
    box = models.ForeignKey(Box)
    paciente= models.ForeignKey(Paciente)
    fecha = models.DateTimeField()
    detalles = models.TextField()

class Derivacion(models.Model):
    paciente = models.ForeignKey(Paciente)
    especialidad= models.ForeignKey(Especialidad)
    atencion = models.ForeignKey(Atencion)
    justificacion = models.TextField()
    desabilitado = models.BooleanField()

class Oferta_horaria(models.Model):
    disponible = models.BooleanField()
    dentista = models.ForeignKey(Dentista)
    calendario = models.ForeignKey(Calendario)

class Dentista_especialidad(models.Model):
    dentista=models.ForeignKey(Dentista)
    especialidad=models.ForeignKey(Especialidad)


class Especialidad_Box(models.Model):
    especialidad=models.ForeignKey(Especialidad)
    box = models.ForeignKey(Box)

class Plan_prestacion(models.Model):
    plan_tratamiento = models.ForeignKey(Plan_tratamiento)
    prestacion = models.ForeignKey(Prestacion)

class Prestacion_atencion(models.Model):
    prestacion= models.ForeignKey(Prestacion)
    atencion = models.ForeignKey(Atencion)
    
class Agendamiento(models.Model):                  
    especialidad = models.ForeignKey(Especialidad)
    dentista = models.ForeignKey(Dentista)
    calendario = models.ForeignKey(Calendario)
    paciente = models.ForeignKey(Paciente)
    desabilitado = models.BooleanField()

class Auditoria(models.Model):
    momento = models.DateTimeField()
    accion = models.CharField(max_length=100)
    usuario = models.CharField(max_length=100)
    tabla = models.CharField(max_length=100)

class Calendario_box(models.Model):
    ocupado = models.BooleanField()
    box=models.ForeignKey(Box)
    calendario=models.ForeignKey(Calendario)