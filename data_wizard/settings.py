from rest_framework.settings import import_from_string as drf_import
from django.conf import settings


DEFAULTS = {
    'BACKEND': '.backends.threading',
    'LOADER': '.loaders.FileLoader',
    'PERMISSION': 'rest_framework.permissions.IsAdminUser',
}


def get_setting(name):
    #  FIXME: Drop this in 2.0
    if getattr(settings, 'CELERY_RESULT_BACKEND', None):
        DEFAULTS['BACKEND'] = '.backends.celery'

    wizard_settings = getattr(settings, 'DATA_WIZARD', {})
    return wizard_settings.get(name, DEFAULTS[name])


def import_from_string(path, setting_name):
    try:
        obj = drf_import(path, setting_name)
    except ImportError as e:
        msg = e.args[0].replace("API", "Data Wizard")
        raise ImportError(msg)
    else:
        return obj


def import_setting(name):
    path = get_setting(name)
    return import_from_string(path, name)
