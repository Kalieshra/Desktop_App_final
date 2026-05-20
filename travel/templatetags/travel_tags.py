from django import template
from django.urls import resolve

register = template.Library()


ARABIC_DIGITS = str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')


@register.filter(name='arabic_number')
def arabic_number(value):
    """Convert Western digits in a value to Arabic-Indic digits."""
    if value is None:
        return ''
    return str(value).translate(ARABIC_DIGITS)


@register.simple_tag(takes_context=True)
def active_nav(context, url_name):
    request = context['request']
    try:
        current = resolve(request.path_info)
        if current.url_name == url_name or current.namespace + ':' + current.url_name == url_name:
            return 'active'
    except Exception:
        pass
    return ''


@register.simple_tag(takes_context=True)
def active_nav_group(context, *url_names):
    request = context['request']
    try:
        current = resolve(request.path_info)
        full_name = current.namespace + ':' + current.url_name
        for url_name in url_names:
            if current.url_name == url_name or full_name == url_name:
                return 'active'
    except Exception:
        pass
    return ''
