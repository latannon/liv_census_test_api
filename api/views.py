from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
import json

from django.conf.urls import url

from api.models import CensusLearnSql
# from api.serializer import *

from django.db.models import Avg, Count, F
from django.core.paginator import Paginator

from django.http import HttpResponse

DB_NAME = 'census'
MAX_RESULTS = 100

VALUE_RESULT_COL_NAME = 'value'
AVG_AGE_RESULT_COL_NAME = 'age'
COUNT_RESULT_COL_NAME = 'count'
EXCLUDED_VARIABLES = ['id']


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CensusSearchResultResponse:
    def __init__(self, total_rows_number, data):
        self.total_rows = total_rows_number
        # self.data = data

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class CensusSearchResultView(ListAPIView):
    pagination_class = StandardResultsSetPagination
    """queryset = CensusLearnSql.objects.using('census').values('education').annotate(count=Count('education'),avg_age=Avg('age')).order_by('-count').exclude(education__exact = None)
    serializer_class = CensusSearchResultSerializer"""
    def get(self, request, *args, **kw):
        filterVariable = request.GET.get('variable', None)
        filterMaxResults = request.GET.get('limit_size', MAX_RESULTS)
        kwargs = {
            '{0}__{1}'.format(filterVariable, 'exact'): None
        }
        searchQueryset = CensusLearnSql.objects.using(DB_NAME).values(filterVariable).annotate(value=F(filterVariable), count=Count(filterVariable),avg_age=Avg('age')).order_by('-value').exclude(**kwargs)
        resultPaginator = Paginator(searchQueryset, filterMaxResults)
        results = resultPaginator.page(1).object_list
        responseToSend = {'total_results_count': resultPaginator.count, 'data' : results} # CensusSearchResultResponse(resultPaginator.count, results)
        response = Response(responseToSend, status=status.HTTP_200_OK)
        return response


class VariablesView(ListAPIView):
    def get(self, request, *args, **kw):
        allowed_variables = filter(lambda field: field.name not in EXCLUDED_VARIABLES, CensusLearnSql._meta.get_fields())
        result = map(lambda field:  { 'code': field.name, 'label' : field.db_column if field.db_column else field.name } , allowed_variables) # ['education','age','class_of_worker']
        response = Response(result, status=status.HTTP_200_OK)
        return response
