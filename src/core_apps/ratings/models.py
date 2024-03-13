from django.db import models

from django.utils.translation import gettext_lazy as _ 
from django.contrib.auth import get_user_model

from core_apps.articles.models import Article
from core_apps.common.models import TimeStampModel


User = get_user_model()

class Ratings(TimeStampModel): 
        RATING_CHOICES = [
                (1, 'Poor'),
                (2, 'Fair'),
                (3, 'Good'), 
                (4, 'Very Good'), 
                (5, 'Excellent') 
        ]

        article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='ratings')
        rating = models.PositiveSmallIntegerField(verbose_name=_('Article Rating'), choices=RATING_CHOICES)
        user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_rating')
        review = models.TextField(verbose_name=_('Article Review'), blank=True)
        
        class Meta: 
                verbose_name = 'Rating'
                verbose_name_plural = 'Ratings'
                unique_together = ('article', 'user')
        
        def __str__(self) -> str:
                return f"{self.user.first_name.title()}  {self.user.last_name.title()} rated {self.article.title} as {self.get_rating_display()}"
                # get_rating_display automatically created by django with field that has choices attached. ( get_ choiceField _display)
