import graphene
from graphene_django import DjangoObjectType
from users.models import User
from users.mutations import CreateUserMutaion, UserLoginMutation
from users.queries import resolve_user


class UserType(DjangoObjectType):
    rooms = graphene.Field("rooms.schema.RoomType")

    class Meta:
        model = User
        exclude = ("password", "is_staff", "last_login")


class Query(object):
    user = graphene.Field(
        UserType, id=graphene.Int(required=True), resolver=resolve_user
    )


class Mutation(object):
    create_account = CreateUserMutaion.Field()
    login = UserLoginMutation.Field()
