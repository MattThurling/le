from rest_framework import views, viewsets, permissions, response
from website.models import TimeLog
from django.contrib.auth.models import User
from .serializers import TimeLogSerializer, UserSerializer

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