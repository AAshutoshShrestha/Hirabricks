from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']

    @classmethod
    def bulk_create_from_import(cls, data):
        cls.objects.bulk_create([cls(**item) for item in data])