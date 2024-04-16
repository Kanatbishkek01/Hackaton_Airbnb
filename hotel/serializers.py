from .models import *
from rest_framework.serializers import ModelSerializer,ReadOnlyField

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class HotelSerializer(ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['images'] = HotelImageSerializer(instance.images.all(),many=True).data
        return repr
    
class HotelListSerializer(ModelSerializer):
    class Meta:
        model = Hotel
        fields = ('title','image','price','allowed_dates')

class HotelImageSerializer(ModelSerializer):
    class Meta:
        model = HotelImage
        fields = '__all__'

class LikeSerializer(ModelSerializer):
    author = ReadOnlyField(source = 'author.email')
    class Meta:
        model = Like
        fields = '__all__'
    
    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['author'] = user
        return super().create(validated_data)
    
class CommentSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.name')
    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['author'] = user
        return super().create(validated_data)
    
    def to_representation(self, instance):
        repr =  super().to_representation(instance)
        repr['likes'] = instance.likes.count()
        return repr