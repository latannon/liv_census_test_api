from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
import json

from django.conf.urls import url

from api.models import CensusLearnSql

from django.db.models import Avg, Count, F
from django.core.paginator import Paginator

from django.http import HttpResponse

DB_NAME = 'census'
MAX_RESULTS = 100

VALUE_RESULT_COL_NAME = 'value'
AVG_AGE_RESULT_COL_NAME = 'age'
COUNT_RESULT_COL_NAME = 'count'
EXCLUDED_VARIABLES = ['id']

# Controller de recuperation des donnees pour une colonnes selectionnees
class CensusSearchResultView(ListAPIView):
    def get(self, request, *args, **kw):
        filterVariable = request.GET.get('variable', None)
        filterMaxResults = request.GET.get('limit_size', MAX_RESULTS)
        kwargs = {
            '{0}__{1}'.format(filterVariable, 'exact'): None
        }
        # TODO utiliser un custom query set
        searchQueryset = CensusLearnSql.objects.using(DB_NAME).values(filterVariable).annotate(value=F(filterVariable), count=Count(filterVariable),avg_age=Avg('age')).order_by('-value').exclude(**kwargs)
        resultPaginator = Paginator(searchQueryset, filterMaxResults)
        results = resultPaginator.page(1).object_list
        # TODO utiliser un serializer ?
        responseToSend = {'total_results_count': resultPaginator.count, 'data' : results}
        response = Response(responseToSend, status=status.HTTP_200_OK)
        return response

# Controller de recuperation dynamique des noms de colonnes de la table
class VariablesView(ListAPIView):
    def get(self, request, *args, **kw):
        allowed_variables = filter(lambda field: field.name not in EXCLUDED_VARIABLES, CensusLearnSql._meta.get_fields())
        # TODO utiliser un serializer ?
        result = map(lambda field:  { 'code': field.name, 'label' : field.db_column if field.db_column else field.name } , allowed_variables)
        response = Response(result, status=status.HTTP_200_OK)
        return response
