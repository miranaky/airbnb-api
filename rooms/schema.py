import graphene
from graphene_django import DjangoObjectType
from rooms.models import Room


class RoomType(DjangoObjectType):

    user = graphene.Field("users.schema.UserType")

    class Meta:
        model = Room


class RoomListResponse(graphene.ObjectType):

    arr = graphene.List(RoomType)
    total = graphene.Int()


class Query(object):

    rooms = graphene.Field(RoomListResponse, page=graphene.Int())

    def resolve_rooms(self, info, page=1):
        if page < 0:
            page = 1
        page_size = 10
        skipping = (page - 1) * page_size
        taking = page * page_size
        rooms = Room.objects.all()[skipping:taking]
        total = Room.objects.count()
        return RoomListResponse(arr=rooms, total=total)
