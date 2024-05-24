from .models import User, Profile
from django import forms


class LoginForm(forms.Form):
    email = forms.CharField(label="Email", widget=forms.EmailInput(attrs={'class': "form-control client-info",
                                                                          'id': 'email',
                                                                          "placeholder": "ელფოსტა",
                                                                          "type": "email",
                                                                          "name": "email"}))

    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': "form-control client-info",
                                                                                   'id': 'password',
                                                                                   "type": "password",
                                                                                   "name": "password",
                                                                                   'placeholder': 'პაროლი'}))

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        non_field_errors() because it doesn't apply to a single
        field.
        """
        if 'email' not in self.cleaned_data and 'password' not in self.cleaned_data:
            raise forms.ValidationError("please fill the forms")
        return self.cleaned_data


class RegistrationAccountForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control client-info', 'id': 'password1',
        'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control client-info', 'id': 'password2',
        'placeholder': 'Confirmation Password'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control client-info', 'placeholder': 'Email',
        'id': 'email'}))
    identification_number = forms.CharField(widget=forms.NumberInput(attrs={

        'class': 'form-control',
        'placeholder': 'Identification Number',
        'id': 'id_id'}), required=True)

    class Meta:
        model = User
        exclude = ('is_active', 'is_staff', 'date_joined', 'password')
        fields = ['email', 'identification_number', 'is_vendor', 'is_customer']

    def clean(self):
        cleaned_data = super().clean()
        is_vendor = cleaned_data.get('is_vendor')
        is_customer = cleaned_data.get('is_customer')
        if is_vendor == is_customer:
            raise forms.ValidationError("Choose one of the options for profile status vendor or customer")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        print('clean pass---', password1, password2)
        if password1 and password2 and password1 != password2:
            print('clean pass--11-', password1, password2)
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        # user = super().save(commit=False)

        self.instance.set_password(self.cleaned_data["password2"])

        if commit:
            self.instance.save()
        return self.instance

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields=['first_name','last_name']
        exclude=['uuid']


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(label='current_password',
                                       widget=forms.PasswordInput(attrs={'class': "form-control",
                                                                         'id': 'password',
                                                                         "type": "password",
                                                                         "name": "password",
                                                                         }))
    password = forms.CharField(label='new_password', widget=forms.PasswordInput(attrs={'class': "form-control",
                                                                                       'id': 'password',
                                                                                       "type": "password",
                                                                                       "name": "password",
                                                                                       }))
    repeat_password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': "form-control",
                                                                                          'id': 'password',
                                                                                          "type": "password",
                                                                                          "name": "password",
                                                                                          }))
    def clean(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("repeat_password")
        print('clean pass---', password1, password2)
        if password1 and password2 and password1 != password2:
            print('clean pass--11-', password1, password2)
            raise forms.ValidationError("Passwords don't match")








