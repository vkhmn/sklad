from django import template
from app.document.models import Status

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    """Добавляет параметры к GET запросу."""

    updated = request.GET.copy()
    values_dict = updated.dict()
    updated.clear()
    values_dict.update(kwargs)
    updated.update(values_dict)
    return updated.urlencode()


@register.simple_tag
def status_add(request, values, value):
    """Добавляет value в параметр status GET запроса."""

    updated = request.GET.copy()
    values_dict = updated.dict()
    updated.clear()

    status_values = set(values_dict.get('status', value).split(','))
    status_values.add(value)
    if set(values).issubset(status_values):
        del values_dict['status']
    else:
        values_dict['status'] = ','.join(status_values - set(['None']))

    updated.update(values_dict)
    return updated.urlencode()


@register.simple_tag
def status_sub(request, values, value):
    """Удаляет value параметра status GET запроса."""
    updated = request.GET.copy()
    values_dict = updated.dict()
    updated.clear()

    status_values = set(values_dict.get('status', ','.join(values)).split(','))
    status_values -= set([value])
    values_dict['status'] = ','.join(status_values) if status_values else None

    updated.update(values_dict)
    return updated.urlencode()
