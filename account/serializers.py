from rest_framework import serializers
from django.contrib.auth import get_user_model
from .tasks import send_activation_code_celery
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=6,required=True,write_only=True)

    class Meta:
        model = User
        fields = 'email','password','password_confirm'

    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.pop('password_confirm')

        if p1 != p2:
            raise serializers.ValidationError(
                'Пароли не совпалают!'
            )
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        send_activation_code_celery.delay(user.email,user.activation_code)
        return user
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=6, required=True)
    new_password = serializers.CharField(min_length=6, required=True)
    new_password_confirm = serializers.CharField(min_length=6, required=True)

    def validate_old_password(self, old_pass):
        user = self.context.get('request').user
        if not user.check_password(old_pass):
            raise serializers.ValidationError(
                'Вы ввели некорректный пароль'
            )
        return old_pass

    def validate(self, attrs):
        password = attrs.get('new_password')
        password_confirm = attrs.pop('new_password_confirm')
        old = attrs.get('old_password')
        if old == password:
            raise serializers.ValidationError(
                'Пароли совпадают'
            )
        if password != password_confirm:
            raise serializers.ValidationError(
                'Пароли не совпадают'
            )
        return attrs
    
    def set_new_password(self):
        new_pass = self.validated_data.get('new_password')
        user = self.context.get('request').user
        user.set_password(new_pass)
        user.save()



class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь не найден'
            )
        return email
    
    def gen_new_password(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        new_pass = get_random_string(10)
        user.set_password(new_pass)
        user.save()

        send_mail(
            'Восстановление пароля', 
            f'Ваш новый пароль: {new_pass}',
            'test@gmail.com',
            [user.email]
        )