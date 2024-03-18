from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from core_apps.articles.models import Article
from core_apps.common.models import TimeStampModel

User = get_user_model()


class Response(TimeStampModel):
    """Model class responsible for replies/responses/comments of Users to an Article"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="responses")
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="responses"
    )
    parent_response = models.ForeignKey(
        "self",
        verbose_name=_("Reply of another parent Response"),
        on_delete=models.CASCADE,
        related_name="replies",
        null=True,
        blank=True,
    )

    content = models.TextField(verbose_name=_("Response Content"))

    class Meta:
        verbose_name = "Response"
        verbose_name_plural = "Responses"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.user.first_name.title()} {self.user.last_name.title()} commented on article - {self.article.title}"
