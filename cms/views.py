from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, ProfileSerializer, ContentSerializer, CategorySerializer
from .models import Profile, Content, Category
from django.db.models import Q

# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the CMS!")


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    
class ProfileDetail(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

class IsAuthorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author or request.user.profile.role == 'admin'

class ContentListCreate(generics.ListCreateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ContentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [IsAuthorOrAdmin]


class ContentSearch(generics.ListAPIView):
    serializer_class = ContentSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q')
        if query:
            return Content.objects.filter(
                Q(title__icontains=query) |
                Q(body__icontains=query) |
                Q(summary__icontains=query) |
                Q(categories__name__icontains=query)
            ).distinct()
        return Content.objects.all()


