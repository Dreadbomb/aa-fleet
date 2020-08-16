from django.db import models
from allianceauth.groupmanagement.models import AuthGroup
from datetime import datetime

class Fleet(models.Model):
    fleet_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=50, default='')
    fleet_commander_id = models.BigIntegerField()
    created_at = models.DateTimeField()
    motd = models.CharField(max_length=4000)
    is_free_move = models.BooleanField()

    groups = models.ManyToManyField(AuthGroup, related_name="restricted_groups", help_text="Group listed here will be able to join the fleet")

    class Meta:                     
        default_permissions = ()
        permissions = ( 
            ('fleet_access', 'Can access this app'),
            ('manage', 'Can Manage Fleets')
        )

class FleetInformation(models.Model):
    fleet = models.ForeignKey(Fleet, on_delete=models.CASCADE)
    ship_type_name = models.CharField(max_length=100)
    count = models.IntegerField()
    date = models.DateTimeField(default=datetime.now)

    class Meta:                     
        default_permissions = ()

    
