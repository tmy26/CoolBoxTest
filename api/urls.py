from django.urls import path
from api.views import SearchView


urlpatterns = [
    path('api/search', SearchView.as_view()),
]
