from django.db import models

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _ 

from autoslug import AutoSlugField
from taggit.managers import TaggableManager

from core_apps.common.models import TimeStampModel
from .article_read_time_engine import ArticleReadTimeEngine

User = get_user_model()


class Article(TimeStampModel): 
        author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
        title = models.CharFiel(verbose_name=_('Article Title'), max_length=255)
        slug = AutoSlugField(populate_from='title', always_update=True, unique=True)
        description = models.CharField(verbose_name=_('Article Description'), max_length=255, blank=True)
        body = models.TextField(verbose_name=_('Article Body'))
        
        banner_image = models.ImageField(verbose_name=_('Banner Image'), default='/article-default.png')
        body_image_1 = models.ImageField(verbose_name=_('Banner Image'), default='/article-default.png')
        body_image_2 = models.ImageField(verbose_name=_('Banner Image'), default='/article-default.png')
        body_image_3 = models.ImageField(verbose_name=_('Banner Image'), default='/article-default.png')
        body_image_4 = models.ImageField(verbose_name=_('Banner Image'), default='/article-default.png')
        
        tags = TaggableManager()
        
        def __str__(self): 
                return f"{self.author.first_name} {self.author.last_name}'s Article - {self.title}"
        
        @property
        def estimated_reading_time(self): 
                return ArticleReadTimeEngine.estimate_reading_time(self)
        