from plivoxml import Response
from dialer_cdr.models import Callrequest 
from survey.constants import SECTION_TYPE
from audiofield.models import AudioFile

class OutboundCall:
    
    def __init__(self,request_uuid):
        try:
            self.obj_callrequest = Callrequest.objects.get(request_uuid=request_uuid)
            self.campaign = self.obj_callrequest.campaign
            self.contact = self.obj_callrequest.subscriber.contact
            self.app_type = self.campaign.get_campaign_type()
            self.audio_file = AudioFile.objects.filter(user=self.obj_callrequest.user)
            self.marked_complete = False
            self.recording_file = None
            self.response = Response()

        except Callrequest.DoesNotExist:
            print 'Invalid request_uuid -> %s' %(request_uuid)
            return False

    def load_data(self):
        if self.app_type == 'survey':
            self.survey = self.campaign.survey_set.get()
            self.survey_section_list = self.survey.section_set.order_by('order')
            #self.start_node = self.survey_section_list[0]
            q = """SELECT survey_branching.id, keys, section_id, goto_id FROM survey_branching LEFT JOIN 
                   survey_section ON survey_section.id=survey_branching.section_id WHERE survey_id=%s"""%(self.survey.id)
            from django.db import connection as con
            cur = con.cursor()
            cur.execute(q)
            rows = cur.fetchall()
            print rows
        else:
            return False
    
    def add_play(self):
        if self.current_node.audiofile:
            file_name = self.current_node.audiofile.audio_file.audio_converted.url().split('/')[-1].replace(
                '.wav','.mp3')
            file_loc = 'http://162.209.57.150:8000/mediafiles/' + file_name
            self.response.add_play(file_loc)
        else:
            self.response.addSpeak(self.current_node.script)

    def end_call(self):
        return self.response

    def transferCall(self):
        pass 

    def mark_complete(self,node):
        pass 

    def record_message(self):
        from random import random
        self.recording_file = 'rec-' + self.obj_callrequest.phone_number + '.mp3'
        rec_params = {'action':'http://162.209.57.150:8000/plivo_cloud/recv_recording'}
        self.response.addRecord()

    def generate_xml(self):
        for node in self.survey_section_list:
            self.current_node = node
            if node.type == SECTION_TYPE.PLAY_MESSAGE:
                self.add_play()
            elif node.type == SECTION_TYPE.HANGUP_SECTION:
                self.add_play()
                self.end_call()
            elif node.type == SECTION_TYPE.CALL_TRANSFER:
                pass 
            elif node.type == SECTION_TYPE.CONFERENCE:
                pass 
            elif node.type == SECTION_TYPE.DNC:
                pass 
            elif node.type == SECTION_TYPE.MULTI_CHOICE:
                pass
            elif node.type == SECTION_TYPE.RATING_SECTION:
                pass 
            elif node.type == SECTION_TYPE.CAPTURE_DIGITS:
                pass 
            elif node.type == SECTION_TYPE.RECORD_MESSAGE:
                self.add_play()
                self.record_message()
            self.response.addWait()
        return self.response
                
