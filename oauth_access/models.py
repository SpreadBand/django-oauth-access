import datetime

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models

class OAuthAssociation(models.Model):
    """
    Associates an entity with an oauth service
    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    associated_object = generic.GenericForeignKey()

    service = models.CharField(max_length=75, db_index=True)
    identifier = models.CharField(max_length=255, db_index=True)
    token = models.CharField(max_length=200)
    expires = models.DateTimeField(null=True)
    
    class Meta:
        unique_together = [("content_type", "object_id", "service")]
    
    def expired(self):
        return self.expires and datetime.datetime.now() < self.expires
