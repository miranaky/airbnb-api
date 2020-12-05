from users.models import User


def resolve_user(parent, info, id):
    return User.objects.get(id=id)


def resolver_me(parent, info):
    user = info.context.user
    if user.is_authenticated:
        return user
    else:
        raise Exception("You need to logged in.")