from django.contrib import admin

# Register your models here.
from . models import *

# Register your models here.
admin.site.register(Post)
admin.site.register(Vote)
admin.site.register(Comment)
#admin.site.register(UserInfo)
