from django.contrib import admin
from .models import Users, Items, PaymentHistory, Profiles, ReferalBase, Audiences
from .forms import BaseForm, ItemsForm, PaymentsForm, ProfilesForm, ReferalsForm, AudiencesForm

@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'external_id', 'username', 'firstname', 'lastname', 'phone_number')
    form = BaseForm

@admin.register(Items)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'description', 'volume')
    form = ItemsForm

@admin.register(PaymentHistory)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'external_id', 'summ', 'comment')
    form = PaymentsForm

@admin.register(Profiles)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'ref_count', 'sub_ref_count', 'items_count', 'wallet')
    form = ProfilesForm

@admin.register(ReferalBase)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'from_who', 'get_refs')
    form = ReferalsForm

@admin.register(Audiences)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'external_id', 'name', 'category', 'time')
    form = AudiencesForm