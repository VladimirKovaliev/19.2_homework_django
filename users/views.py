import random
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, UpdateView
from users.models import User
from users.forms import UserRegisterForm, UserProfileForm, ResetForm

import users
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from users.utils import restore_password


def logout_view(request):
    logout(request)
    return redirect('/')


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register/html'

    def form_valid(self, form):
        self.object = form.save()
        self.object.is_active = False
        self.object.verify_code = get_random_string(12)
        self.object.save()
        url = f'http://127.0.0.1:8000/users/email/verify/{self.object.verify_code}'
        send_mail(
            subject='Регистрация',
            message=f'Для продолжения регистрации перейдите по ссылке: {url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list={self.object.email},
            fail_silently=False,
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('users:verify')


def verification(request, verify_code):
    try:
        user = User.objects.filter(verify_code=verify_code).first()
        user.is_active = True
        user.save()
        return redirect('users:success_verify')
    except (AttributeError, ValidationError):
        return redirect('users:invalid_verify')


def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый пароль: "{new_password}"',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('catalog:index'))


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def reset_password(request):
    if request.method == 'POST':  # если форма отправлена
        email = request.POST.get('email')  # получаем почту из формы
        user = User.objects.get(email=email)  # находим такого пользователя
        new_password = get_random_string(12)  # тут генерируем новый пароль
        send_mail(
            subject='Восстановление пароля',
            message=f'Для входа используйте новый пароль: {new_password}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )  # отправлем новый пароль пользователю
        user.set_password(new_password)
        user.save()
        return redirect('users:login')
    else:
        form = ResetForm
        context = {
            'form': form
        }
        return render(request, 'users/reset_password.html', context)
