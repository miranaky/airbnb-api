from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .models import Room
from .serializers import RoomSerializer


class OwnPaginator(PageNumberPagination):
    page_size = 20


class RoomsView(APIView):
    def get(self, request):
        paginator = OwnPaginator()
        rooms = Room.objects.all()
        result = paginator.paginate_queryset(rooms, request)
        serializer = RoomSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save(user=request.user)
            room_serializer = RoomSerializer(room).data
            return Response(data=room_serializer, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response()


class RoomView(APIView):
    def get_room(self, pk):
        try:
            room = Room.objects.get(pk=pk)
            return room
        except Room.DoesNotExist:
            return None

    def get(self, request, pk):
        room = self.get_room(pk)
        if room is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = RoomSerializer(room).data
            return Response(serializer)

    def put(self, request, pk):
        room = self.get_room(pk)
        if room is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serializer = RoomSerializer(room, data=request.data, partial=True)
            if serializer.is_valid():
                room = serializer.save()
                return Response(RoomSerializer(room).data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response()

    def delete(self, request, pk):
        room = self.get_room(pk)
        if room is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            room.delete()
            return Response(status=status.HTTP_200_OK)
