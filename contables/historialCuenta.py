# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import PeriodoContable,Transaccion,Cuenta,detalleTransaccion,estadoComprobacion,estadoResulta,estadoCapital,balanceGeneral
from myauth.models import  MyUser
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Max,Count,Q
from django.db import connection
from .models import Empleado,planillaGeneral,Pan,MateriaPrima,CIF,Final,Kardex,Entrada,Salida,Orden,materialUtilizado,productoTerminado,empleadosXorden
import datetime
import decimal
from django.db.models import Q

def buscarCuenta(fecha1,fecha2,cuenta1,cuenta2):
    cuentas2=[]
    cuentas = Cuenta.objects.all()
    cuentas2.append(cuentas.filter(Q(codigo__gt=999999999)& Q(codigo__lt=99999999999)).order_by('codigo'))
    #print cuentas2
    nombreCuenta1 = cuentas.get(id=cuenta1)
    nombreCuenta2 = cuentas.get(id=cuenta2)
    #print cuenta1
    #print cuenta2
    cuentasT1=[]
    cuentasT2=[]
    transaccionCuenta = Transaccion.objects.filter(Q(fecha__range=(fecha1,fecha2)))
    #print transaccionCuenta
    for tc in transaccionCuenta:
        #print tc
        dt = detalleTransaccion.objects.filter(id_Transaccion=tc)
        for d in dt:
            #print d.id_cuenta.id
            if int(d.id_cuenta.id) == int(cuenta1):
                cuentasT1.append(d)
            if int(d.id_cuenta.id) == int(cuenta2):
                cuentasT2.append(d)
    #print 'aqui T1: {0} y aqui T2 {1}'.format(cuentasT1,cuentasT2)
    context={'cuenta':cuentas2,'cuentasT1':cuentasT1,'cuentasT2':cuentasT2,'c1':nombreCuenta1.nombre,'c2':nombreCuenta2.nombre}
    return context

def historialCuenta(request):
    cuentas2=[]
    cuentas = Cuenta.objects.filter(Q(codigo__lt=99999)).order_by('codigo')
    #cuentas2.append(Cuenta.objects.filter(Q(codigo__gt=9) & Q(codigo__lt=999)).order_by('codigo'))
    #print 'aqui cuentas:{0}'.format(cuentas)
    if request.method == 'POST':
        fechaI = request.POST['fecha1']
        fechaF = request.POST['fecha2']
        cuenta1 = request.POST['cuentaId1']
        cuenta2 = request.POST['cuentaId2']
        context=buscarCuenta(fechaI,fechaF,cuenta1,cuenta2)
        context['f1']=fechaI
        context['f2']=fechaF
        context['c1Id']=cuenta1
        context['c2Id']=cuenta2
        return render(request,'contables/historialCuenta.html',context)
    context={'cuenta':cuentas}
    return render(request,'contables/historialCuenta.html',context)
