from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Hobby, PageView, FriendRequest, Friends

class HobbyInline(admin.TabularInline):
    """
    Allows editing of the Hobby M2M relationship directly from the User admin page.
    """
    model = User.hobbies.through  # The 'through' model for the ManyToManyField on User
    extra = 1  # How many blank hobby entries to show by default

class UserAdmin(BaseUserAdmin):
    list_display = (
        'username', 
        'email', 
        'first_name', 
        'last_name', 
        'date_of_birth', 
        'is_staff'
    )
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'date_of_birth')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    inlines = [HobbyInline]
    exclude = ('hobbies',)

class HobbyAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name']

class PageViewAdmin(admin.ModelAdmin):
    list_display = ['count']

class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'status']
    list_filter = ['status']
    search_fields = ['sender__username', 'receiver__username']

class FriendsAdmin(admin.ModelAdmin):
    list_display = ['user1', 'user2']
    search_fields = ['user1__username', 'user2__username']

admin.site.register(User, UserAdmin)
admin.site.register(Hobby, HobbyAdmin)
admin.site.register(PageView, PageViewAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(Friends, FriendsAdmin)
