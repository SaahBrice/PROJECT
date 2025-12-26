# Settings module - imports from development by default
# For production: set DJANGO_SETTINGS_MODULE=fdtm.settings.production

import os

environment = os.environ.get('DJANGO_ENV', 'development')

if environment == 'production':
    from .production import *
else:
    from .development import *
