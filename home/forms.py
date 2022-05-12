from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

class RegisterForm(forms.Form):
    firstname = forms.CharField(required=True)
    lastname = forms.CharField(required=True)
    email = forms.EmailField(required=True, validators=[RegexValidator(regex='^[a-z0-9]+@[a-z]+\.[a-z]{2,3}$', message='Invalid email', code='nomatch')])
    password = forms.CharField(required=True, validators=[RegexValidator(regex='^(?=.*[A-Z])(?=.*[!@#$&*_]).{8,20}$', message='Password Must be min 8, 1 capital letter and 1 special charecter', code='nomatch')])
    phone = forms.CharField(required=True, validators=[RegexValidator(regex='^[0-9]{10,10}$', message='Invalid Phone number', code='nomatch')])

class LoginForm(forms.Form):
    email = forms.CharField(required=True)
    password = forms.CharField(required=True)

class UpdatePasswordForm(forms.Form):
    password = forms.CharField()
    confirm = forms.CharField()

    class Meta:
        model = get_user_model()

    def clean(self):
        cleaned_data = super(UpdatePasswordForm, self).clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm")

        if password != confirm:
            e = forms.ValidationError("password and confirm_password does not match")
            self.add_error("confirm", e)
