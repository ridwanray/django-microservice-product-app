from rest_framework import viewsets

from .models import Product
from .serializers import ProductSerializer


class   ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    pagination_class = None
    http_method_names = ["get","post","put","delete"]
    serializer_class = ProductSerializer