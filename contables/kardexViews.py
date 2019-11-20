# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import *
from myauth.models import  MyUser
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Max,Count
from django.db import connection
from .scriptCuentas import cargarCatalogoCuentas
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
def catalogoProducto(request):
	cargarCatalogoCuentas()
	p = Pan.objects.all()
	return render(request, 'contables/productos/catalogoProducto.html',{'productos':p})
	
@login_required
def crearProducto(request):
	if request.method == 'POST':
		Pan.objects.create(descripcion = request.POST['descripcion'])
		return redirect('/producto/')
	return render(request, 'contables/productos/crearProducto.html')

@login_required
def manejoKardex(request,periodoId):
	mp = MateriaPrima.objects.all()
	return render(request, 'contables/kardex.html',{'periodoId':periodoId,'materia':mp})

@login_required
def detalleKardex(request,materiaId,periodoId):
	mp=MateriaPrima.objects.filter(id=materiaId).first()
	kdx = Kardex.objects.get(materiaPrima = mp)
	fin=Final.objects.filter(kardex=kdx)
	entry=Entrada.objects.filter(kardex=kdx)
	out=Salida.objects.filter(kardex=kdx)

	return render(request, 'contables/detalleKardex.html',{'periodoId':periodoId,'materia':mp,'final':fin,'entrada':entry,'salida':out})