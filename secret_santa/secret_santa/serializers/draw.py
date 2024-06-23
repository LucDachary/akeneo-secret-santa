from rest_framework.serializers import ModelSerializer

from secret_santa.models import Draw


class DrawSerializer(ModelSerializer):
    class Meta:
        model = Draw
        fields = "__all__"
