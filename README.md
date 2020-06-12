# Fleet plugin app for Alliance Auth

This is an fleet plugin app for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth) (AA) that can be used as starting point to develop custom plugins.

![License](https://img.shields.io/badge/license-MIT-green) ![python](https://img.shields.io/badge/python-3.5-informational) ![django](https://img.shields.io/badge/django-2.2-informational)

## Features

- The plugin can be installed, upgraded (and removed) into an existing AA installation using PyInstaller.

- It has it's own menu item in the sidebar.

- It has one view that shows a panel and some text

## How to use it

To use this fleet as basis for your own development just fork this repo and then clone it on your dev machine.

You then should rename the app and then you can install it into your AA dev installation.

### Cloning from repo

For this app we are assuming that you have all your AA projects, your virtual environement and your AA installation under one top folder (e.g. aa-dev).

This should look something like this:

```plain
aa-dev
|- venv/
|- myauth/
|- allianceauth-fleet-plugin
|- (other AA projects ...)

```

Then just cd into the top folder (e.g. aa-dev) and clone the repo from your fork. You can give the repo a new name right away (e.g. `allianceauth-your-app-name`).
You also want to create a new git repo for it.

```bash
git clone https://gitlab.com/YourName/allianceauth-fleet-plugin.git allianceauth-your-app-name
cd allianceauth-your-app-name
rm -rf .git
git init
```

### Renaming the app

Before installing this app into your dev AA you need to rename it to something suitable for your development project. Otherwise you risk not being able to install additional apps that might also be called fleet.

Here is an overview of the places that you need to edit to adopt the name.

Easiest is to just find & replace `fleet` with your new app name in all files listed below. 

One small warning about picking names: Python is a bit particular about what special characters are allowed for names of modules and packages. To avoid any pitfalls I would therefore recommend to use only normal characters (a-z) in your app's name unless you know exactly what you are doing.

Location | Description
-- | --
/fleet/ | folder name
/fleet/templates/fleet/ | folder name
/setup.py | update modul name for version import, update package name, update title, author, etc.
/MANIFEST.IN | path of files to include / exclude for PyInstaller
/fleet/apps.py | app name
`/fleet/__init__.py` | app name
/fleet/auth_hooks.py | menu hook config incl. icon and label of your app's menu item appearing in the sidebar
/fleet/models.py | app name
/fleet/urls.py | app name
/fleet/views.py | permission name and template path
/fleet/templates/fleet/base.html | Title of your app to be shown in all views and as title in the browser tab
/fleet/templates/fleet/index.html | template path
/README.md | clear content
/LICENSE | Replace with your own license

## Clearing migrations

Instead of renaming your app in the migrations its easier to just recreate them later in the process. For this to work you need to delete the old migration files in your migrations folder.

```bash
rm your-app-name/migrations/0001_initial.py
rm -rf your-app-name/migrations/_pycache
```

## Installing into your dev AA

Once you have cloned or copied all files into place and finished renaming the app you are ready to install it to your dev AA instance.

Make sure you are in your venv. Then install it with pip in editable mode:

```bash
pip install -e allianceauth-your-app-name
```

First add your app to the Django project by adding the name of your app to INSTALLED_APPS in `settings/local.py`.

Next we will create new migrations for your app:

```bash
python manage.py makemigrations
```

Then run a check to see if everything is setup correctly.

```bash
python manage.py check
```

In case they are errors make sure to fix them before proceeding.

Next perform migrations to add your model to the database:

```bash
python manage.py migrate
```

Finally restart your AA server and that's it.

## Installing into production AA

To install your plugin into a production AA run this command within the virtual Python environment of your AA installation:

```bash
pip install git+https://gitlab.com/YourName/allianceauth-your-app-name
```

Alternatively you can create a package file and manually deliver it to your production AA:

```bash
python setup.py sdist
```

And then install it directly from the package file

```bash
pip install your-package-app.tar.gz
```

Then add your app to `INSTALLED_APPS` in `settings/local.py`, run migrations and restart your allianceserver.

## Contribute

If you made a new app for AA please consider sharing it with the rest of the community. For any questions on how to share your app please contact the AA devs on their Discord. You find the current community creations [here](https://gitlab.com/allianceauth/community-creations).
