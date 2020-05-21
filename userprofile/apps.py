from django.apps import AppConfig


class UserprofileConfig(AppConfig):
    name = 'userprofile'

    def ready(self): # method just to import the signals
    	import userprofile.signals
