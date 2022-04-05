import email
from operator import mod
from statistics import mode
from django.db import models
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify

# Create your models here.

class Subscribe(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)
     
    def __str__(self):
        return f"{self.user}"

class Categories(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title
    
class Post(models.Model):
    title = models.CharField(max_length= 50)
    overview = models.TextField()
    body_text = RichTextUploadingField(null = True)
    time_upload = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, related_name='author', on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to = 'thumbnails')
    publish = models.BooleanField()
    categories = models.ManyToManyField(Categories)
    read = models.IntegerField(default=0)
    slug = models.SlugField(null= True, blank= True)

    class Meta:
        ordering = ['-time_upload']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
    
class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    message = models.TextField()
    sent_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} at {self.sent_time}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    def __str__(self):
        return f'{self.user} said {self.comment[0:15]}'

class SubComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    reply = models.TextField()

    def __str__(self):
        return f'{self.user} replied {self.reply[0:15]}'
    