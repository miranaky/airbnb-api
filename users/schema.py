import graphene
from graphene_django import DjangoObjectType
from users.models import User
from users.mutations import (
    CreateUserMutaion,
    UserLoginMutation,
    ToggleFavsMutation,
    EditProfileMutation,
)
from users.queries import resolve_user, resolver_me


class UserType(DjangoObjectType):
    rooms = graphene.Field("rooms.schema.RoomType")

    class Meta:
        model = User
        exclude = ("password", "is_staff", "last_login")


class Query(object):
    user = graphene.Field(
        UserType, id=graphene.Int(required=True), resolver=resolve_user
    )
    me = graphene.Field(UserType, resolver=resolver_me)


class Mutation(object):
    create_account = CreateUserMutaion.Field()
    login = UserLoginMutation.Field()
    toggle_favs = ToggleFavsMutation.Field()
    edit_profile = EditProfileMutation.Field()
