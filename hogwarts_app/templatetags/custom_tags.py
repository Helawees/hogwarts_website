from django import template

register = template.Library()

@register.filter
def in_group(user, group_name: str):
    """
    Проверяет, состоит ли пользователь в указанной группе.
    :param user: Объект пользователя
    :param group_name: Имя группы (строка)
    :return: True, если пользователь в группе; иначе False
    """
    if user.is_authenticated:  # Проверяем, что пользователь авторизован
        return user.groups.filter(name=group_name).exists()
    return False