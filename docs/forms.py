from django import forms
from .models import *

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','slug','content','category','author','status']
        exclude = ['created_at','updated_at']
