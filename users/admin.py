from django.contrib import admin

from tastypie.admin import ApiKeyInline
from tastypie.models import ApiKey

from .models import User, Membership


def export_csv(modeladmin, request, queryset):
    import csv
    from django.http import HttpResponse

    membership_name = {
        0: 'Basic', 1: 'Supporting', 2: 'Sponsor', 3: 'Managing',
        4: 'Contributing', 5: 'Fellow'
    }
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=membership.csv'
    fieldnames = [
        'membership_type', 'creator', 'email_address', 'votes',
        'last_vote_affirmation',
    ]
    writer = csv.DictWriter(response, fieldnames=fieldnames)
    writer.writeheader()
    for obj in queryset:
        writer.writerow({
            'membership_type': membership_name.get(obj.membership_type),
            'creator': obj.creator,
            'email_address': obj.email_address,
            'votes': obj.votes,
            'last_vote_affirmation': obj.last_vote_affirmation,
        })
    return response

export_csv.short_description = 'Export CSV'


class MembershipInline(admin.StackedInline):
    model = Membership
    extra = 0
    readonly_fields = ('created', 'updated')


class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['username', 'email', 'date_joined', 'last_login']}),
        ('User profile', {'fields': [
            'public_profile', 'first_name', 'last_name', 'bio_markup_type',
            'bio', 'search_visibility', 'email_privacy',
        ]}),
        ('Permissions', {'fields': [
            'is_staff', 'is_superuser', 'groups', 'user_permissions',
        ]}),
    ]
    inlines = [ApiKeyInline, MembershipInline]


class MembershipAdmin(admin.ModelAdmin):
    actions = [export_csv]
    list_display = (
        '__str__',
        'created',
        'updated'
    )
    date_hierarchy = 'created'
    search_fields = ['creator__username']
    list_filter = ['membership_type']


class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'created', )
    date_hierarchy = 'created'


admin.site.register(User, UserAdmin)
admin.site.register(Membership, MembershipAdmin)

try:
    admin.site.unregister(ApiKey)
except admin.sites.NotRegistered:
    pass
finally:
    admin.site.register(ApiKey, ApiKeyAdmin)
