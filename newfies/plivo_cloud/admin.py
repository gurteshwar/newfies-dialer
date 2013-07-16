from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from plivo_cloud.models import PlivoSubAccount
import plivo

class PlivoSubAccountAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    fields = ('name','enabled',)
    readonly_fields = ('auth_id','auth_token',)

    def save_model(self,request,obj,form,change):
        p = plivo.RestAPI(settings.PLIVO_AUTH_ID,settings.PLIVO_AUTH_TOKEN)
        params = {'name':obj.name,'enabled':obj.enabled,'subauth_id':obj.auth_id}
        if change:
            r = p.modify_subaccount(params=params)
            obj.save()
            return
        r = p.create_subaccount(params=params)
        obj.auth_id = r[1]['auth_id']
        obj.auth_token = r[1]['auth_token']
        obj.save()

    def delete_model(self,request,obj):
        p = plivo.RestAPI(settings.PLIVO_AUTH_ID,settings.PLIVO_AUTH_TOKEN)
        params = {'subauth_id':obj.auth_id}
        r = p.delete_subaccount(params=params)
        obj.delete()

admin.site.register(PlivoSubAccount, PlivoSubAccountAdmin)
