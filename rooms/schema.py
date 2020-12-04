import graphene
from rooms.models import Room
from rooms.types import RoomType, RoomListResponse


class Query(object):

    rooms = graphene.Field(RoomListResponse, page=graphene.Int())
    room = graphene.Field(RoomType, id=graphene.Int(required=True))

    def resolve_rooms(self, info, page=1):
        if page < 1:
            page = 1
        page_size = 10
        skipping = (page - 1) * page_size
        taking = page * page_size
        rooms = Room.objects.all()[skipping:taking]
        total = Room.objects.count()
        return RoomListResponse(arr=rooms, total=total)

    def resolve_room(self, info, id):
        return Room.objects.get(pk=id)
