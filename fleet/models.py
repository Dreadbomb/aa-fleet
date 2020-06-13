from django.db import models


# Create your models here.

class Fleet(models.Model):
    fleet_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=50, default='')
    fleet_commander_id = models.BigIntegerField()
    created_at = models.DateTimeField()
    motd = models.CharField(max_length=4000)
    is_free_move = models.BooleanField()

    class Meta:                     
        default_permissions = ()
        permissions = ( 
            ('fleet_access', 'Can access this app'),
            ('manage', 'Can Manage Fleets')
        )