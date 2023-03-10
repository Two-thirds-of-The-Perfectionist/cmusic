from rest_framework import serializers

from .models import User, Subscription


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


class NewPasswordSerializer(serializers.Serializer):
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


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'
    

    def validate(self, attrs):
        user = attrs.get('user')
        subs = attrs.get('subscribe')

        if Subscription.objects.filter(user=user, subscribe=subs).exists():
            Subscription.objects.filter(user=user, subscribe=subs).delete()
        else:
            Subscription.objects.create(user=user, subscribe=subs)
        
        return attrs


class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('user_id',)


class SubscriberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('subscribe_id',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'is_staff')


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        
        rep['rating'] = instance.rating
        rep['subscribers'] = SubscriberSerializer(instance.subscribers.all(), many=True).data
        rep['subscriptions'] = SubscribeSerializer(instance.subscriptions.all(), many=True).data

        return rep
