from app.core.enums import menu


def menu_context(request):
    if request.user.is_superuser:
        return dict(menu=menu)
    return {}
