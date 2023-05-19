from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from social_link_aggregator.models import Link
from social_link_aggregator.serializers import LinkSerializer


# Create your views here.
class LinkViewSet(viewsets.ModelViewSet):
    """
    A view to manage all the actions regarding /links endpoints
    """
    queryset = Link.objects.all().order_by("-score")
    serializer_class = LinkSerializer

    @action(detail=True, methods=['post'])
    def upvote(self, request, pk=None):
        link = self.get_object()
        link.upvotes += 1
        link.score += 1
        link.save()
        serializer = self.get_serializer(link)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def downvote(self, request, pk=None):
        link = self.get_object()
        link.downvotes += 1
        link.score -= 1
        link.save()
        serializer = self.get_serializer(link)
        return Response(serializer.data)
