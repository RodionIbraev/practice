from rest_framework import serializers
from .models import User, Account


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "phone_number", "password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class CreatePaymentSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    value = serializers.DecimalField(10, 2)
    return_url = serializers.CharField()


# class AccountSerializer(serializers.ModelSerializer):
#     user_uuid = serializers.UUIDField()
#
#     class Meta:
#         model = Account
#         fields = ('user_uuid',)
