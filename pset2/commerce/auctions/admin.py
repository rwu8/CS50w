from django.contrib import admin
from .models import User, Auction, Category, Comment, WatchList

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category")

class AuctionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "current_price", "current_price_user", "listing_user", "winning_user", "photo", "category", "created", "is_closed")

class WatchListAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "auction")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "comment", "user", "auction", "created")

# Register your models here.
admin.site.register(User)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(WatchList, WatchListAdmin)