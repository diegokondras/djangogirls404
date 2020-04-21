from django.contrib import admin
from .models import Post, Comment, PostLike, PostDislike



class OpinionAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'like', 'deslike')


admin.site.register(models.Post)
admin.site.register(models.Comment)
admin.site.register(models.Opinion, OpinionAdmin)
admin.site.register(PostLike)
admin.site.register(PostDislike)