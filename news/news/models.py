from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.template.defaultfilters import truncatechars_html, striptags

from filer.fields.image import FilerImageField


class User(AbstractUser):
    pass


class Category(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class News(models.Model):
    APP_NAME = 'news'

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    category = models.ManyToManyField(Category, verbose_name='Category', related_name='news_category')

    content = models.TextField()

    image = models.ImageField(upload_to='news')

    publication_date = models.DateTimeField(default=timezone.now, db_index=True)
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(auto_now=True, editable=False)

    bookmarks = models.ManyToManyField(User, blank=True, related_name="news_bookmarks")

    is_active = models.BooleanField()

    is_hot_news = models.BooleanField()

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'
        ordering = '-publication_date',

    def __str__(self):
        return (f"{self.title} - {self.publication_date}")

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug}, current_app=self.APP_NAME)

    def get_short_excerpt(self):
        return truncatechars_html(self.content, 200)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.news.title} - {self.comment} - {self.user} - {self.timestamp} "
