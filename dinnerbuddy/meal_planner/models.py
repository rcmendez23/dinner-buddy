from django.db import models
# from django.contrib.auth.models import User


# Recipe Request Options
class Options(models.Model):
    DAYS_OF_WEEK = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )

    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    days_of_week = models.JSONField()
    dietary_restrictions = models.JSONField()
    ingredients_include = models.JSONField()
    ingredients_exclude = models.JSONField()
    instant_pot = models.BooleanField()

    # TODO: add some validation?


