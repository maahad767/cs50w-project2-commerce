from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from auctions.models import (
    User,
    Category,
    Listing,
    Watchlist,
    Bid,
    Comment,
)

class CustomUserAdmin(UserAdmin):
    pass 

class WatchlistAdmin(admin.ModelAdmin):
    filter_horizontal = (
        "listings",
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
