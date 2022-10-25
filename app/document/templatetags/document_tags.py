from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    """Добавляет параметры к GET запросу."""

    updated = request.GET.copy()
    values_dict = updated.dict()
    updated.clear()
    values_dict.update(kwargs)
    updated.update(values_dict)
    print(updated)
    return updated.urlencode()
