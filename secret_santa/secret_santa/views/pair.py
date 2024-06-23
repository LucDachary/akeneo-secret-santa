from rest_framework import viewsets

from secret_santa import models, serializers


class PairViewSet(viewsets.ReadOnlyModelViewSet):
    """REST API for the Pair model.

    Lists are sorted alphabetically on donor names.
    """
    queryset = models.Pair.objects.order_by("donor").all()
    serializer_class = serializers.PairSerializer
