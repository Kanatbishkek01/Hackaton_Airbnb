from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
# from .permissions import IsAuthorPermission,BlockPermission
from .serializers import *
from .models import *

class PermissionMixin:
    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            permissions = [AllowAny]
        else:
            permissions = [IsAdminUser]
        return [permission() for permission in permissions]



class HotelViewSet(PermissionMixin, ModelViewSet):
    queryset = Hotel.objects.all().order_by('slug')
    serializer_class = HotelSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_fileds = ['category','price']
    search_fields = ['title','price', 'allowed_dates']

    def get_serializer_class(self):
        if self.action == 'list':
            return HotelListSerializer
        return self.serializer_class
    


class CommentViewSet(PermissionMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    
class HotelImageViewSet(ModelViewSet):
    queryset = HotelImage.objects.all()
    serializer_class = HotelImageSerializer
    permission_classes = [IsAdminUser]

class CategoryViewSet(PermissionMixin, ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer