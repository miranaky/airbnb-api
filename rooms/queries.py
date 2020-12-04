from rooms.models import Room


def resolve_rooms(info, page=1):
    if page < 1:
        page = 1
    page_size = 10
    skipping = (page - 1) * page_size
    taking = page * page_size
    rooms = Room.objects.all()[skipping:taking]
    total = Room.objects.count()
    return RoomListResponse(arr=rooms, total=total)


def resolve_room(info, id):
    return Room.objects.get(pk=id)
