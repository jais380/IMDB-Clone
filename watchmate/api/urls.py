from django.urls import path
from watchmate.api import views

urlpatterns = [
    path("stream/", views.StreamplatformList.as_view(), name='stream-list'),
    path("stream/<int:pk>/", views.StreamplatformDetail.as_view(), name="stream-detail"),
    path("watch/", views.WatchlistAV.as_view(), name="movie-list"),
    path("watch/<int:pk>/", views.WatchlistdetailAV.as_view(), name="movie-detail"),
    path("<int:pk>/review/create/", views.ReviewcreateAV.as_view(), name="review-create"),
    path("<int:pk>/reviews/", views.ReviewlistAV.as_view(), name="review-list"),
    path("review/<int:pk>/", views.ReviewdetailAV.as_view(), name="review-detail"),
    path("user/reviews/", views.UserReview.as_view(), name="user-review-list")
]