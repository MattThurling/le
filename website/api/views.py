from rest_framework import views, viewsets, permissions, response
from rest_framework.decorators import action
from website.models import TimeLog, TabooSet
from django.db.models import Q
from .serializers import TimeLogSerializer, UserSerializer, TabooCardSerializer, TabooSetSerializer

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
    serializer_class = TabooSetSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = TabooSet.objects.all()
        user = self.request.user if self.request.user.is_authenticated else None

        # Temporary hack to provide the default sets
        q = Q(owner__id=1) 

        # ... and the auth user's sets
        if user:
            q |= Q(owner=user)

        # ... or the anonymous user's sets
        q |= Q(session_key = self.request.session.session_key)

        return queryset.filter(q)


    @action(detail=True, methods=["get"], url_path="cards")
    def cards(self, request, pk=None):
        taboo_set = self.get_object()
        cards = (
            taboo_set.cards
            .select_related("target")
            .prefetch_related("taboo_links__taboo_word")
            .all()
        )
        serializer = TabooCardSerializer(cards, many=True)
        return response.Response(serializer.data)