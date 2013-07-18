import requests
from django.conf import settings
from celery.decorators import task
from dialer_cdr.models import Callrequest
from survey.models import Result

@task()
def fetch_recording(callrequest_id,rec_url,section_id):
    rec_path = settings.RECORDING_PATH + callrequest_id + '.mp3'
    r = requests.get(rec_url)
    with open(rec_path,'wb') as f:
        f.write(r.content)
    cr = Callrequest.objects.get(request_uuid=callrequest_id)
    result = Result.objects.create(callrequest=cr,section_id=section_id)
    result.record_file = rec_path
    result.save()
    return True
