from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Skill, SkillListing, Exchange, Message, Review

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('bio', 'location', 'verified', 'video_intro_url')}),
    )
    list_display = ['username', 'email', 'location', 'verified', 'is_staff']
    list_filter = ['verified', 'location']
    search_fields = ['username', 'email', 'location']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(SkillListing)
class SkillListingAdmin(admin.ModelAdmin):
    list_display = ['user', 'skill', 'is_offer', 'created_at']
    list_filter = ['is_offer']
    search_fields = ['user__username', 'skill__name']

@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ['requester', 'responder', 'status', 'start_date']
    list_filter = ['status']
    search_fields = ['requester__username', 'responder__username']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'timestamp']
    search_fields = ['sender__username', 'receiver__username']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'reviewee', 'rating']
    list_filter = ['rating']
    
admin.site.site_header = "SkillSwap Admin Panel"
admin.site.site_title = "SkillSwap Admin"
admin.site.index_title = "Welcome to SkillSwap Administration"

