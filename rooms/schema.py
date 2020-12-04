import graphene
from rooms.models import Room
from rooms.types import RoomType, RoomListResponse
from rooms.queries import resolve_room, resolve_rooms


class Query(object):

    rooms = graphene.Field(
        RoomListResponse, page=graphene.Int(), resolver=resolve_rooms
    )
    room = graphene.Field(
        RoomType, id=graphene.Int(required=True), resolver=resolve_room
    )
