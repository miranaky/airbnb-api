from django.contrib.auth import authenticate
from django.conf import settings
import graphene
import jwt
from users.models import User
from rooms.models import Room


class CreateUserMutaion(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    error = graphene.String()

    def mutate(root, info, email, password, first_name=None, last_name=None):
        try:
            User.objects.get(email=email)
            return CreateUserMutaion(ok=False, error="User already exist.")
        except User.DoesNotExist:
            try:
                User.objects.create_user(email, email, password)
                return CreateUserMutaion(ok=True)
            except Exception:
                return CreateUserMutaion(ok=False, error="Can't create User.")


class UserLoginMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.String()
    error = graphene.String()
    pk = graphene.Int()

    def mutate(root, info, email, password):
        user = authenticate(username=email, password=password)
        if user:
            token = jwt.encode({"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256")
            return UserLoginMutation(token=token.decode("utf-8"), pk=user.pk)
        else:
            return UserLoginMutation(error="Username/Password is wrong")


class ToggleFavsMutation(graphene.Mutation):
    class Arguments:
        room_id = graphene.Int(required=True)

    ok = graphene.Boolean()
    error = graphene.String()

    def mutate(root, info, room_id):
        user = info.context.user
        if user.is_authenticated:
            try:
                room = Room.objects.get(pk=room_id)
                if room in user.favs.all():
                    user.favs.remove(room)
                else:
                    user.favs.add(room)
                return ToggleFavsMutation(ok=True)
            except Room.DoesNotExist:
                return ToggleFavsMutation(ok=False, error="Room Does not exist.")
        else:
            return ToggleFavsMutation(ok=False, error="You need to logged in")


class EditProfileMutation(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()

    ok = graphene.Boolean()
    error = graphene.String()

    def mutate(root, info, first_name=None, last_name=None, email=None):
        user = info.context.user
        if user.is_authenticated:
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if email:
                try:
                    User.objects.get(email=email)
                    return EditProfileMutation(
                        ok=False, error="That email already taken."
                    )
                except User.DoesNotExist:
                    user.email = email
            user.save()
            return EditProfileMutation(ok=True)
        else:
            return EditProfileMutation(ok=False, error="You need to logged in")
