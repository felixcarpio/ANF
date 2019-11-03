from __future__ import unicode_literals
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render
from django.views.generic import View
from . import historialCuenta

from xhtml2pdf import pisa

def render_pdf(url_template,contexto=None):
    contexto2=historialCuenta.buscarCuenta(contexto['fecha1'],contexto['fecha2'],contexto['cuenta1'],contexto['cuenta2'])
    template = get_template(url_template)
    contexto2['f1']=contexto['fecha1']
    contexto2['f2']=contexto['fecha2']
    html = template.render(contexto2)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type="application/pdf")
    return None


def envio(request,f1=None,f2=None,c1=None,c2=None):
    context ={'fecha1':f1,'fecha2':f2,'cuenta1':c1,'cuenta2':c2}
    url_template="contables/pdf/comparacion_cuentas.html"
    pdf=render_pdf(url_template,context)
    return HttpResponse(pdf,content_type="application/pdf")

# class PDFPrueba(View):
#     def get(self,request,*args,**kwargs):
#         pdf=render_pdf("contables/pdf/comparacion_cuentas.html")
#         return HttpResponse(pdf,content_type="application/pdf")
