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
####################  MOVIMIENTO DE CODIGO ############# CODIGO: C2 #################################


@login_required
def manejoKardex(request,periodoId):
	mp = MateriaPrima.objects.all()
	return render(request, 'contables/kardex.html',{'periodoId':periodoId,'materia':mp})

@login_required
def detalleKardex(request,materiaId,periodoId):
	fin=Final.objects.filter(kardex_id=materiaId)
	entry=Entrada.objects.filter(kardex_id=materiaId)
	out=Salida.objects.filter(kardex_id=materiaId)
	mp=MateriaPrima.objects.get(id=materiaId)
	return render(request, 'contables/detalleKardex.html',{'periodoId':periodoId,'materia':mp,'final':fin,'entrada':entry,'salida':out})