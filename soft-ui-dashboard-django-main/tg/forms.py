from django import forms

from .models import Users, Items, PaymentHistory, Profiles, ReferalBase, Audiences

class BaseForm(forms.ModelForm):

    class Meta:
        model = Users
        fields = ('external_id', 'username', 'firstname', 'lastname', 'phone_number')
        widgets = {
            'username': forms.TextInput,
            'firstname': forms.TextInput,
            'lastname': forms.TextInput
        }

class ItemsForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = ('name', 'price', 'description', 'volume')
        widgets = {
            'name': forms.TextInput,
            'price': forms.NumberInput,
            'description': forms.Textarea,
            'volume': forms.NumberInput
        }

class PaymentsForm(forms.ModelForm):
    class Meta:
        model = PaymentHistory
        fields = ('external_id', 'summ', 'comment')
        widgets = {
            'summ': forms.NumberInput,
            'comment': forms.Textarea,
        }

class ProfilesForm(forms.ModelForm):
    class Meta:
        model = Profiles
        fields = ('external_id', 'ref_count', 'sub_ref_count', 'items_count', 'wallet')
        widgets = {
            'ref_count': forms.NumberInput,
            'sub_ref_count': forms.NumberInput,
            'items_count': forms.NumberInput,
            'wallet': forms.NumberInput
        }

class ReferalsForm(forms.ModelForm):
    class Meta:
        model = ReferalBase
        fields = ('external_id', 'from_who', 'referals')
        widgets = {
            'from_who': forms.NumberInput,
            'referals': forms.Textarea
        }

class AudiencesForm(forms.ModelForm):
    class Meta:
        model = Audiences
        fields = ('username', 'external_id', 'name', 'category', 'time')
        widgets = {
            'username': forms.TextInput,
            'name': forms.TextInput,
            'category': forms.TextInput,
        }
