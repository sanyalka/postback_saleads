from django import forms
from .models import Campaign


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'slug', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Например: Летняя кампания'}),
            'slug': forms.TextInput(attrs={'placeholder': 'summer-campaign'}),
        }
