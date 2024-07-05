from django.urls import path
from .views import UserCreate, ProfileDetail
from .views import ContentListCreate, ContentDetail
from .views import ContentSearch


urlpatterns = [
    path('register/', UserCreate.as_view(), name='register'),
    path('profile/<int:pk>/', ProfileDetail.as_view(), name='profile-detail'),
    path('contents/', ContentListCreate.as_view(), name='content-list-create'),
    path('contents/<int:pk>/', ContentDetail.as_view(), name='content-detail'),
    path('contents/search/', ContentSearch.as_view(), name='content-search'),
]
