from django.conf.urls import patterns

urlpatterns = patterns('plivo_cloud.views',
    (r'plivo_cloud/answerurl$', 'answer_url_handler'),
)
