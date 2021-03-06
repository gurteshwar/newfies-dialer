from django.conf import settings
from plivoxml import Response
from dialer_cdr.models import Callrequest 
from survey.constants import SECTION_TYPE
from dialer_cdr.constants import CALLREQUEST_STATUS
from dialer_campaign.constants import SUBSCRIBER_STATUS
from survey.models import Branching, Result
from audiofield.models import AudioFile

class OutboundCall:
    
    def __init__(self,request_uuid):
        try:
            self.obj_callrequest = Callrequest.objects.get(request_uuid=request_uuid)
            self.subscriber = self.obj_callrequest.subscriber
            self.campaign = self.obj_callrequest.campaign
            self.contact = self.obj_callrequest.subscriber.contact
            self.app_type = self.campaign.get_campaign_type()
            self.xml_added = []
            self.audio_file = AudioFile.objects.filter(user=self.obj_callrequest.user)
            self.response = Response()
            if self.app_type == 'survey':
                self.survey = self.campaign.survey_set.get()
                self.survey_section_list = self.survey.section_set.order_by('order')
            else:
                return False
        except Callrequest.DoesNotExist:
            print 'Invalid request_uuid -> %s' %(request_uuid)
            return False

    def add_play(self):
        if self.current_section.audiofile:
            file_name = self.current_section.audiofile.audio_file.audio_converted.url().split('/')[-1].replace(
                '.wav','.mp3')
            host = settings.HOST
            file_loc = 'http://' + settings.HOST + settings.MEDIA_URL + file_name
            self.response.addPlay(file_loc)
        else:
            self.response.addSpeak(self.current_section.script)

    def send_response(self):
        self.obj_callrequest.status = CALLREQUEST_STATUS.SUCCESS
        self.obj_callrequest.completed = True
        self.subscriber.status = SUBSCRIBER_STATUS.COMPLETED
        self.campaign.completed += 1
        self.obj_callrequest.save()
        self.subscriber.save()
        self.campaign.save()
        return self.response

    def add_record(self):
        action_url = 'http://' + settings.HOST + '/plivo_cloud/recv_recording/' + str(self.current_section.id)
        self.response.addRecord(action=action_url,redirect=False)

    def add_getdigits(self):
        retries = self.current_section.retries
        if retries == 0 :
            retries += 1
        timeout = self.current_section.timeout
        valid_digits = '123456789'
        number_digits = 1
        if self.current_section.type == SECTION_TYPE.CAPTURE_DIGITS:
            number_digits = self.current_section.number_digits
        elif self.current_section.type == SECTION_TYPE.MULTI_CHOICE:
            valid_digits = self.current_section.build_dtmf_filter()
        action_url = 'http://' + settings.HOST + '/plivo_cloud/recv_dtmf/' + str(self.current_section.id)
        self.response.addGetDigits(action=action_url,timeout=timeout,numDigits=number_digits,
                                   retries=retries,validDigits=valid_digits,redirect=False)

    def add_transfer(self):
        phonenumber = self.current_section.phonenumber
        action_url = 'http://' + settings.HOST + '/plivo_cloud/call_transfer/' + str(self.current_section.id)
        dial = self.response.addDial(action=action_url)
        dial.addNumber(phonenumber)

    def inspect_branching(self):
        branch = Branching.objects.get(section=self.current_section)
        if branch.goto:
            self.current_section = branch.goto
            self.add_xml()
        elif not branch.goto and self.current_section.completed == True:
            self.send_response()
    
    def add_xml(self):
        self.response.addWait()
        self.add_play()
        if self.current_section.type == SECTION_TYPE.PLAY_MESSAGE:
            pass
        elif self.current_section.type == SECTION_TYPE.RECORD_MSG:
            self.add_record()
        elif self.current_section.type == SECTION_TYPE.HANGUP_SECTION:
            self.send_response()
        elif self.current_section.type in (SECTION_TYPE.CAPTURE_DIGITS,
                                           SECTION_TYPE.MULTI_CHOICE,
                                           SECTION_TYPE.RATING_SECTION):
            self.add_getdigits()
        elif self.current_section.type == SECTION_TYPE.CALL_TRANSFER:
            self.add_transfer()
        self.xml_added.append(self.current_section)
        self.inspect_branching()

    def generate_xml(self):
        for section in self.survey_section_list:
            self.current_section = section
            if self.current_section not in self.xml_added:
                self.add_xml()
        return self.send_response()

