from django.contrib import admin

from .models import Dream, Comment, Tag

admin.site.register(Dream)
admin.site.register(Comment)
admin.site.register(Tag)

