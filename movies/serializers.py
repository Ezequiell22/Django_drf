from rest_framework import serializers
from movies.models import Movie
from django.db.models import Avg


class MovieModelSerializer(serializers.ModelSerializer):
  rate = serializers.SerializerMethodField(read_only=True)

  class Meta:
    model = Movie
    fields = '__all__'

  def get_rate(self, obj):
    # movie . related_name in table review >> reviews.models
    rate = obj.reviews.aggregate(Avg('stars'))['stars__avg']
    if rate:
      return round(rate,2)

    return None

  #validate_ + name of field
  def validate_release_date(self, value):
    if value.year < 1990:
      raise serializers.ValidationError('Data too old')
    return value
  
  def validate_resume(self, value):
    if len(value) > 400:
      raise serializers.ValidationError('Text too big')
    return value