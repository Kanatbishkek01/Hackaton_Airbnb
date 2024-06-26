from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('hotel', HotelViewSet)
router.register('like', LikeViewSet)
router.register('comments', CommentViewSet)
router.register('images', HotelImageViewSet)
router.register('category',CategoryViewSet)
router.register('favorites', FavoritesViewSet)

urlpatterns = [
    path('',include(router.urls))
]