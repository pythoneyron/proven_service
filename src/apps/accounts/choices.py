
class RoleUser:
    Administrator = '0'
    Expert = '1'
    User = '2'
    Moderator = '3'

    CHOICES = (
        (Administrator, 'Администратор'),
        (Expert, 'Эксперт'),
        (User, 'Пользователь'),
        (Moderator, 'Модератор'),
    )
