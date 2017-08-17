# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify

# Create your models here.
class Post(models.Model):
    """
    Here we'll define our Post model
    """

    # author is linked to a registered user
    # via the User model in the auth app.
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(unique=True)  # used for storing slugs (e.g this-is-a-slug)
    views = models.IntegerField(default=0)  # Record how often a post is seen

    def __unicode__(self):
        return self.title

    # fetches the post based on a slug
    @models.permalink
    def get_absolute_url(self):
        return 'post_detail', (), {'slug': self.slug}

    # auto generates a slug by overriding the model save method, sets self.slug to
    # the slug generated by the slugify helper function then calls the parent save method
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def publish(self):
        self.published_date = timezone.now()
        self.save()
