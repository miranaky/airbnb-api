from users.models import User


def resolve_user(parent, info, id):
    return User.objects.get(id=id)
