import json
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


def load_and_preprocess_quran_data(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        data = json.load(file)
    preprocessed_data = {}
    for surah in data:
        preprocessed_data[surah['id']] = {
            ayah['id']: {
                'Surah Name': surah['name'],
                'Ayah ID': ayah['id'],
                'Arabic Text': ayah['ar'],
                'English Text': ayah['en']
            }
            for ayah in surah['array']
        }
    return preprocessed_data

def get_ayah_details(preprocessed_data, surah_id, ayah_id):
    try:
        return preprocessed_data[surah_id][ayah_id]
    except KeyError:
        return {'error': 'Surah or Ayah not found'}

file_path = os.path.join(settings.BASE_DIR, 'resources', 'Quran.json')
preprocessed_data = load_and_preprocess_quran_data(file_path)

import re  # Import regular expressions

class QuranSearchView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get(self, request):
        user_search, _ = UserSearch.objects.get_or_create(user=request.user)
        # Reset search count after an hour
        if user_search.last_search_time < timezone.now() - timedelta(hours=1):
            user_search.search_count = 0
        # Check search limit
        if user_search.search_count >= user_search.max_search_limit:
            return Response({"error": "Search limit reached. Please try again later."}, status=429)
        user_search.search_count += 1
        user_search.last_search_time = timezone.now()
        user_search.save()

        query = request.query_params.get('query', None)
        if query:
            results = find_top_related_verses(query, model, df)
            data = []
            for _, row in results.iterrows():
                ayah_details = get_ayah_details(preprocessed_data, int(row['surah_name']), int(row['verse_id']-1))
                name = ayah_details.get('Surah Name', 'Unknown Surah')
                arabic = ayah_details.get('Arabic Text', 'No Arabic text available')

                # Process the text to modify the number
                match = re.match(r'(\d+)(.*)', row['processed_text'])
                if match:
                    number = int(match.group(1)) - 1
                    text = f"{number}{match.group(2)}"
                else:
                    text = row['processed_text']  # Use original text if no number is found

                data.append({
                    "surah_name": name,
                    "verse_id": row['verse_id'],
                    "text": f"{text} * {arabic}"
                })
            return Response({"results": data})
        return Response({"error": "No query provided"}, status=400)
