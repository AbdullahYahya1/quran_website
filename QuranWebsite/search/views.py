from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import find_top_related_verses, load_model_and_embeddings
from django.conf import settings
import os
from rest_framework.permissions import IsAuthenticated
from .models import UserSearch
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

# Assuming your model and embeddings are stored as follows:
model_path = os.path.join(settings.BASE_DIR, 'resources', 'model')
embeddings_path = os.path.join(settings.BASE_DIR, 'resources', 'quran_embeddings.pkl')

model, df = load_model_and_embeddings(model_path, embeddings_path)
class QuranSearchView(APIView):
    def get(self, request):
        permission_classes = [IsAuthenticated]
        authentication_classes = [SessionAuthentication, TokenAuthentication]
        user_search, _ = UserSearch.objects.get_or_create(user=request.user)
        if user_search.last_search_time < timezone.now() - timedelta(hours=1):
            user_search.search_count = 0
        if user_search.search_count >= user_search.max_search_limit:
            return Response({"error": "Search limit reached. Please try again later."}, status=429)
        user_search.search_count += 1
        user_search.save()
        query = request.query_params.get('query', None)
        if query:
            results = find_top_related_verses(query, model, df)
            data = [
                {
                    "surah_name": row['surah_name'],
                    "verse_id": row['verse_id'],
                    "text": row['processed_text']
                } for _, row in results.iterrows()
            ]
            return Response({"results": data})
        return Response({"error": "No query provided"}, status=400)
