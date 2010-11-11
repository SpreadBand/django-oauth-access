from django.contrib import admin
from oauth_access.models import OAuthAssociation

class UserAssociationAdmin(admin.ModelAdmin):
    list_display = ('associated_object', 'name', 'service', 'identifier', 'expires')
    list_filter = ('service',)
    search_fields = ['identifier']
    
    def name(self, obj):
        return "%s %s" % (obj.associated_object, obj.service)
        
admin.site.register(OAuthAssociation, UserAssociationAdmin)
