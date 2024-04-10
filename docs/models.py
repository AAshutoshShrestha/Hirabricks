# Import necessary modules
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Choices for post status
STATUS = [
    ('Draft', 'Draft'),
    ('Publish', 'Publish'),
]

# Choices for post category
post_type = [
    ('Developers', 'Developers'),
    ('System Admin', 'System Admin'),
    ('Users Guide', 'Users Guide'),
]

# Model for posts
class Post(models.Model):
    # Fields for post model
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=post_type)  # Increased max_length
    author = models.ForeignKey(User, null=True, default=1, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Draft')

    class Meta:
        ordering = ['id']  # Order posts by id by default
        
    def save(self, *args, **kwargs):
        # Generate slug from title
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        # Return title as string representation
        return self.title
