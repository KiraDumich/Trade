from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from trade.models import Provider, Network, Product
from trade.permissions import IsActive
from trade.serializers import ProviderSerializers, NetworkSerializers, ProductSerializers


class ProviderViewSet(viewsets.ModelViewSet):
    serializer_class = ProviderSerializers
    queryset = Provider.objects.all()
    filter_backends = [SearchFilter]  # фильтр поиска по полю "страна"
    filterset_fields = ['country']
    permission_classes = [IsActive]

    def update(self, request, *args, **kwargs):
        """Запрет обновления через API поля «Задолженность перед поставщиком»"""
        partial = kwargs.pop('partial', False)  # запрет выполняется через метод частичного обновления
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if 'arrears' in serializer.validated_data:
            serializer.validated_data.pop('arrears')
        self.perform_update(serializer)

        return Response(serializer.data)


class NetworkViewSet(viewsets.ModelViewSet):
    serializer_class = NetworkSerializers
    queryset = Network.objects.all()
    permission_classes = [IsActive]


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializers
    queryset = Product.objects.all()
    permission_classes = [IsActive]
