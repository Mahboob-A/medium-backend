import logging

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django_elasticsearch_dsl.registries import registry

from core_apps.articles.models import Article

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Article)
def update_document(sender, instance=None, created=False, **kwargs):
    """Update the ArticleDocument in Elasticsearch when article object is updated or created"""
    # update the instance state in the elastic search
    registry.update(instance)
    if created:
        logger.info(
            f"\nLog from core_apps.searches.signals.update_document Signal: \n"
            f"\nArticle {instance.title} created by {instance.author.first_name.title()} {instance.author.last_name.title()}\n"
        )
    else:
        logger.info(
            f"\nLog from core_apps.searches.signals.update_document Signal: "
            f"\nArticle {instance.title} updated by {instance.author.first_name.title()} {instance.author.last_name.title()}\n"
        )


@receiver(post_delete, sender=Article)
def delete_document(sender, instance=None, **kwargs):
    """Delete the ArticleDocument in Elasticsearch when article object is updated or created"""
    # delete the instance state in the elastic search
    registry.delete(instance)
    logger.info(
        f"\nLog from core_apps.searches.signals.delete_document Signal: \n"
        f"\nArticle {instance.title} deleted by {instance.author.first_name.title()} {instance.author.last_name.title()}\n"
    )
