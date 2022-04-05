from django.forms import ModelForm

from .models import Post

class CreateForm(ModelForm):
    class Meta:
        model = Post
        # fields = '__all__'
        fields = [
            'title',
            'overview',
            'body_text',
            'thumbnail',
            'categories',
            'publish',
        ]
