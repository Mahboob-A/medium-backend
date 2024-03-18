
import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django_elasticsearch_dsl.registries import registry

from core_apps.articles.models import Article


logger = logging.getLogger(__name__)


@receiver(post_save, sender=Article)
def update_document(sender, instance=None, created=False, **kwargs): 
        
        # update the instance state in the elastic search
        registry.update(instance)
        if created: 
                logger.info(
                        f'Log from core_apps.searches.signals.update_document Signal: '
                        f'Article {instance.title} created by {instance.author.first_name.title()} {instance.author.last_name.title()}'
                )
        else: 
                logger.info(
                        f'Log from core_apps.searches.signals.update_document Signal: '
                        f'Article {instance.title} updated by {instance.author.first_name.title()} {instance.author.last_name.title()}'
                )



@receiver(post_delete, sender=Article)
def delete_document(sender, instance=None, **kwargs): 
        
        # update the instance state in the elastic search
        registry.delete(instance)
        logger.info(
                        f'Log from core_apps.searches.signals.delete_document Signal: '
                        f'Article {instance.title} deleted by {instance.author.first_name.title()} {instance.author.last_name.title()}'
                )