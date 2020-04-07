"""lidacoa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from .controlador import InicioSesionControlador
from .controlador import menuBasesDatosBibliograficasControlador
from .controlador import menuFormatosControlador
from .controlador import cerrarSesionControlador
from .controlador import registroControlador
from .controlador import añadirBDControlador
from .controlador import agregarBaseDatosControlador
from .controlador import descargarInformacionControlador
from .controlador import verBaseDatosControlador
from .Modelo import registroModelo
from .Modelo import InicioSesionModelo
from .Modelo import añadirBDModelo
from .Modelo import crearReporteModelo
from .Modelo import agregarBaseDatosModelo
from .Modelo import agregarFormularioModelo
from .Modelo import actualizarBaseDatosModelo
from .Modelo import actualizarFormatoModelo
from .Modelo import descargarInformacionModelo
from .controlador import crearRegistroBDControlador

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', InicioSesionControlador.signIn),
    url(r'^postsign/',InicioSesionModelo.postsign),
    url(r'^logout/',cerrarSesionControlador.logout,name="log"),
    url(r'^signUp/',registroControlador.signUp,name='signup'),
    url(r'^postsignup/',registroModelo.postsignup,name='postsignup'),
    url(r'^create/',añadirBDControlador.create,name='create'),
    url(r'^post_create/',añadirBDModelo.post_create,name='pos_create'),
    url(r'^createReport/', crearRegistroBDControlador.create_report, name='createReport'),
    url(r'^postcreateReport/', crearReporteModelo.create_report, name='postcreateReport'),
    url(r'^agregarBaseDatos/', agregarBaseDatosControlador.agregarBaseDatos, name='agregarBaseDatos'),
    url(r'^agregarFormato/', menuFormatosControlador.agregarFormato, name='agregarFormato'),
    url(r'^formularioAgregarBaseDatos/', agregarBaseDatosModelo.agregarBaseDatos, name='formularioAgregarBaseDatos'),
    url(r'^formularioAgregarFormato/', agregarFormularioModelo.agregarFormulario, name='formularioAgregarFormato'),
    url(r'^menuBasesDatos/', menuBasesDatosBibliograficasControlador.menuBaseDatosBibliograficas, name='menuBasesDatos'),
    url(r'^menuFormatos/', menuFormatosControlador.menuFormatos, name='menuFormatos'),
    url(r'^verBasesDatos/', verBaseDatosControlador.verBaseDatos, name='verBasesDatos'),
    url(r'^verFormatos/', menuFormatosControlador.verFormatos, name='verFormatos'),
    url(r'^confirmarActualizacion/', actualizarBaseDatosModelo.actualizar, name='confirmarActualizacion'),
    url(r'^confirmarActualizacionFormato/', actualizarFormatoModelo.actualizar, name='confirmarActualizacionFormato'),
    url(r'^descargarInformacion/', descargarInformacionControlador.descargar, name='descargarInformacion'),
    url(r'^formularioDescargar/', descargarInformacionModelo.verReporte, name='formularioDescargar'),
    url(r'^actualizarBDB/', actualizarBaseDatosModelo.agregar, name='actualizarBDB'),
    url(r'^eliminarBDB/', actualizarBaseDatosModelo.eliminarBaseDatos, name='eliminarBDB'),
    url(r'^actualizarFormato/', actualizarFormatoModelo.agregar, name='actualizarFormato'),
    url(r'^eliminarFormato/', actualizarFormatoModelo.eliminarFormato, name='eliminarFormato'),

]
