from django.contrib import admin
from .models import Author, NoGroupAuthor, SteamGroupName, UpdateDate

admin.site.register(Author)
admin.site.register(NoGroupAuthor)
admin.site.register(SteamGroupName)
admin.site.register(UpdateDate)
