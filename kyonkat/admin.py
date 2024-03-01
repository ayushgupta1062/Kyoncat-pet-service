from django.contrib import admin

@admin.action(description='Enable Valid Flag')
def enableValidFlag(modeladmin, request, queryset):
    queryset.update(is_valid=True)

@admin.action(description='Disable Valid Flag')
def disableValidFlag(modeladmin, request, queryset):
    queryset.update(is_valid=False)