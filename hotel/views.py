from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from .permissions import IsAuthorPermission,BlockPermissions
from .serializers import *
from .models import *
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

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

    @method_decorator(cache_page(60*2))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ('retrieve','list'):
            self.permission_classes = [IsAuthorPermission,IsAdminUser]
        elif self.action =='destroy':
            self.permission_classes = [IsAuthorPermission]
        else:
            self.permission_classes = [BlockPermissions]
        return super().get_permissions()

class FavoritesViewSet(ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ('retrieve','list'):
            self.permission_classes = [IsAuthorPermission,IsAdminUser]
        elif self.action =='destroy':
            self.permission_classes = [IsAuthorPermission]
        else:
            self.permission_classes = [BlockPermissions]
        return super().get_permissions()
    
class HotelImageViewSet(ModelViewSet):
    queryset = HotelImage.objects.all()
    serializer_class = HotelImageSerializer
    permission_classes = [IsAdminUser]

class CategoryViewSet(PermissionMixin, ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer