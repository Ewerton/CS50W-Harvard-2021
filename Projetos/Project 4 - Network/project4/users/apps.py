from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    default_auto_field = 'django.db.models.BigAutoField'
    #
    #profile_pic_folder = settings.PROFILE_PICS_URL # 'media/profile_pics/'

    def ready(self):
        import users.signals