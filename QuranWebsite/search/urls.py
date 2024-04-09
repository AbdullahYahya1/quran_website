from django.urls import path
from .views import QuranSearchView
urlpatterns = [
    path('', QuranSearchView.as_view(), name='quran_search'),
]
