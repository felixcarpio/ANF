from django.conf.urls import url,include
from django.conf.urls import handler400, handler403, handler404, handler500

from . import views, kardexViews, orderViews,estadosFinancieros,historialCuenta,reportes_pdf
from . import errors

handler404 = errors.mi_error_404
handler500 = errors.handler500

urlpatterns = [
    url(r'^index/$', estadosFinancieros.index),
    url(r'^periodoConta/$', views.periodoConta),
    url(r'^periodoConta/nuevoPeriodo/$',estadosFinancieros.nuevoPeriodo),
    url(r'^catalogo/$',views.catalogoCuenta),
    url(r'^menu/(?P<periodoId>\d+)/$', views.manejoTransaccion),
    url(r'^consulta/(?P<periodoId>\d+)/$', views.consultarTransaccion),
    url(r'^nuevaTrans/(?P<periodoId>\d+)/$', views.nuevaTransaccion),
    url(r'^transaccion/(?P<periodoId>\d+)/$',views.transacciones),
    url(r'^detalleTrans/(?P<periodoId>\d+)/(?P<transaccionId>\d+)/$',views.detallesTransaccion),
    url(r'^detalleAfectado/(?P<periodoId>\d+)/(?P<transaccionId>\d+)/$',views.consultaAfectado),
    url(r'^generador/(?P<periodoId>\d+)/$', views.generadorEstados),
    url(r'^historial/(?P<periodoId>\d+)/$', views.historialCuenta),
    url(r'^balanceComprobacion/(?P<periodoId>\d+)/$', estadosFinancieros.balancesComprobacion),
    url(r'^agregarCuenta/$', views.agregarCuentaPadre),
    url(r'^agregarCuentaHija/(?P<cuentaId>\d+)/$', views.agregarCuentaHija),
    url(r'^modificarCuenta/(?P<cuentaId>\d+)/$', views.modificarCuenta),
    url(r'^contabilidadGeneral/(?P<periodoId>\d+)/$', views.contabilidadGeneral),
    url(r'^estadoResultado/(?P<periodoId>\d+)/$', views.estadosResultado),
    url(r'^estadoCapital/(?P<periodoId>\d+)/$', views.estadoCapita),
    url(r'^balanceGeneral/(?P<periodoId>\d+)/$', views.balanceGral),
    url(r'^contabilidadCostos/(?P<periodoId>\d+)/$', views.contabilidadCost),
    url(r'^compraMP/(?P<periodoId>\d+)/$', views.compraMateriaPrima),
    url(r'^compraMP/(?P<periodoId>\d+)/agregarMp$', views.crearMateriaPrima),
    url(r'^manejoOrdenes/(?P<periodoId>\d+)/$', views.manejoOrden),
    url(r'^contratacion/(?P<periodoId>\d+)/$', views.contratacionEmpleado),
    url(r'^planillaGeneral/(?P<periodoId>\d+)/$', views.planilla),
    url(r'^productoTerminado/(?P<ordenId>\d+)/(?P<periodoId>\d+)/$', views.prodTerminado),
    url(r'^planillaGral/(?P<empleadoId>\d+)/(?P<periodoId>\d+)/$', views.asignarPlanilla),
    url(r'^historialCuenta/$',historialCuenta.historialCuenta),
    url(r'^pdf_cuentas/(?P<f1>[-\w]+)/(?P<f2>[-\w]+)/(?P<c1>\d+)/(?P<c2>\d+)/$', reportes_pdf.envio,name="pdf_hc"),

    #################    kardexViews #######################
    url(r'^kardex/(?P<periodoId>\d+)/$', kardexViews.manejoKardex),
    url(r'^detallesKardex/(?P<materiaId>\d+)/(?P<periodoId>\d+)/$', kardexViews.detalleKardex),
    url(r'^producto/$', kardexViews.catalogoProducto),
    url(r'^producto/crear/$', kardexViews.crearProducto),

    #################   orderViews #########################
    url(r'^crearOrden/(?P<periodoId>\d+)/$', orderViews.crearOrd),
    url(r'^modificarCIF/(?P<periodoId>\d+)/$', orderViews.modificarCif),
    url(r'^gestionarOrden/(?P<ordenId>\d+)/(?P<periodoId>\d+)/$', orderViews.gestionOrden),
    url(r'^asignarMP/(?P<ordenId>\d+)/(?P<periodoId>\d+)/$', orderViews.asignarMP),
    url(r'^asignarMOD/(?P<ordenId>\d+)/(?P<periodoId>\d+)/$', orderViews.asignarMOD),
]
