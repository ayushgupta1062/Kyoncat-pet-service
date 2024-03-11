from django import template
from portal.models import Navigation

register = template.Library()

@register.simple_tag(takes_context=True)
def getNavigation(context):
    request = context["request"]
    return Navigation.objects.filter(is_valid = True).all().order_by('type', 'priority')

@register.filter()
def query_filter(value, attr):
    return value.filter(**eval(attr))

@register.simple_tag()
def isInQuerySet(valueid, querySet, returnvalue):
    for data in querySet:
        if valueid == data.id:
            return returnvalue
    return ''