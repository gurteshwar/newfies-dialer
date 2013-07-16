#
# Newfies-Dialer License
# http://www.newfies-dialer.org
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (C) 2011-2013 Star2Billing S.L.
#
# The Initial Developer of the Original Code is
# Arezqui Belaid <info@star2billing.com>
#

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db.models import Q
from django.conf import settings
#from django.utils.translation import ugettext_lazy as _
from user_profile.models import UserProfile, Customer, Staff
#from user_profile.models import Agent


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    if settings.NEWFIES_DIALER_ENGINE == 'plivo':
        exclude = ('userprofile_gateway',)
    if settings.NEWFIES_DIALER_ENGINE == 'esl':
        exclude = ('plivo_subaccount',)



class StaffAdmin(UserAdmin):
    inlines = [UserProfileInline]

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff',
                    'is_active', 'is_superuser', 'last_login')

    def queryset(self, request):
        qs = super(UserAdmin, self).queryset(request)
        qs = qs.filter(Q(is_staff=True) | Q(is_superuser=True))
        return qs


# class AgentAdmin(UserAdmin):
#     inlines = [UserProfileInline]

#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff',
#                     'is_active', 'is_superuser', 'last_login')

#     def queryset(self, request):
#         qs = super(UserAdmin, self).queryset(request)
#         qs = qs.filter(Q(is_staff=False) & Q(is_superuser=False))
#         ##TODO: We might want something like this : & Q(user_profile__is_agent=True)
#         return qs

class CustomerAdmin(StaffAdmin):

    # fieldsets = (
    #     ('', {
    #         'fields': ('username', 'password', ),
    #     }),
    #     (_('Personal info'), {
    #         #'classes': ('collapse',),
    #         'fields': ('first_name', 'last_name', 'email', )
    #     }),
    #     (_('Permission'), {
    #         'fields': ('is_active', )
    #     }),
    #     (_('Important dates'), {
    #         'fields': ('last_login', 'date_joined', )
    #     }),
    # )

    inlines = [
        UserProfileInline,
    ]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff',
                    'is_active', 'is_superuser', 'last_login')

    def queryset(self, request):
        qs = super(UserAdmin, self).queryset(request)
        qs = qs.exclude(Q(is_staff=True) | Q(is_superuser=True))
        return qs

admin.site.unregister(User)
admin.site.register(Staff, StaffAdmin)
#admin.site.register(Agent, AgentAdmin)
admin.site.register(Customer, CustomerAdmin)
