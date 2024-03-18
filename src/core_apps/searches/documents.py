from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from core_apps.articles.models import Article

"""
Modle in Django, Document in elasticsearch. 
We need to define documents for each Django Model we want to index.   

"""

# an another code example of elastic search
# https://github.com/Yagua/BookStore_API/tree/master/search


@registry.register_document
class ArticleDocument(Document):
    """Elastisearch Document for Article Model."""

    title = fields.TextField(attr="title")
    description = fields.TextField(attr="description")
    body = fields.TextField(attr="body")

    author_first_name = fields.TextField()
    author_last_name = fields.TextField()
    tags = fields.KeywordField()

    class Index:
        name = "articles"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Article
        fields = ["created_at"]

    # prepare _ field name just like get _ field name in DRF for cusom fields values.
    def prepare_author_first_name(self, instance):
        return instance.author.first_name

    def prepare_author_last_name(self, instance):
        return instance.author.last_name

    def prepare_tags(self, instance):
        return [tag.name for tag in instance.tags.all()]
