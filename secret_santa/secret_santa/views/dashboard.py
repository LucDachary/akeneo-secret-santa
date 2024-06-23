from django.views.generic.list import ListView

from secret_santa.models import Draw


class DashboardView(ListView):
    model = Draw
    queryset = Draw.objects.order_by("-drawn_on").all()[:5]
