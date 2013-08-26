from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
# from dajaxice.core import dajaxice_autodiscover, dajaxice_config
# dajaxice_autodiscover()

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'odclock.views.index', name='index'),
    url(r'^index$', 'odclock.views.index', name='index'),
    url(r'^sesionpaciente$', 'odclock.views.iniciosesionpaciente', name='iniciosesionpaciente'),
    url(r'^sesionpersonal$', 'odclock.views.iniciosesionpersonal', name='iniciosesionpersonal'),
    url(r'^crear/usuario$', 'odclock.views.crear_usuario'),
    url(r'^modificar/password$', 'odclock.views.cambiarpass'),
    url(r'^modificar/correo$', 'odclock.views.cambiaremail'),
    url(r'^modificar/telefonocelular$', 'odclock.views.cambiartelefonoc'),
    url(r'^modificar/telefonofijo$', 'odclock.views.cambiartelefonof'),
    url(r'^ubicacion$', 'odclock.views.ubicacion', name='ubicacion'),
    url(r'^paciente$', 'odclock.views.paciente', name='paciente'),
    url(r'^odclock$', 'odclock.views.quienessomos', name='quienessomos'),
    url(r'^dentista$', 'odclock.views.dentista', name='dentista'),
    url(r'^secretaria$', 'odclock.views.secretaria', name='secretaria'),
    url(r'^administrador$', 'odclock.views.administrador', name='administrador'),
    url(r'^login$', 'odclock.views.login_view'),
    url(r'^logout$', 'odclock.views.logout_view'),
    url(r'^borrar/hora/(\d+)/$', 'odclock.views.borrar_hora'),
    url(r'^agregardentista$', 'odclock.views.agregardentista'),
    url(r'^agregarsecretaria$', 'odclock.views.agregarsecretaria'),
    url(r'^agregarbox$', 'odclock.views.agregarbox'),
    url(r'^agregarespecialidad$', 'odclock.views.agregarespecialidad'),
    url(r'^eliminardentista$', 'odclock.views.eliminardentista'),
    url(r'^eliminarsecretaria$', 'odclock.views.eliminarsecretaria'),
    url(r'^eliminarbox$', 'odclock.views.eliminarbox'),
    url(r'^eliminarespecialidad$', 'odclock.views.eliminarespecialidad'),
    url(r'^asignarespecialidad$', 'odclock.views.asignarespecialidad'),
    url(r'^desasignarespecialidad$', 'odclock.views.desasignarespecialidad'),
    url(r'^ingresaroferta$', 'odclock.views.ingresaroferta'),
    url(r'^eliminaroferta$', 'odclock.views.eliminaroferta'),
    url(r'^verficha$', 'odclock.views.verficha'),
    url(r'^atencion$', 'odclock.views.atencion'),
    url(r'^nombraradministrador$', 'odclock.views.nombraradministrador'),
    url(r'ajaxespecialidad$','odclock.views.ajaxespecialidad',name='ajaxespecialidad'),
    url(r'ajaxdentista$','odclock.views.ajaxdentista',name='ajaxdentista'),
    url(r'ajaxoferta$','odclock.views.ajaxoferta',name='ajaxoferta'),
    url(r'tomarhora$','odclock.views.tomarhora',name='tomarhora'),
    url(r'dameoferta$','odclock.views.dameoferta',name='dameoferta'),
    # url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'cancelarhoradelpaciente$','odclock.views.cancelarhoradelpaciente'),
    
    url(r'^admin/', include(admin.site.urls)),
)
handler404 = 'odclock.views.index'
handler500 = 'odclock.views.index'
urlpatterns += staticfiles_urlpatterns()
