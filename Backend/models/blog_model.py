from django.db import models
from django.utils import timezone


class BlogType(models.TextChoices):
    GUIDE = "guide", "Guide"
    NUTRITION = "nutrition", "Nutrition"
    TENDANCES = "tendances", "Tendances"
    NEWS = "news", "News"


class BlogPostStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    PUBLISHED = "published", "Published"


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    excerpt = models.TextField()
    content = models.TextField()

    image = models.ImageField(upload_to="blog/", null=True, blank=True)

    type = models.CharField(
        max_length=20,
        choices=BlogType.choices,
        default="news"
    )

    status = models.CharField(
        max_length=10,
        choices=BlogPostStatus.choices,
        default=BlogPostStatus.DRAFT
    )

    published_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def publish(self):
        self.status = BlogPostStatus.PUBLISHED
        if not self.published_at:
            self.published_at = timezone.now()
        self.save()

    def __str__(self):
        return self.title
