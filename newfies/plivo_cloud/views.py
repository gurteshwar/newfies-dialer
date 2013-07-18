# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from dialer_cdr.models import Callrequest
from survey.models import Result, Section
from survey.constants import SECTION_TYPE
from plivo_cloud.call_handler import OutboundCall as out_handler
from plivo_cloud.tasks import fetch_recording
from plivoxml import Response

@csrf_exempt
def answer_url_handler(request):
    call_direction = request.POST['Direction']
    request_uuid = request.POST['RequestUUID']
    print 'Direction -> %s RequestUUID -> %s' % (call_direction,request_uuid)
    if call_direction == 'outbound':
        handler = out_handler(request_uuid)
        if handler:
            xml_response = handler.generate_xml()
    print xml_response
    response = HttpResponse(xml_response)
    response['Content-Type'] = 'application/xml'
    return response

@csrf_exempt
def get_recording(request,section_id):
    post = request.POST
    rec_url = post['RecordUrl']
    request_uuid = post['RequestUUID']
    fetch_recording.apply_async(args=[request_uuid,rec_url,section_id])
    return HttpResponse()

@csrf_exempt
def get_dtmf(request,section_id):
    req_id = request.POST['RequestUUID']
    digits = request.POST['Digits']
    section = Section.objects.get(id=section_id)
    response = digits
    cr = Callrequest.objects.get(request_uuid=req_id)
    res = Result.objects.create(callrequest=cr,section_id=section_id,
                                response=response)
    res.save()
    return HttpResponse()

@csrf_exempt
def transfer_complete(request,section_id):
    print request.POST
    return HttpResponse()

@csrf_exempt
def play_hold_music(request):
    response = Response()
    response.addPlay('http://198.61.169.210:8000')
    return HttpResponse()
