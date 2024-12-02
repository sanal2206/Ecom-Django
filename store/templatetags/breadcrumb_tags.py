from django import template
from django.urls import reverse

register = template.Library()

# Global breadcrumbs list
breadcrumbs = []

@register.simple_tag
def add_crumb(name, url_name=None, *args):
    """
    Add a breadcrumb with a name and optional URL.
    """
    global breadcrumbs
    if url_name:
        url = reverse(url_name, args=args)
    else:
        url = None
    breadcrumbs.append({'name': name, 'url': url})
    return ''

@register.simple_tag
def render_breadcrumbs():
    """
    Render breadcrumbs as HTML.
    """
    global breadcrumbs
    breadcrumb_html = ' > '.join(
        f'<a href="{crumb["url"]}">{crumb["name"]}</a>' if crumb["url"] else crumb["name"]
        for crumb in breadcrumbs
    )
    breadcrumbs.clear()  # Clear breadcrumbs after rendering
    return breadcrumb_html
