from django.contrib import admin
from .models import Author, NoGroupAuthor, SteamGroupName, UpdateDate, Steamid

admin.site.register(Author)
admin.site.register(NoGroupAuthor)
admin.site.register(SteamGroupName)
admin.site.register(UpdateDate)
admin.site.register(Steamid)
