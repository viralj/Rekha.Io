from django.db import models


class Tag(models.Model):
    """
    Tag common model to attach tags in questions, tutorials etc
    """
    name = models.CharField(max_length=254, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
