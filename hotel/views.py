# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework.decorators import action
# from rest_framework.filters import SearchFilter
# from .permissions import IsAuthorPermission,BlockPermission
from .serializers import *
from .models import *


# Create your views here.

class HotelViewSet(ModelViewSet):
    queryset = Hotel.objects.all().order_by('slug')
    serializer_class = HotelSerializer
    # filter_backends = [DjangoFilterBackend,SearchFilter]
    # filterset_fileds = ['title','price']
    # search_fields = ['title','price']

    def get_serializer_class(self):
        if self.action == 'list':
            return HotelListSerializer
        return self.serializer_class
    
    def get_permissions(self):
        return super().get_permissions()

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        return super().get_permissions()
    
class HotelImageViewSet(ModelViewSet):
    queryset = HotelImage.objects.all()
    serializer_class = HotelImageSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer