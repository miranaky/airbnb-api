import graphene
from graphene_django import DjangoObjectType
from users.models import User


class UserType(DjangoObjectType):
    rooms = graphene.Field("rooms.schema.RoomType")

    class Meta:
        model = User
        exclude = ("password", "is_staff", "last_login")


class Query(object):
    user = graphene.Field(UserType, id=graphene.Int(required=True))

    def resolve_user(self, info, id):
        return User.objects.get(id=id)