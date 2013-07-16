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
from django.conf.urls import handler404, handler500, \
    include, patterns
from django.conf import settings
from frontend.urls import urlpatterns as urlpatterns_frontend
from dialer_contact.urls import urlpatterns as urlpatterns_dialer_contact
from dialer_campaign.urls import urlpatterns as urlpatterns_dialer_campaign
from dialer_cdr.urls import urlpatterns as urlpatterns_dialer_cdr
from dnc.urls import urlpatterns as urlpatterns_dnc
from user_profile.urls import urlpatterns as urlpatterns_user_profile
from survey.urls import urlpatterns as urlpatterns_survey
from dialer_audio.urls import urlpatterns as urlpatterns_dialer_audio
from frontend_notification.urls import urlpatterns as urlpatterns_frontend_notification
from api.api_playgrounds.urls import urlpatterns as urlpatterns_api_playgrounds
from plivo_cloud.urls import urlpatterns as urlpatterns_plivo_cloud
from tastypie.api import Api

from api.user_api import UserResource
from api.gateway_api import GatewayResource
from api.content_type_api import ContentTypeResource
from api.phonebook_api import PhonebookResource
from api.campaign_api import CampaignResource
from api.bulk_contact_api import BulkContactResource
from api.campaign_delete_cascade_api import CampaignDeleteCascadeResource
from api.subscriber_api import SubscriberResource
from api.subscriber_per_campaign_api import \
    SubscriberPerCampaignResource
from api.callrequest_api import CallrequestResource
#from api.store_cdr_api import CdrResource
from api.audiofile_api import AudioFileResource
from api.dnc_api import DNCResource
from api.dnc_contact_api import DNCContactResource

from survey.api.survey_api import SurveyResource
from survey.api.survey_section_api import SectionResource
from survey.api.survey_branching_api import BranchingResource
from survey.api.survey_aggregate_result_api import ResultAggregateResource

import os
from django.contrib import admin
from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()

try:
    admin.autodiscover()
except admin.sites.AlreadyRegistered:
    # nose imports the admin.py files during tests, so
    # the models have already been registered.
    pass

# tastypie api
tastypie_api = Api(api_name='v1')
tastypie_api.register(UserResource())
tastypie_api.register(GatewayResource())
tastypie_api.register(ContentTypeResource())
tastypie_api.register(PhonebookResource())
tastypie_api.register(CampaignResource())
tastypie_api.register(BulkContactResource())
tastypie_api.register(CampaignDeleteCascadeResource())
tastypie_api.register(SubscriberResource())
tastypie_api.register(SubscriberPerCampaignResource())
tastypie_api.register(CallrequestResource())
#tastypie_api.register(CdrResource())
tastypie_api.register(DNCResource())
tastypie_api.register(DNCContactResource())
tastypie_api.register(SurveyResource())
tastypie_api.register(SectionResource())
tastypie_api.register(BranchingResource())
tastypie_api.register(ResultAggregateResource())
tastypie_api.register(AudioFileResource())


js_info_dict = {
    'domain': 'djangojs',
    'packages': ('dialer_campaign',
                 'user_profile',
                 'survey',
                 'audiofield'),
}

urlpatterns = patterns('',
    (r'^logout/$', 'frontend.views.logout_view'),
    (r'^admin/', include(admin.site.urls)),
    (r'^api/', include(tastypie_api.urls)),

    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
    (r'^admin_tools/', include('admin_tools.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),
    #(r'^sentry/', include('sentry.web.urls')),
    (r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
)

urlpatterns += urlpatterns_frontend
urlpatterns += urlpatterns_dialer_contact
urlpatterns += urlpatterns_dialer_campaign
urlpatterns += urlpatterns_dialer_cdr
urlpatterns += urlpatterns_dnc
urlpatterns += urlpatterns_user_profile
urlpatterns += urlpatterns_survey
urlpatterns += urlpatterns_dialer_audio
urlpatterns += urlpatterns_api_playgrounds
urlpatterns += urlpatterns_frontend_notification
urlpatterns += urlpatterns_plivo_cloud

urlpatterns += patterns('',
    (r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.strip(os.sep),
        'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)


handler404 = 'urls.custom_404_view'
handler500 = 'urls.custom_500_view'


def custom_404_view(request, template_name='404.html'):
    """404 error handler which includes ``request`` in the context.

    Templates: `404.html`
    Context: None
    """
    from django.template import Context, loader
    from django.http import HttpResponseServerError

    t = loader.get_template('404.html')  # Need to create a 404.html template.
    return HttpResponseServerError(t.render(Context({
        'request': request,
    })))


def custom_500_view(request, template_name='500.html'):
    """500 error handler which includes ``request`` in the context.

    Templates: `500.html`
    Context: None
    """
    from django.template import Context, loader
    from django.http import HttpResponseServerError

    t = loader.get_template('500.html')  # Need to create a 500.html template.
    return HttpResponseServerError(t.render(Context({
        'request': request,
    })))
