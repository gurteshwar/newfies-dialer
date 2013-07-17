# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from plivo_cloud.call_handler import OutboundCall as out_handler

@csrf_exempt
def answer_url_handler(request):
    call_direction = request.POST['Direction']
    request_uuid = request.POST['RequestUUID']
    print 'Direction -> %s RequestUUID -> %s' % (call_direction,request_uuid)
    if call_direction == 'outbound':
        handler = out_handler(request_uuid)
        if handler:
            handler.load_data()
            xml_response = handler.generate_xml()
    response = HttpResponse(xml_response)
    response['Content-Type'] = 'application/xml'
    return response
