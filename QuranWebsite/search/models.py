from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

class UserSearch(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    search_count = models.IntegerField(default=0)
    last_search_time = models.DateTimeField(auto_now=True)
    max_search_limit = models.IntegerField(default=5) 

    def __str__(self):
        return f"{self.user.username} - Searches: {self.search_count}, Limit: {self.max_search_limit}"
