from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

# Inline model to show UserProfile fields within the User admin panel
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('phone_number',)

# Extend the UserAdmin to include UserProfile
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)  # Add the profile as inline
    list_display = ('username', 'email', 'get_phone_number', 'is_staff', 'is_active')  # Add phone number to the list display

    # Method to display the phone number in the User list view
    def get_phone_number(self, instance):
        return instance.profile.phone_number if hasattr(instance, 'profile') else None
    get_phone_number.short_description = 'Phone Number'

# Safely unregister the default User admin
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass  # Ignore if User is not registered

# Register the custom User admin
admin.site.register(User, CustomUserAdmin)