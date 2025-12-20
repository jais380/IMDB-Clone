from rest_framework import serializers
from watchmate.models import StreamPlatform, WatchList, Review


class ReviewSerializers(serializers.ModelSerializer):

    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:

        model = Review

        fields = '__all__'


class WatchListSerializers(serializers.ModelSerializer):

    class Meta:

        model = WatchList
        fields = '__all__'

        

class StreamPlatformSerializers(serializers.ModelSerializer):

    watchlist = WatchListSerializers(many=True, read_only=True)

    class Meta:

        model = StreamPlatform
        fields = '__all__'