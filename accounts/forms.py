from django import forms
from .models import CustomUser

class RecruiterRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = 'RECRUITER'
        user.is_approved = False
        if commit:
            user.save()
        return user
