from app.core.enums import menu


def menu_context(request):
    return dict(menu=menu)
