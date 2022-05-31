from django.conf import settings
from django.db import models


class Project(models.Model):
    """ Project Information """

    PROJECT_TYPE = [
        ("back-end", "Back-End"),
        ("front-end", "Front-End"),
        ("ios", "iOS"),
        ("android", "Android")
    ]

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Creation date")
    date_updated = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=128, verbose_name="Title")
    description = models.CharField(max_length=2048, verbose_name="Description")
    type = models.CharField(max_length=15, choices=PROJECT_TYPE, verbose_name="Type")
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE,
                                       related_name='projects',
                                       verbose_name="Project author",
                                       null=True)
