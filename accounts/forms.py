from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm

TAILWIND_INPUT = 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'

# class CustomUserSignupForm(UserCreationForm):
#     rollnumber = forms.CharField(
#         label="Roll Number",
#         widget=forms.TextInput(attrs={
#             'placeholder': 'e.g. 12345',
#             'class': TAILWIND_INPUT
#         })
#     )

#     class Meta:
#         model = CustomUser
#         fields = ('email', 'rollnumber', 'password1', 'password2')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         # Apply Tailwind to inherited fields
#         for field in self.fields.values():
#             field.widget.attrs['class'] = TAILWIND_INPUT

#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#             'email',
#             Div(
#                 Div('rollnumber', css_class='form-group col-md-10 mb-0'),
#                 css_class='form-row'
#             ),
#             'password1',
#             'password2',
#         )

#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         if not email.endswith("@ucsy.edu.mm"):
#             raise ValidationError("Email must be a @ucsy.edu.mm address.")
#         return email
    
#     def clean_rollnumber(self):
#         rollnumber = self.cleaned_data.get("rollnumber")
#         full_name = f"YKPT-{rollnumber}"

#         if CustomUser.objects.filter(full_name=full_name).exists():
#             raise ValidationError("This roll number is already taken! If you are sure this is your number and haven't created account yet, you can leave a message at dummy@ucsy.edu.mm.")
        
#         return rollnumber

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         rollnumber = self.cleaned_data['rollnumber']
#         user.full_name = f"YKPT-{rollnumber}"
#         if commit:
#             user.save()
#         return user

class CustomUserSignupForm(UserCreationForm):
    full_name = forms.CharField(
        label="Full Name",
        widget=forms.TextInput(attrs={
            'class': TAILWIND_INPUT
        })
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'full_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = TAILWIND_INPUT

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'email',
            Div(
                Div('full_name', css_class='form-group col-md-10 mb-0'),
                css_class='form-row'
            ),
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.full_name = self.cleaned_data['full_name']
        if commit:
            user.save()
        return user
class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = TAILWIND_INPUT

class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(disabled=True, label="Email", widget=forms.EmailInput(attrs={
        'class': TAILWIND_INPUT
    }))

    class Meta:
        model = CustomUser
        fields = ['email', 'full_name']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = TAILWIND_INPUT