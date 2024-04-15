from django.db import models
from slugify import slugify
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    title = models.CharField(max_length=30,unique=True)
    slug = models.SlugField(max_length=30,primary_key=True,blank=True)
    
    def __str__(self) -> str:
        return self.title
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()

class Hotel(models.Model):
    title = models.CharField(max_length=30,unique=True)
    slug = models.SlugField(max_length=30,primary_key=True,blank=True)
    image = models.ImageField(upload_to='media/')
    price = models.DecimalField(max_digits=10,decimal_places=2)
    rating = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)],default=3)
    allowed_dates = models.CharField(max_length=30)
    desc = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='hotels')
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.title
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        try: 
            self.full_clean()
        except:
            raise ValidationError('Ошибка валидации! Проверьте введенные данные')
        super().save()

class HotelImage(models.Model):
    image = models.ImageField(upload_to='media/')
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE,related_name='images')

    def __str__(self) -> str:
        return f'{self.image} -> {self.hotel.slug}'
    
class Comment(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE,related_name='comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.body
    
class Like(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='likes')
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE,related_name='likes')
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name='likes',blank=True,null=True)

    def __str__(self) -> str:
        return f'liked by {self.author.name}'