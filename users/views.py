import random
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.views import View
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
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:code')

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_pass = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        new_user.code = new_pass
        new_user.save()
        send_mail(
            recipient_list=[new_user.email],
            message=f'Для подтверждения email введите код {new_user.code}',
            subject='Регистрация на сервисе',
            from_email=settings.EMAIL_HOST_USER,
        )
        return super().form_valid(form)
        # self.object = form.save()
        # self.object.email_verify = False
        # code = ''.join([str(random.randint(0, 9)) for _ in range(12)])
        # self.object.verify_code = code
        # self.object.save()
        # send_mail(
        #     subject='Регистрация',
        #     message=f'Для продолжения регистрации введите код: {self.object.verify_code}',
        #     from_email=settings.EMAIL_HOST_USER,
        #     recipient_list={self.object.email},
        #     fail_silently=False,
        # )
        # return super().form_valid(form)

    # def form_valid(self, form):
    #     new_pass = ''.join([str(random.randint(0, 9)) for in range(6)])
    #     new_user = form.save(commit=False)
    #     new_user.code = new_pass
    #     new_user.save()
    #     send_mail(
    #         recipient_list=[new_user.email],
    #         message=f'Для подтверждения email введите код {new_user.code}',
    #         subject='Регистрация на сервисе',
    #         from_email=settings.DEFAULT_FROM_EMAIL,
    #     )

    # def get_success_url(self):
    #     return reverse('users:verify')


#
# def verification(request, verify_code):
#     try:
#         user = User.objects.filter(verify_code=verify_code).first()
#         user.is_active = True
#         user.save()
#         return redirect('users:success_verify')
#     except (AttributeError, ValidationError):
#         return redirect('users:invalid_verify')

class CodeView(View):
    model = User
    template_name = 'users/code.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        print(type(request))
        code = request.POST.get('code')
        user = User.objects.filter(code=code).first()

        if user is not None and user.code == code:
            user.is_active = True
            user.save()
            return redirect(reverse('users:login'))


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
