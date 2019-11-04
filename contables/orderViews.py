# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import PeriodoContable,Transaccion,Cuenta,detalleTransaccion,estadoComprobacion,estadoResulta,estadoCapital,balanceGeneral
from myauth.models import  MyUser
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Max,Count
from django.db import connection
from .models import Empleado,planillaGeneral,Pan,MateriaPrima,CIF,Final,Kardex,Entrada,Salida,Orden,materialUtilizado,productoTerminado,empleadosXorden
import datetime
import decimal
# Create your views here.
# @login_required
# def index(request):
# 	userId=request.user.is_admin
# 	return render(request, 'contables/index.html', {'user':userId})


#####################################################################################################
####################  MOVIMIENTO DE CODIGO ############# CODIGO: C1 #################################

@login_required
def crearOrd(request,periodoId):
	x=Pan.objects.all()
	cif=CIF.objects.all()
	if request.method=='POST':
		Orden.objects.create(
			pan=Pan.objects.get(id=request.POST['productoId']),
			cif=CIF.objects.get(porcentaje=request.POST['cif']),
			descripcion=request.POST['descripcion'],
			diasTrabajados=request.POST['diasTrabajados'],
			cantEmpleados=0,
			terminado=False,
			fechaEntrega=request.POST['fechaEntrega'],
			fechaCreacion=request.POST.get('fechaCreacio'),
			CMOD=0.0,
			CIF_O=0.0,
			CMP=0.0
			)


	return render(request, 'contables/crearOrden.html',{'periodoId':periodoId,'tipoPan':x,'cif':cif})

@login_required
def modificarCif(request, periodoId):
	if request.method == 'POST':
		cif = CIF.objects.get(id=1)
		cif.porcentaje=request.POST['cif']
		cif.save()
	return render(request, 'contables/cif.html',{'periodoId':periodoId})

@login_required
def gestionOrden(request,ordenId,periodoId):
	orden= Orden.objects.filter(id=ordenId)
	return render(request, 'contables/gestionarOrden.html',{'orden':orden,'ordenId':ordenId,'periodoId':periodoId})

@login_required
def asignarMP(request,ordenId,periodoId):

	mp=MateriaPrima.objects.all()

	if request.method == 'POST':
		final=Final.objects.filter(kardex_id=request.POST.get('productoId'),es_Actual=True)
		tamano=len(final)
		print(tamano)
		if tamano != 0:
			cantidadAux=int(0)
			costoUnitario=float(0.00)
			costoTotal=float(0.00)
			if tamano != 0:
				final=Final.objects.get(kardex_id=request.POST['productoId'],es_Actual=True)
				cantidadAux=int(final.cantidadFinal)
				costoUnitario=float(final.costoUnitarioFinal)
				costoTotal=float(cantidadAux)*float(costoUnitario)
				final.es_Actual=False
				final.save()
			Salida.objects.create(
				kardex=Kardex.objects.get(materiaPrima=request.POST['productoId']),
				fechaSalida= request.POST['fechaSalida'],
				costoUnitarioSalida= (float(costoUnitario)),
				cantidadSalida= request.POST['cantidadMP'],
				costoTotalSalida= (float(costoUnitario))*float(request.POST['cantidadMP'])
			)

			Final.objects.create(

				kardex=Kardex.objects.get(materiaPrima=request.POST['productoId']),
				fechaFinal= request.POST['fechaSalida'],
				costoUnitarioFinal= (float(costoUnitario)),
				cantidadFinal=int(cantidadAux)-int(request.POST['cantidadMP']),
				costoTotalFinal= (int(cantidadAux)-int(request.POST['cantidadMP']))*float(costoUnitario),
				es_Actual=True
				)
			materialUtilizado.objects.create(
				orden=Orden.objects.get(id=ordenId),
				materiaPrima=MateriaPrima.objects.get(id=request.POST['productoId'])
				)

			orde=Orden.objects.get(id=ordenId)
			orde.CMP=float(orde.CMP)+((float(costoUnitario))*float(request.POST['cantidadMP']))
			orde.save()

	return render(request, 'contables/asignarMP.html',{'ordenId':ordenId,'product':mp,'periodoId':periodoId})

@login_required
def asignarMOD(request,ordenId,periodoId):
	emp=Empleado.objects.filter(puesto="Panadero")
	empleados= empleadosXorden.objects.filter(orden_id=ordenId)
	if request.method=='POST':
		orde=Orden.objects.get(id=ordenId)
		orde.cantEmpleados=int(orde.cantEmpleados)+int(1)
		orde.save()

		empleadosXorden.objects.create(
			orden= Orden.objects.get(id=request.POST['idOrden']),
			dui= Empleado.objects.get(dui=request.POST['empleadoId'])
			)
	empleados= empleadosXorden.objects.filter(orden_id=ordenId)

	return render(request, 'contables/asignarMOD.html',{'ordenId':ordenId,'empleado':emp,'empx':empleados,'periodoId':periodoId})