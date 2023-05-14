from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from micro_shared_lib.authentication.permissions import IsAdmin


from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    pagination_class = None
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action == "destroy":
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]
