from django.db import models


class Draw(models.Model):
    """A Secret Santa draw.

    Store the date the draw was made, and its outcome.
    """
    drawn_on = models.DateTimeField(auto_now_add=True)
