from django.urls import path
from api.views import SearchView


urlpatterns = [
    path('api/companies', SearchView.as_view(), name='search_sort_filter'),
]
