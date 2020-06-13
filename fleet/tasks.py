from .providers import esi
from .models import Fleet
from esi.models import Token
from celery import shared_task
from django.utils import timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging


logger = logging.getLogger(__name__)

@shared_task
def open_fleet(character_id, motd, free_move, name, groups):
    required_scopes = ['esi-fleets.read_fleet.v1','esi-fleets.write_fleet.v1']
    c = esi.client
    token = Token.get_token(character_id,required_scopes)
    fleet_result = c.Fleets.get_characters_character_id_fleet(character_id=token.character_id,token=token.valid_access_token()).result()
    fleet_id = fleet_result.pop('fleet_id')
    fleet_role = fleet_result.pop('role')

    if fleet_id == None or fleet_role == None or fleet_role != 'fleet_commander':
        return;

    fleet = Fleet(fleet_id=fleet_id, created_at=timezone.now(), motd=motd, is_free_move=free_move, fleet_commander_id = token.character_id, name=name)
    fleet.save()
    fleet.groups.set(groups)

    esiFleet = {
        'is_free_move': free_move,
        'motd': motd
    }
    c.Fleets.put_fleets_fleet_id(fleet_id=fleet_id, token=token.valid_access_token(), new_settings=esiFleet).result()

@shared_task
def send_fleet_invitation(character_ids, fleet_id):
    required_scopes = ['esi-fleets.write_fleet.v1']
    c = esi.client
    fleet = Fleet.objects.get(fleet_id=fleet_id)
    fleet_commander_token = Token.get_token(fleet.fleet_commander_id,required_scopes)
    _processes = []
    with ThreadPoolExecutor(max_workers=50) as ex:
        for _chracter_id in character_ids:
            _processes.append(ex.submit(send_invitation, character_id=_chracter_id, fleet_commander_token=fleet_commander_token, fleet_id=fleet_id))
    for item in as_completed(_processes):
        _ = item.result()


@shared_task
def send_invitation(character_id, fleet_commander_token, fleet_id):
    c = esi.client
    invitation = {
        'character_id': character_id,
        'role': 'squad_member'
    }
    c.Fleets.post_fleets_fleet_id_members(fleet_id=fleet_id, token=fleet_commander_token.valid_access_token(), invitation=invitation).result()

@shared_task
def check_fleet_adverts():
    required_scopes = ['esi-fleets.read_fleet.v1','esi-fleets.write_fleet.v1']
    c = esi.client
    fleets = Fleet.objects.all()
    for fleet in fleets:
        token = Token.get_token(fleet.fleet_commander_id,required_scopes)
        try:
            fleet_result = c.Fleets.get_characters_character_id_fleet(character_id=token.character_id,token=token.valid_access_token()).result()
            fleet_id = fleet_result['fleet_id']
            if(fleet_id != fleet.fleet_id):
                fleet.delete()
        except Exception as e:
            if(e.status_code == 404): # 404 means the character is not in a fleet
                fleet.delete()
                logger.info("Character is not in a fleet - fleet advert removed")



   