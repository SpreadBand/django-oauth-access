from django import template

from oauth_access.models import OAuthAssociation


register = template.Library()


@register.filter
def authed_via(user, service):
    if user.is_authenticated():
        try:
            assoc = OAuthAssociation.objects.get(user=user, service=service)
        except OAuthAssociation.DoesNotExist:
            return False
        return not assoc.expired()
    else:
        return False
