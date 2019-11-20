# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from .models import *
#from .models import PeriodoContable,Transaccion,Cuenta,detalleTransaccion,estadoComprobacion,estadoResulta,estadoCapital,balanceGeneral
from myauth.models import  MyUser
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Max,Count
from django.db import connection
from django.db.models import Q
#from .models import Empleado,planillaGeneral,Pan,MateriaPrima,CIF,Final,Kardex,Entrada,Salida,Orden,materialUtilizado,productoTerminado,empleadosXorden
import datetime
import decimal

def createEstadoIniciales():
    try:
        estadoCNull = estadoComprobacion.objects.get(id=1)
    except estadoComprobacion.DoesNotExist:
        estadoCNull = None
    if estadoCNull==None:
        estadoComprobacion.objects.create(debe=0.00,haber=0.00)

    try:
        estadoRNull = estadoResulta.objects.get(id=1)
    except estadoResulta.DoesNotExist:
        estadoRNull = None
    if estadoRNull==None:
        estadoResulta.objects.create(debe=0.00,haber=0.00,utilidades=0.00,utilidadNeta=0.00)

    try:
        estadoCPNull = estadoCapital.objects.get(id=1)
    except estadoCapital.DoesNotExist:
        estadoCPNull = None
    if estadoCPNull==None:
        estadoCapital.objects.create(debe=0.00,haber=0.00,capitalContable=0.00,UtilidadRetenida=0.00)

    try:
        balanceGNull = balanceGeneral.objects.get(id=1)
    except balanceGeneral.DoesNotExist:
        balanceGNull = None
    if balanceGNull==None:
        balanceGeneral.objects.create(debe=0.00,haber=0.00)

    panes = ['Donas chocolate','Pastel fresa','Budín','Semita de piña']
    try:
        panNull = Pan.objects.get(id=1)
    except Pan.DoesNotExist:
        panNull = None
    if panNull==None:
        for pan in panes:
            Pan.objects.create(descripcion=pan)
    dic=[]
    dic.append(dict(nombre='azucar',cantidad=5,precio=2.50))
    dic.append(dict(nombre='crema',cantidad=5,precio=3.50))
    try:
        mpNull = MateriaPrima.objects.get(id=1)
    except MateriaPrima.DoesNotExist:
        mpNull=None
    if mpNull == None:
        for mprima in dic:
            MateriaPrima.objects.create(nombreMateriaPrima=mprima['nombre'],cantidad=mprima['cantidad'],precioUnitario=mprima['precio'])
            mp = MateriaPrima.objects.filter(nombreMateriaPrima=mprima['nombre']).first();
            Kardex.objects.create(materiaPrima = mp)



@login_required
def index(request):
    	userId=request.user.is_admin
        createEstadoIniciales()
        return render(request, 'contables/index.html', {'user':userId})

@login_required
def nuevoPeriodo(request):
    if request.method == 'POST':
        periodo = PeriodoContable(fechaInicio=request.POST['fechaIni'],fechaFin=request.POST['fechaFin'],estadoPeriodo=True)
        periodo.save()
        print 'aqui esto es: {0}'.format(periodo)
        bal = estadoComprobacion.objects.get(id=1)
        bal.debe=0.00
        bal.haber= 0.00
        bal.save()
        cuenta = Cuenta.objects.all()
        for cuentas in cuenta:
    		cuentaParcial=Cuenta.objects.get(id=cuentas.id)
    		cuentaParcial.saldoAcreedor=0.00
    		cuentaParcial.saldoDeudor=0.00
    		cuentaParcial.debe=0.00
    		cuentaParcial.haber=0.00
    		cuentaParcial.save()
        return HttpResponse('No se almacenaron los datos')
    return render(request, 'contables/nuevoPeriodo.html')

@login_required
def balancesComprobacion(request,periodoId):
	detalles = detalleTransaccion.objects.all()
	transaccion = Transaccion.objects.filter(id_periodoContable=periodoId)
	cuentas=Cuenta.objects.all()
	haberParcial = float(0.00)
	debeParcial = float(0.00)
	sumaHaber=float(0.00)
	sumaDebe=float(0.00)


	for cuenta in cuentas:
		cuentaSet=Cuenta.objects.get(id=cuenta.id)
		cuentaSet.saldoAcreedor=0.00
		cuentaSet.saldoDeudor=0.00
		cuentaSet.save()
		bal=estadoComprobacion.objects.get(id=int(1))
		bal.debe=float(0.00)
		bal.haber=float(0.00)
		bal.save()

	for cuenta in cuentas:
		bal=estadoComprobacion.objects.get(id=int(1))
		cuentaParcial=Cuenta.objects.get(id=cuenta.id)
		for transacciones in transaccion:
			for detalle in detalles:
				if detalle.id_cuenta_id == cuenta.id:
					if detalle.id_Transaccion_id == transacciones.id_Transaccion:
						haberParcial=float(haberParcial) + float(detalle.haber)
						debeParcial=float(debeParcial) + float(detalle.debe)
		if haberParcial > debeParcial:
			cuentaParcial.saldoAcreedor=float(haberParcial)-float(debeParcial)
			cuentaParcial.save()
			bal.haber=float(bal.haber)+float(cuentaParcial.saldoAcreedor)
			bal.save()
		if debeParcial > haberParcial:
			cuentaParcial.saldoDeudor=float(debeParcial)-float(haberParcial)
			cuentaParcial.save()
			bal.debe=float(bal.debe)+float(cuentaParcial.saldoDeudor)
			bal.save()
		if debeParcial == haberParcial:
			cuentaParcial.saldoAcreedor=0.00
			cuentaParcial.saldoDeudor=0.00
			cuentaParcial.save()
			bal.debe=float(bal.debe)+float(cuentaParcial.saldoDeudor)
			bal.haber=float(bal.haber)+float(cuentaParcial.saldoAcreedor)
			bal.save()
		haberParcial=0.00
		debeParcial=0.00

	balanceC= estadoComprobacion.objects.all()
	transaccion = Transaccion.objects.filter(id_periodoContable=periodoId)
	cuentas=Cuenta.objects.all()
	return render(request, 'contables/balanceComprobacion.html',{'cuenta':cuentas,'estados':balanceC,'periodoId':periodoId})
