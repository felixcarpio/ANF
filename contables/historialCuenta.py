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

def buscarCuenta(fecha1,fecha2,cuenta1,cuenta2):
    cuentas = Cuenta.objects.all()
    nombreCuenta1 = cuentas.get(id=cuenta1)
    nombreCuenta2 = cuentas.get(id=cuenta2)
    print cuenta1
    print cuenta2
    cuentasT1=[]
    cuentasT2=[]
    transaccionCuenta = Transaccion.objects.filter(Q(fecha__range=(fecha1,fecha2)))
    print transaccionCuenta
    for tc in transaccionCuenta:
        print tc
        dt = detalleTransaccion.objects.filter(id_Transaccion=tc)
        for d in dt:
            print d.id_cuenta.id
            if int(d.id_cuenta.id) == int(cuenta1):
                cuentasT1.append(d)
            if int(d.id_cuenta.id) == int(cuenta2):
                cuentasT2.append(d)
    print 'aqui T1: {0} y aqui T2 {1}'.format(cuentasT1,cuentasT2)
    context={'cuenta':cuentas,'cuentasT1':cuentasT1,'cuentasT2':cuentasT2,'c1':nombreCuenta1.nombre,'c2':nombreCuenta2.nombre}
    return context

def historialCuenta(request):
    cuentas = Cuenta.objects.all()
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
