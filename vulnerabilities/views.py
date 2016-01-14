from django.shortcuts import render
from rest_framework import viewsets, mixins, filters
from rest_framework import pagination
import django_filters
from vulnerabilities.serializers import *
from vulnerabilities.models import Vulnerability
from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery

class VulnerabilityCursorPagination(pagination.CursorPagination):
    page_size_query_param = 'page_size'
    page_size = 25
    ordering = '-released_on'

class VulnerabilitySearch(filters.SearchFilter):
    def filter_queryset(self, request, queryset, view):
        #ElasticSearch
        if request.query_params.get('search'):
            aux = SearchQuerySet().models(Vulnerability).filter(content=request.query_params.get('search'))
            #TOFIX
            obj_ids = aux.values_list('pk', flat=True)[:100]
            queryset = Vulnerability.objects.filter(id__in=obj_ids)

        return queryset

class VulnerabilityViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                            mixins.RetrieveModelMixin):
    lookup_field = 'cve'
    paginate_by = 10
    serializer_class = VulnerabilitySerializer
    pagination_class = VulnerabilityCursorPagination
    # filter_backends = (VulnerabilitySearch,)

    def get_queryset(self):
        queryset = Vulnerability.objects.all()

        product = self.request.QUERY_PARAMS.get('product', None)
        if product is not None:
            queryset = queryset.filter(product__name__iexact=product)

        vendor = self.request.QUERY_PARAMS.get('vendor', None)
        if vendor is not None:
            queryset = queryset.filter(product__vendor__iexact=vendor)

        version = self.request.QUERY_PARAMS.get('version', None)
        if version is not None:
            queryset = queryset.filter(product__version__istartswith=version)

        cpe = self.request.QUERY_PARAMS.get('cpe', None)
        if cpe is not None:
            cpe = queryset.filter(product__version__iexact=cpe)

        return queryset