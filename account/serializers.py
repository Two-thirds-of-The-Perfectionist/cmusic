from rest_framework import serializers

from .models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=6, required=True)


    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password_confirm')
    

    def validate(self, attrs):
        pass1 = attrs.get('password')
        pass2 = attrs.pop('password_confirm')

        if pass1 != pass2:
            raise serializers.ValidationError('Password dont match')
        
        return attrs
    

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email already exists')
        
        return email
    

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('User with this username already exists')

        return username
    

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class NewPasswordSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=150, required=True)
    activation_code = serializers.CharField(max_length=8, min_length=8, required=True)
    password = serializers.CharField(min_length=4, required=True)
    password_confirm = serializers.CharField(min_length=4, required=True)


    class Meta:
        model = User
        fields = ('email', 'activation_code', 'password', 'password_confirm')


    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователя с таким email не найден')
        return email


    def validate(self, attrs):
        pass1 = attrs.get('password')
        pass2 = attrs.pop('password_confirm')

        if pass1 != pass2:
            raise serializers.ValidationError("Password don't match")
        
        return attrs
    

    def save(self, **kwargs):
        data = self.validated_data
        email = data.get('email')
        password = data.get('password')
        try:
            user = User.objects.get(email=email)
            if not user:
                raise serializers.ValidationError('Пользователь не найден')
        except User.DoesNotExist:
            raise serializers.ValidationError('Пользователь не найден')
        user.set_password(password)
        user.save()
        return user
