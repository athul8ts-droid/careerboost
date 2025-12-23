from django import forms
from .models import SupportMessage


class SupportMessageForm(forms.ModelForm):
    class Meta:
        model = SupportMessage
        fields = ["subject", "message"]


class AdminReplyForm(forms.ModelForm):
    class Meta:
        model = SupportMessage
        fields = ['admin_reply']
        widgets = {
            'admin_reply': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Type admin reply here...'
            })
        }