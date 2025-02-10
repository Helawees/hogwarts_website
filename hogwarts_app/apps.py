from django.apps import AppConfig


class HogwartsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hogwarts_app'

    def ready(self):
        """Динамическое добавление метода проверки
        принадлежности пользователя к группе"""
        from django.contrib.auth.models import User

        def is_in_group(self, group_name: str):
            if self.groups.filter(name=group_name).exists():
                return True
            else:
                return False

        User.add_to_class("is_in_group", is_in_group)
