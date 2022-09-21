from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ProfileUpload)
admin.site.register(FriendList)
admin.site.register(Post)
admin.site.register(PostLikes)
admin.site.register(PostComment)
admin.site.register(CommentLike)