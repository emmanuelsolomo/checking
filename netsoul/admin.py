from django.contrib import admin

# Register your models here.
from .models import O365User, NsLog
from django import forms

class NsLogForm(forms.ModelForm):


    class Meta:
        fields = ('user', 'date', 'last_signin', 'timestamp', 'last_logoff', 'ip')
        model = NsLog

class O365UserAdmin(admin.ModelAdmin):
    list_filter = ('email',)
    fields = ('email',)

class NsLogAdmin(admin.ModelAdmin):
    fields = ('user', 'date','last_signin',  'timestamp', 'last_logoff', 'ip', 'active')
    list_filter = ('user', 'date', 'last_signin', 'timestamp', 'last_logoff', 'ip', 'active')
    list_display = ('user', 'date', 'last_signin', 'timestamp', 'last_logoff', 'ip', 'active')
    form = NsLogForm

admin.site.register(O365User, O365UserAdmin)
admin.site.register(NsLog, NsLogAdmin)
