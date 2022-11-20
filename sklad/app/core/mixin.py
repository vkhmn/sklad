from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class SuperUserRequiredMixin(LoginRequiredMixin):
    """Проверка, что текущий пользователь является суперпользователем."""
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
