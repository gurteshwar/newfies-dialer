from django.conf.urls import patterns

urlpatterns = patterns('plivo_cloud.views',
    (r'plivo_cloud/answerurl$', 'answer_url_handler'),
    (r'plivo_cloud/recv_recording/(\d+)$','get_recording'),
    (r'plivo_cloud/recv_dtmf/(\d+)$','get_dtmf'),
)
