from rest_framework import serializers
from users.serializers import RelateUserSerializer
from .models import Room


class ReadRoomSerializer(serializers.ModelSerializer):

    user = RelateUserSerializer()

    class Meta:
        model = Room
        exclude = ("modified",)


class WriteRoomSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=140)
    address = serializers.CharField(max_length=140)
    price = serializers.IntegerField()
    beds = serializers.IntegerField(default=1)
    lat = serializers.DecimalField(max_digits=10, decimal_places=6)
    lng = serializers.DecimalField(max_digits=10, decimal_places=6)
    bedrooms = serializers.IntegerField(default=1)
    bathrooms = serializers.IntegerField(default=1)
    check_in = serializers.TimeField(default="00:00:00")
    check_out = serializers.TimeField(default="00:00:00")
    instant_book = serializers.BooleanField(default=False)

    def validate(self, data):
        if self.instance:
            check_in = data.get("check_in", self.instance.check_in)
            check_out = data.get("check_out", self.instance.check_out)
        else:
            check_in = data.get("check_in")
            check_out = data.get("check_out")
        if check_in == check_out:
            raise serializers.ValidationError("Not enough time between changes")
        return data

    def create(self, validated_data):
        return Room.objects.create(**validated_data)

    def update(self, instance, validate_data):
        instance.name = validate_data.get("name", instance.name)
        instance.address = validate_data.get("address", instance.address)
        instance.price = validate_data.get("price", instance.price)
        instance.beds = validate_data.get("beds", instance.beds)
        instance.lat = validate_data.get("lat", instance.lat)
        instance.lng = validate_data.get("lng", instance.lng)
        instance.bedrooms = validate_data.get("bedrooms", instance.bedrooms)
        instance.bathrooms = validate_data.get("bathrooms", instance.bathrooms)
        instance.check_in = validate_data.get("check_in", instance.check_in)
        instance.check_out = validate_data.get("check_out", instance.check_out)
        instance.instant_book = validate_data.get("instant_book", instance.instant_book)
        instance.save()
        return instance