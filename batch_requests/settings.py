'''
@author: Rahul Tanwani

@summary: Contains the default settings.
'''

from django.conf import settings
from django.utils.importlib import import_module

DEFAULTS = {
    "HEADERS_TO_INCLUDE": ["HTTP_USER_AGENT", "HTTP_COOKIE"],
    "DEFAULT_CONTENT_TYPE": "application/json",
    "USE_HTTPS": False,
    "EXECUTE_PARALLEL": False,
    "MAX_LIMIT": 20
}


USER_DEFINED_SETTINGS = getattr(settings, 'BATCH_REQUESTS', {})


def import_class(class_path):
    '''
        Imports the class for the given class name.
    '''
    module_name, class_name = class_path.rsplit(".", 1)
    module = import_module(module_name)
    claz = getattr(module, class_name)
    return claz


class BatchRequestSettings(object):

    '''
        Allow API settings to be accessed as properties.
    '''

    def __init__(self, user_settings=None, defaults=None):
        self.user_settings = user_settings or {}
        self.defaults = defaults or {}
        self.executor = self._executor()

    def _executor(self):
        '''
            Creating an ExecutorPool is a costly operation. Executor needs to be instantiated only once.
        '''
        if self.EXECUTE_PARALLEL is False:
            executor_path = "batch_requests.concurrent.executor.SequentialExecutor"
            executor_class = import_class(executor_path)
            return executor_class()

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
