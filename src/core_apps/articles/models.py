from django.db import models

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _ 

from autoslug import AutoSlugField
from taggit.managers import TaggableManager

from core_apps.common.models import TimeStampModel
from .article_read_time_engine import ArticleReadTimeEngine

User = get_user_model()


class Article(TimeStampModel): 
        ''' Model for individual Article object '''
        author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
        title = models.CharField(verbose_name=_('Article Title'), max_length=255)
        slug = AutoSlugField(populate_from='title', always_update=True, unique=True)
        description = models.CharField(verbose_name=_('Article Description'), max_length=255, blank=True)
        body = models.TextField(verbose_name=_('Article Body'))
        
        banner_image = models.ImageField(verbose_name=_('Banner Image'), upload_to='ArticleMedia/BannerImages', default='/article-default.png')
        body_image_1 = models.ImageField(verbose_name=_('Body Image 1'), upload_to='ArticleMedia/BodyImage1', default='/article-default.png')
        body_image_2 = models.ImageField(verbose_name=_('Body Image 2'), upload_to='ArticleMedia/BodyImage2', default='/article-default.png')

        
        tags = TaggableManager()
        
        # an user can clap multiple articles and an article can have clap of multiple users. 
        clapps = models.ManyToManyField(User, through='Clap', related_name='clapped_articles')
        
        class Meta: 
                verbose_name = _("Article")
                verbose_name_plural = _("Articles")
        
        def __str__(self): 
                return f"{self.author.first_name} {self.author.last_name}'s Article - {self.title}"
        
        
        # calls ArticleReadTimeEngine 
        @property
        def estimated_reading_time(self): 
                return ArticleReadTimeEngine.estimate_reading_time(self)
        
        # article_veiws is the reverse relation with ArticleViews model with Article model. 
        def view_count(self): 
                return self.article_views.count()

         # calculate average rating of individual article instannce 
        def average_rating(self): 
                # self.ratings.all() is the reverse relationship in the Rating model with Article model. 
                # as Rating model has ForeignKey with Article model with related_name "ratings", 
                # we are just getting all the ratings instances of this article instance. 
                ratings = self.ratings.all()  # reverve relation with Rating model 

                if ratings.count() > 0: 
                        total_rating = sum(rating.rating for rating in ratings)
                        average_rating = total_rating / ratings.count()
                        return round(average_rating, 2)
                return None 

class ArticleViews(TimeStampModel): 
        ''' Model for storing each Article Being Viewed By Which User and with What IP Address'''
        article = models.ForeignKey(Article, verbose_name=_("Article being viewed"), on_delete=models.CASCADE, related_name='article_views')
        user = models.ForeignKey(User, verbose_name=_("Article viewd by User"), on_delete=models.CASCADE, related_name='article_views')
        viewer_ip = models.GenericIPAddressField(verbose_name=_("Viewer IP"), null=True, blank=True)

        class Meta:         
                verbose_name = _("Article View")
                verbose_name_plural = _("Article Views")
                unique_together = ('article', 'user', 'viewer_ip')
                
        def __str__(self) -> str:
                user_info = f'{self.user.first_name.title()} {self.user.last_name.title()}' if self.user else 'Anonymous User'
                return f'{self.article.title} viewed by {user_info} from IP {self.viewer_ip}'
        
        @classmethod
        def record_view(cls, article, user, viewer_ip): 
                article_view, created = cls.objects.get_or_create(article=article, user=user, viewer_ip=viewer_ip)
                article_view.save()




class Clap(TimeStampModel): 
        ''' Model to store the claps to an Article by Users '''
        article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='claps')
        user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='claps')
        
        class Meta: 
                unique_together = ['article', 'user']
                ordering = ['-created_at']
        
        def __str__(self) -> str:
                return f'{self.user.first_name.title()} {self.user.last_name.title()} clapped the Article - {self.article.title}!'