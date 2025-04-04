from django.shortcuts import render
from django.http import JsonResponse
from .models import Operadora
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q



@api_view(['GET'])
def buscar_operadoras(request):
    termo = request.GET.get('q', '')
    
    resultados = Operadora.objects.filter(
        Q(razao_social__icontains=termo) |
        Q(nome_fantasia__icontains=termo) |
        Q(cnpj__icontains=termo)
    )[:10]  

    data = [{
        'registro_ans': o.registro_ans,
        'razao_social': o.razao_social,
        'nome_fantasia': o.nome_fantasia,
        'cnpj': o.cnpj,
    } for o in resultados]

    return Response(data)
