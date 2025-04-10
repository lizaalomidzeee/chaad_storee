from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str



User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['id', 'username', 'email', 'phone_number', 'first_name', 'last_name']
        
        
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])




class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    password2= serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'first_name', 'last_name', 'password', 'password2']
  

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "password dont match"})
        return attrs
    

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        return user
    


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("მომხმარებელი მსგავსი email'ით ვერ მოიძებნა")
        return value
    


class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField(write_only=True, required = True, validators = [validate_password])
    password2 = serializers. CharField(write_only=True, required=True)


    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "პაროლები არ ემთხვევა"})
        
        try:
            uid = force_str(urlsafe_base64_decode(attrs['uidb64']))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, KeyError):
            raise serializers.ValidationError({"message": "მომხმარებელი ვერ მოიძებნა"})
        

        token = attrs['token']
        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError({"message": "არასწორი ან ვადაგასული ტოკენია"})
        

        attrs['user']= user
        return attrs
    
    def save(self):
        user = self.validated_data['user']
        user.set_password(self.validated_data['password'])
        user.save()
    
    




             


