from django.contrib import admin
from .models import Author, Categories, Post, Subscribe, Contact, Comment, SubComment
# Register your models here.
admin.site.register(Author)
admin.site.register(Categories)
admin.site.register(Post)
admin.site.register(Subscribe)
admin.site.register(Contact)
admin.site.register(Comment)
admin.site.register(SubComment)