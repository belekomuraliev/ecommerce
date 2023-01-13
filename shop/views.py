from rest_framework import viewsets
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .serializers import CategorySerializer, ItemSerializer, OrderSerializer
from .models import Item, Category, Order
from .permissions import IsSenderPermission, IsOwnerPermission, IsBayerPermission


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API для создание категории товаров
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsSenderPermission, ]


class ItemListCreateAPIView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsSenderPermission, ]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['name', 'price']
    ordering_fields = ['name', 'price']

    def get_queryset(self):
        return super().get_queryset().filter(category_id=self.kwargs.get('category_id'))

    def perform_create(self, serializer):
        serializer.save(
            category_id=self.kwargs.get('category_id'),
            profile=self.request.user.profile
        )


class ItemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsOwnerPermission, ]
    permission_classes = [IsOwnerPermission]

    def get_queryset(self):
        return super().get_queryset().filter(category_id=self.kwargs.get('category_id'))


class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsBayerPermission, ]

    def get_queryset(self):
        return super().get_queryset().filter(item=self.kwargs.get('item_id'))

    def perform_create(self, serializer):
        serializer.save(
            profile=self.request.user.profile,
            item_id=self.kwargs.get('item_id'),
        )


class OrderRetrieveDestroyUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerPermission, ]
    #swagger_schema = None

    def get_queryset(self):
        return super().get_queryset().filter(item=self.kwargs.get('item_id'))
