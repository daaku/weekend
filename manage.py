#!/usr/bin/env python

import os.path as path
import site

project_dir = path.realpath(path.dirname(__file__))
site.addsitedir(path.join(project_dir, 'lib'))

from django.core.management import execute_manager
import weekend.settings as settings

# enable debug stuff
import logging
import colorized_logger
logging.debug('Enabled DEBUG mode')

import sys
sys.stdout = sys.stderr

settings.DEBUG = settings.TEMPLATE_DEBUG = True
settings.INTERNAL_IPS = (
    '172.16.75.2',
    '67.169.165.78',
    '::1',
    '127.0.0.1',
    '207.192.74.92',
)
if hasattr(settings, 'TEMPLATE_CONTEXT_PROCESSORS'):
    settings.TEMPLATE_CONTEXT_PROCESSORS += (
        'django.core.context_processors.debug',
    )
settings.MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
settings.INSTALLED_APPS += (
    'django_extensions',
    'debug_toolbar',
)
settings.DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.logger.LoggingPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.cache.CacheDebugPanel',
)

if __name__ == "__main__":
    execute_manager(settings)
