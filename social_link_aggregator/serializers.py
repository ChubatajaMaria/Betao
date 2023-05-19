from django.core.validators import URLValidator
from rest_framework import serializers
from .models import Link

class LinkSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(read_only=True)

    class Meta:
        model = Link
        fields = ["id", "url", "created", "upvotes", "downvotes", "score"]