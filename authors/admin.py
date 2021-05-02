from django.contrib import admin
from .models import Author, NoGroupAuthor, SteamGroupName

admin.site.register(Author)
admin.site.register(NoGroupAuthor)
admin.site.register(SteamGroupName)
