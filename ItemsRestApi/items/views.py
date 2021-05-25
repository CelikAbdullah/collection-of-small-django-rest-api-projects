from items.models import Item
from items.serializers import ItemSerializer
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination


class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = PageNumberPagination
    search_fields = ['name']


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
