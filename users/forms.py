from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from users.models import User


class StyleFormMixin:

    def init(self, args, **kwargs):
        super().init(args, **kwargs)
        for fild_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar')

        def __init(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields['password'].widget = forms.HiddenInput


class ResetForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
