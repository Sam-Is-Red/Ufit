from django.contrib import admin

# Register your models here.
from .models import Post, User, Message, Author

admin.site.register(Post)
admin.site.register(User)
admin.site.register(Author)
admin.site.register(Message)


