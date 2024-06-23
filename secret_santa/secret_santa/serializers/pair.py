from rest_framework.serializers import ModelSerializer

from secret_santa.models import Pair


class PairSerializer(ModelSerializer):
    class Meta:
        model = Pair
        fields = "__all__"
