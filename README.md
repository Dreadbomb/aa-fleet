# Fleet plugin app for Alliance Auth

This is an fleet plugin app for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth) (AA).

![License](https://img.shields.io/badge/license-MIT-green) ![python](https://img.shields.io/badge/python-3.6-informational) ![django](https://img.shields.io/badge/django-2.2-informational)

## Features

Alliance Fleet offers the following main features:

- Create a fleet advert on auth
- Restrict fleet advert to some AuthGroups
- Set MOTD and Free Move from auth
- Automaticly kill the fleet advert if the creator is out of fleet or changed fleet
- Invite any character related to the user on auth
- FC View with an aggregation of ships in fleet with variation each 60 seconds

![fleets](img/fleets.png)

![fleet_advert_create](img/fleet_advert_create.png)

![fleet_invite](img/fleet_invite.png)

![fleet_view](img/fleet_view.png)

## Installation

### 1. Install app

Install into your Alliance Auth virtual envrionment from github
```bash
pip install aa-fleet
```

### 2. Update Eve Online app

update the Eve Online app used for authentication in your AA installation to include the following scopes:

```plain
esi-fleets.read_fleet.v1
esi-fleets.write_fleet.v1
```

### 3. Configure AA settings
Configure your AA settings ('local.py') as follows:

- Add `'fleet'` to `INSTALLED_APP`
- Add these lines to the bottom of your settings file:

```python
#settings for fleet
CELERYBEAT_SCHEDULE['fleet_check_fleet_adverts'] = {
    'task': 'fleet.tasks.check_fleet_adverts',
    'schedule': crontab(minute='*/1'),
}
```

### 4. Finalize installation into AA

Run migrations & copy static files

```bash
python manage.py migrate
python manage.py collectstatic
```

Restart your supervisor services for AA

### 5. Setup permissions

Now you can access Alliance Auth and setup permissions for your users. See section **Permissions** below for details.

## Updating

To update your existing installation of Alliance Fleet first enable your virtual environment.

Then run the following commands from your AA project directory (the one that contains `manage.py`).

```bash
pip install -U aa-fleet
```

```bash
python manage.py migrate
```

```bash
python manage.py collectstatic
```

Finally restart your AA supervisor services.

## Permissions

This is an overview of all permissions used by this app:

Name | Purpose | Code
-- | -- | --
Can add / manage fleets | Let a user create and update fleet information |  `manage`
Can access this app |Enabling the app for a user. This permission should be enabled for everyone who is allowed to use the app (e.g. Member state) |  `fleet_access`