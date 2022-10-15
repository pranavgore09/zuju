import uuid
from django.db import models


class BaseDateTimeModel(models.Model):
    '''
    This is a abstract base class - No table will be created

    Base DateTime model with two date fields.
    Both fields are populated automatically.

    Each child model class in entire application must use this as a base class
    '''
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseDateTimeUUIDModel(BaseDateTimeModel):
    '''
    This is a abstract base class - No table will be created
    
    Adds UUID to the row. Child of BaseDateTimeModel

    Each child class in entire application must use this as a base class
   
    '''
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True
