from random import random
from django.conf import settings
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


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        new_user = form.save()
        send_mail(
            subject='Поздравляем с регистрацией',
            message='Вы зарегистрировались на нашей платформе, добро пожаловать!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def reset_password(request):
    if request.method == 'POST': # если форма отправлена
        email = request.POST.get('email') # получаем почту из формы
        user = User.objects.get(email=email) # находим такого пользователя
        new_password = get_random_string(12) # тут генерируем новый пароль
        send_mail(
            subject='Восстановление пароля',
            message=f'Для входа используйте новый пароль: {new_password}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        ) # отправлем новый пароль пользователю
        user.set_password(new_password)
        user.save()
        return redirect('users:login')
    else:
        form = ResetForm
        context = {
            'form': form
        }
        return render(request, 'users/reset_password.html', context)
