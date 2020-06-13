from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required
from .tasks import open_fleet, send_fleet_invitation
from .models import Fleet
from esi.decorators import token_required
from allianceauth.eveonline.models import EveCharacter
from allianceauth.groupmanagement.models import AuthGroup



@login_required()
@permission_required('fleet.fleet_access')
def dashboard(request):
    groups = request.user.groups.all()
    fleets = Fleet.objects\
        .filter(Q(groups__group__in=groups) | Q(groups=None))\
        .all()
    context = {
        'fleets': fleets
    }
    return render(request, 'fleet/dashboard.html', context)

@login_required()
@permission_required('fleet.manage')
@token_required(scopes=('esi-fleets.read_fleet.v1','esi-fleets.write_fleet.v1',))
def create_fleet(request, token):
    if request.method == 'POST':
        auth_groups = AuthGroup.objects.all()
        ctx = {
            'character_id': token.character_id,
            'auth_groups': auth_groups
        }
        return render(request, 'fleet/create_fleet.html', context=ctx)
    return redirect("fleet:dashboard")

@login_required()
@permission_required('fleet.fleet_access')
def join_fleet(request, fleet_id):
    ctx = {}
    groups = request.user.groups.all()
    fleet = Fleet.objects\
        .filter(groups__group__in=groups, fleet_id=fleet_id)\
        .count()

    if fleet == 0:
        return redirect("fleet:dashboard")

    if request.method == 'POST':
        character_ids = request.POST.getlist('character_ids', [])
        send_fleet_invitation.delay(character_ids, fleet_id)
        return redirect("fleet:dashboard")
    else:
        characters = EveCharacter.objects\
        .filter(character_ownership__user=request.user)\
        .select_related()\
        .order_by('character_name')
        ctx['characters'] = characters      
    return render(request, 'fleet/join_fleet.html', context=ctx)


@login_required()
@permission_required('fleet.manage')
def save_fleet(request):
    if request.method == 'POST':
        free_move = request.POST.get('free_move', False)
        if(free_move == 'on'):
            free_move = True
        motd = request.POST.get('motd', '')
        name = request.POST.get('name', '')
        groups = request.POST.getlist('groups', [])
        open_fleet(request.POST['character_id'], motd, free_move, name, groups)
    return redirect("fleet:dashboard")