from rest_framework import viewsets

from secret_santa import models, serializers


class DrawViewSet(viewsets.ReadOnlyModelViewSet):
    """REST API for the Draw model.

    The draws are sorted, the most recent first.
    """
    queryset = models.Draw.objects.order_by("-drawn_on").all()
    serializer_class = serializers.DrawSerializer
