from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSeralizer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email','password']

        extra_kwargs = {
            'password':{'write_only':True}
        }
    def create(self,validated_data):
        return get_user_model().objects.create_user(**validated_data)