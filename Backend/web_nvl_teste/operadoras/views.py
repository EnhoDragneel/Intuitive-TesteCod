from django.shortcuts import render
from django.http import JsonResponse
from .models import Operadora
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q



@api_view(['GET'])
def buscar_operadoras(request):
    termo = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))

    operadoras_qs = Operadora.objects.filter(
        Q(razao_social__icontains=termo) |
        Q(nome_fantasia__icontains=termo) |
        Q(cnpj__icontains=termo)
    )

    total = operadoras_qs.count()
    start = (page - 1) * page_size
    end = start + page_size
    operadoras_page = operadoras_qs[start:end]

    data = [{
        'registro_ans': o.registro_ans,
        'razao_social': o.razao_social,
        'nome_fantasia': o.nome_fantasia,
        'cnpj': o.cnpj,
    } for o in operadoras_page]

    return Response({
        'results': data,
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': (total + page_size - 1) // page_size
    })

