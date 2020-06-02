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
from .controlador import SesionControlador
from .controlador import FormatosControlador
"""from .controlador import menuBasesDatosBibliograficasControlador
from .controlador import menuFormatosControlador
from .controlador import cerrarSesionControlador
from .controlador import registroControlador
from .controlador import añadirBDControlador"""
from .controlador import BaseDatosControlador
from .controlador import descargarInformacionControlador
"""from .controlador import verBaseDatosControlador
from .Modelo import registroModelo
from .Modelo import InicioSesionModelo
from .Modelo import añadirBDModelo
from .Modelo import crearReporteModelo
from .Modelo import agregarBaseDatosModelo
from .Modelo import agregarFormularioModelo
from .Modelo import actualizarBaseDatosModelo
from .Modelo import actualizarFormatoModelo
from .Modelo import descargarInformacionModelo"""
from .controlador import ReporteControlador

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', SesionControlador.signIn),
    url(r'^logout/',SesionControlador.logout,name="log"),
    url(r'^signUp/', SesionControlador.signUp, name='signup'),
    #url(r'^create/', añadirBDControlador.create, name='create'),
    url(r'^createReport/', ReporteControlador.create_report, name='createReport'),
    url(r'^agregarBaseDatos/', BaseDatosControlador.agregarBaseDatos, name='agregarBaseDatos'),
    url(r'^agregarFormato/', FormatosControlador.agregarFormato, name='agregarFormato'),
    url(r'^menuBasesDatos/', BaseDatosControlador.menuBaseDatosBibliograficas, name='menuBasesDatos'),
    url(r'^menuFormatos/', FormatosControlador.menuFormatos, name='menuFormatos'),
    url(r'^verBasesDatos/', BaseDatosControlador.verBaseDatos, name='verBasesDatos'),
    url(r'^verFormatos/', FormatosControlador.verFormatos, name='verFormatos'),
    url(r'^descargarInformacion/', descargarInformacionControlador.descargar, name='descargarInformacion'),
    url(r'^consultaBaseDatos/', BaseDatosControlador.verBaseDatosConsulta, name='consultaBaseDatos'),
    url(r'^consultaFormato/', FormatosControlador.verFormatoConsulta, name='consultaFormato'),
    url(r'^actualizarBDB/', BaseDatosControlador.agregar, name='actualizarBDB'),
    url(r'^eliminarBDB/', BaseDatosControlador.eliminarBaseDatos, name='eliminarBDB'),
    url(r'^confirmarActualizacion/', BaseDatosControlador.actualizar, name='confirmarActualizacion'),
    url(r'^formularioAgregarBaseDatos/', BaseDatosControlador.agregarBaseDatosFormulario, name='formularioAgregarBaseDatos'),
    url(r'^postsign/', SesionControlador.postsign),
    url(r'^postsignup/', SesionControlador.postsignup, name='postsignup'),
    url(r'^formularioAgregarFormato/', FormatosControlador.agregarFormulario, name='formularioAgregarFormato'),
    url(r'^actualizarFormato/', FormatosControlador.agregar, name='actualizarFormato'),
    url(r'^eliminarFormato/', FormatosControlador.eliminarFormato, name='eliminarFormato'),
    url(r'^confirmarActualizacionFormato/', FormatosControlador.actualizar, name='confirmarActualizacionFormato'),
    url(r'^reporteBaseDatosEspecifica/', ReporteControlador.AntesCrearReporte, name='reporteBaseDatosEspecifica'),
    url(r'^postcreateReport/', ReporteControlador.AntesCrearReporte, name='postcreateReport'),
    url(r'^formularioDescargar/', ReporteControlador.verReporte, name='formularioDescargar'),
    url(r'^downloadInformacion/', ReporteControlador.descargar, name='downloadInformacion'),
    url(r'^viewGraphic/', ReporteControlador.vistaGrafica, name='viewGraphic'),
    url(r'^graficosRealizados/', ReporteControlador.generarGrafico, name='graficosRealizados'),
    url(r'^imagenLogo/', SesionControlador.buscarImagen),
    #url(r'^post_create/',añadirBDModelo.post_create,name='pos_create'),






]
