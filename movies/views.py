from django.db.models import Avg, Count
from rest_framework import generics,response, status, views
from movies.models import Movie
from movies.serializers import MovieModelSerializer
from rest_framework.permissions import IsAuthenticated
from core.permissions import GlobalDefaultPermission
from reviews.models import Review


class MovieCreateListView(generics.ListCreateAPIView):
  permission_classes = (IsAuthenticated,GlobalDefaultPermission,)
  queryset = Movie.objects.all()
  serializer_class = MovieModelSerializer

class MovieRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = (IsAuthenticated,GlobalDefaultPermission,)
  queryset = Movie.objects.all()
  serializer_class = MovieModelSerializer

class MovieStatsView(views.APIView):
  permission_classes = (IsAuthenticated,GlobalDefaultPermission,)
  queryset = Movie.objects.all()

  def get(self, request):
    count_movies = self.queryset.count()
    movies_by_genre = self.queryset.values('genre__name').annotate(count=Count('id'))
    count_reviews = Review.objects.count()
    average_stars = Review.objects.aggregate(avg_stars=Avg('stars'))['avg_stars'] 

    data = {
      'count_movies' :count_movies,
      'movies_by_genre' : movies_by_genre,
      'count_reviews' : count_reviews,
      'average_stars' : round(average_stars,2) if average_stars else 0
    }

    return response.Response(
      data=data,
      status=status.HTTP_200_OK
    )