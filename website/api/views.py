from rest_framework import views, viewsets, permissions, response
from rest_framework.decorators import action
from website.models import TimeLog, TabooSet, TabooCard
from django.contrib.auth.models import User
from .serializers import TimeLogSerializer, UserSerializer, TabooCardSerializer

class TimeLogViewSet(viewsets.ModelViewSet):
    serializer_class = TimeLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TimeLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CurrentUserAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return response.Response(serializer.data)

class TabooSetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TabooSet.objects.all()

    @action(detail=True, methods=["get"], url_path='cards')
    def cards(self, request, pk=None):
        taboo_set = self.get_object()
        cards = taboo_set.cards.prefetch_related("taboo_links", "target").all()
        serializer = TabooCardSerializer(cards, many=True)
        return response.Response(serializer.data)
