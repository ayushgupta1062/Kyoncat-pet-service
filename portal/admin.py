from django.contrib import admin
from kyonkat.admin import enableValidFlag, disableValidFlag
from . import models

# Register your models here.

@admin.register(models.Navigation)
class NavigationAdmin(admin.ModelAdmin):
    list_display = ['type', 'name', 'is_valid']
    search_fields = ['type', 'name']
    actions = [enableValidFlag, disableValidFlag]
    
    def get_readonly_fields(self, request, obj=None):
        return  ['created_by', 'created_date', 'modified_by', 'modified_date']
       
    def save_model(self, request, obj, form, change):
        if not obj.created_date:
            obj.created_by = request.user
        obj.modified_by = request.user
        obj.save()


class SectionDefaultInline(admin.TabularInline):
    model = models.SectionDefault
    extra = 0
    fields=['image_directory','image_position','title','sub_title','content','image','is_active','is_html']


@admin.register(models.Pages)
class PagesAdmin(admin.ModelAdmin):
    list_display = ['name', 'navigation', 'is_home', 'is_active' , 'is_valid']
    search_fields = ['name', 'navigation']
    actions = [enableValidFlag, disableValidFlag]
    inlines = [SectionDefaultInline]
    
    def get_readonly_fields(self, request, obj=None):
        return  ['created_by', 'created_date', 'modified_by', 'modified_date']
       
    def save_model(self, request, obj, form, change):
        if not obj.created_date:
            obj.created_by = request.user
        obj.modified_by = request.user
        obj.save()


@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['navigation', 'title', 'sub_title', 'image_directory', 'image','is_active','is_html', 'is_valid']
    search_fields = ['title', 'navigation']
    actions = [enableValidFlag, disableValidFlag]
    
    def get_readonly_fields(self, request, obj=None):
        return  ['created_by', 'created_date', 'modified_by', 'modified_date']
       
    def save_model(self, request, obj, form, change):
        if not obj.created_date:
            obj.created_by = request.user
        obj.modified_by = request.user
        obj.save()


@admin.register(models.Testimoinals)
class TestimoinalsAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'content', 'is_active', 'is_valid']
    search_fields = ['name']
    actions = [enableValidFlag, disableValidFlag]
    
    def get_readonly_fields(self, request, obj=None):
        return  ['created_by', 'created_date', 'modified_by', 'modified_date']
       
    def save_model(self, request, obj, form, change):
        if not obj.created_date:
            obj.created_by = request.user
        obj.modified_by = request.user
        obj.save()


@admin.register(models.Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_valid']
    search_fields = ['name']
    actions = [enableValidFlag, disableValidFlag]
    
    def get_readonly_fields(self, request, obj=None):
        return  ['created_by', 'created_date', 'modified_by', 'modified_date']
       
    def save_model(self, request, obj, form, change):
        if not obj.created_date:
            obj.created_by = request.user
        obj.modified_by = request.user
        obj.save()


@admin.register(models.Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['name', 'mobile', 'service', 'date', 'time', 'is_valid']
    search_fields = ['name']
    actions = [enableValidFlag, disableValidFlag]
    date_hierarchy = 'created_date'
    
    def get_readonly_fields(self, request, obj=None):
        return  ['created_by', 'created_date', 'modified_by', 'modified_date']
       
    def save_model(self, request, obj, form, change):
        if not obj.created_date:
            obj.created_by = request.user
        obj.modified_by = request.user
        obj.save()

@admin.register(models.Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ['name', 'mobile', 'is_valid']
    search_fields = ['name']
    actions = [enableValidFlag, disableValidFlag]
    date_hierarchy = 'created_date'
    
    def get_readonly_fields(self, request, obj=None):
        return  ['created_by', 'created_date', 'modified_by', 'modified_date']
       
    def save_model(self, request, obj, form, change):
        if not obj.created_date:
            obj.created_by = request.user
        obj.modified_by = request.user
        obj.save()

