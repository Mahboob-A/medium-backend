from django.db import models
from django.contrib.auth import get_user_model


from core_apps.common.models import TimeStampModel
from core_apps.articles.models import Article


User = get_user_model()


class Bookmark(TimeStampModel): 
        ''' Model for Bookmarks of an Article by an User '''
        user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
        article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='bookmarks')
        

        class Meta: 
                unique_together = ['user', 'article']
                ordering = ['-created_at']

        def __str__(self) -> str:
                return f'{self.user.first_name.title()} {self.user.last_name.title()} bookmarked {self.article.title} !'
        
