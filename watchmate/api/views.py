from django.http import Http404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import filters
from drf_spectacular.utils import extend_schema

from watchmate.models import WatchList, StreamPlatform, Review
from watchmate.api.serializers import StreamPlatformSerializers, WatchListSerializers, ReviewSerializers
from watchmate.api.permissions import IsAdminOrReadonly, IsReviewOrReadonly
from watchmate.api.pagination import WatchListPagination


class UserReview(generics.ListAPIView):

    serializer_class = ReviewSerializers

    def get_queryset(self):
        user = self.request.query_params.get('username', None)

        return Review.objects.filter(review_user__username = user).order_by("-created")



class ReviewcreateAV(generics.CreateAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = ReviewSerializers

    def get_queryset(self):
        return  Review.objects.all()
    
    def perform_create(self, serializer):

        # Get the movie being reviewed
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)

        # To ensure that the user can only review once
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=movie, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError("You have already reviewed this Movie")
        
        # To calculate rating

        if movie.number_rating == 0:
            movie.avg_rating = serializer.validated_data["rating"]
        else: 
            movie.avg_rating = (movie.avg_rating + serializer.validated_data["rating"])/2
        
        movie.number_rating = movie.number_rating + 1
        movie.save()
        
        # save serializer
        serializer.save(watchlist=movie, review_user=review_user)


class ReviewlistAV(generics.ListAPIView):

    permission_classes = [AllowAny]
    
    serializer_class = ReviewSerializers

    def get_queryset(self):
        pk= self.kwargs['pk']

        return Review.objects.filter(watchlist=pk).order_by("-created")



class ReviewdetailAV(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ReviewSerializers
    permission_classes = [IsReviewOrReadonly]

    def get_queryset(self):
        return Review.objects.all()
    
    def perform_update(self, serializer):
        pk = self.kwargs['pk']
        review = Review.objects.get(pk=pk)
        movie = review.watchlist

        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=movie, review_user=review_user)

        if review_queryset.exists():
            
            # rating calculation
            if movie.number_rating == 0 :
                movie.avg_rating = serializer.validated_data['rating']
            else:
                movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating'])/2
            movie.number_rating = movie.number_rating + 1

            movie.save()

            serializer.save(watchlist=movie, review_user=review_user)
        else:
            raise ValidationError('Update is impossible as this review is not yours')



class WatchlistAV(generics.ListCreateAPIView):

    permission_classes= [IsAdminOrReadonly]
    pagination_class = WatchListPagination

    queryset = WatchList.objects.all().order_by("-created")

    serializer_class = WatchListSerializers

    filter_backends = [filters.SearchFilter]

    search_fields = ['title', '=platform__name']



class WatchlistdetailAV(generics.RetrieveUpdateDestroyAPIView):

    permission_classes= [IsAdminOrReadonly]

    queryset = WatchList.objects.all()

    serializer_class = WatchListSerializers



class StreamplatformList(APIView):

    permission_classes = [IsAdminOrReadonly]

    @extend_schema(
        responses=StreamPlatformSerializers(many=True),
    )
    def get(self, request):
        stream = StreamPlatform.objects.all()

        serializers = StreamPlatformSerializers(stream, many=True)
        return Response(serializers.data)
    
    @extend_schema(
        request=StreamPlatformSerializers,
        responses=StreamPlatformSerializers,
    )
    def post(self, request):
        serializers = StreamPlatformSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
  
        

class StreamplatformDetail(APIView):

    permission_classes = [IsAdminOrReadonly]

    @extend_schema(
        responses=StreamPlatformSerializers,
    )
    def get_object(self, pk):
        try:
            return StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            raise Http404

    @extend_schema(
        responses=StreamPlatformSerializers,
    )
    def get(self, request, pk):
        
        stream = self.get_object(pk)

        serializers = StreamPlatformSerializers(stream)
        return Response(serializers.data)

    @extend_schema(
        request=StreamPlatformSerializers,
        responses=StreamPlatformSerializers,
    )   
    def put(self, request, pk):
        
        stream = self.get_object(pk)

        serializers = StreamPlatformSerializers(stream, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses={204: None})    
    def delete(self, request, pk):
        
        stream = self.get_object(pk)
        
        stream.delete()
        return Response({
            "message": "Stream has been deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)
