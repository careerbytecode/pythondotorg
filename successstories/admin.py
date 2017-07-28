from django.contrib import admin
from django.utils.html import format_html

from .models import Story, StoryCategory
from cms.admin import ContentManageableModelAdmin, NameSlugAdmin


class StoryCategoryAdmin(NameSlugAdmin):
    prepopulated_fields = {'slug': ('name',)}


class StoryAdmin(ContentManageableModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ['category']
    search_fields = ['name']

    def get_list_filter(self, request):
        fields = list(super().get_list_filter(request))
        return fields + ['is_published']

    def get_list_display(self, request):
        fields = list(super().get_list_display(request))
        return fields + ['show_link', 'is_published', 'featured']

    def show_link(self, obj):
        return format_html('<a href="{0}">\U0001F517</a>'.format(obj.get_absolute_url()))
    show_link.short_description = 'View on site'

admin.site.register(StoryCategory, StoryCategoryAdmin)
admin.site.register(Story, StoryAdmin)
