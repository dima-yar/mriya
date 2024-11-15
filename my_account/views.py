

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import UpdateView

from my_account.forms import AccountForm
from my_account.models import CustomUser


class ProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'account/profile.html'
    form_class = AccountForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('profile')

    def form_valid(self, form):
        print("Форма валідна")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Форма не валідна")
        print(form.errors.as_json())  # Виведе помилки у форматі JSON
        return super().form_invalid(form)
