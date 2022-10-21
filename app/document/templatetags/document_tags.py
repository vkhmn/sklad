from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    """Return url with adding params."""

    updated = request.GET.copy()
    updated.update(kwargs)
    return updated.urlencode()
