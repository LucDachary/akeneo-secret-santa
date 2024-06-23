from django.db import models
from django.conf import settings

from secret_santa.models import Draw


class Pair(models.Model):
    """A Secret Santa pair of participants.

    One participant is expected to make a gift to the second.
    """
    # models.PROTECT to prevent non-empty Draw deletion.
    draw = models.ForeignKey(Draw, on_delete=models.PROTECT)
    donor = models.CharField(max_length=settings.PARTICIPANT_NAME_MAX_LENGTH)
    beneficiary = models.CharField(max_length=settings.PARTICIPANT_NAME_MAX_LENGTH)
