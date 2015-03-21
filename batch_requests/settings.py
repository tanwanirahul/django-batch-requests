'''
@author: Rahul Tanwani

@summary: Contains the default settings.
'''

from django.conf import settings

DEFAULTS = {
    "HEADERS_TO_INCLUDE": ["HTTP_USER_AGENT", "HTTP_COOKIE"],
    "DEFAULT_CONTENT_TYPE": "application/json",
    "USE_HTTPS": False,
    "MAX_LIMIT": 20
}


USER_DEFINED_SETTINGS = getattr(settings, 'BATCH_REQUESTS', {})


class BatchRequestSettings(object):

    '''
        Allow API settings to be accessed as properties.
    '''

    def __init__(self, user_settings=None, defaults=None):
        self.user_settings = user_settings or {}
        self.defaults = defaults or {}

    def __getattr__(self, attr):
        '''
            Override the attribute access behavior.
        '''

        if attr not in self.defaults.keys():
            raise AttributeError("Invalid API setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Cache the result
        setattr(self, attr, val)
        return val


br_settings = BatchRequestSettings(USER_DEFINED_SETTINGS, DEFAULTS)
