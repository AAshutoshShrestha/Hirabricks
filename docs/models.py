from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

STATUS = [
    ('Draft', 'Draft'),
    ('Publish', 'Publish'),
]

post_type = [
    ('Developers', 'Developers'),
    ('System Admin', 'System Admin'),
    ('Users Guide', 'Users Guide'),
]

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=post_type)  # Increase max_length
    author = models.ForeignKey(User, null=True, default=1, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Draft')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

