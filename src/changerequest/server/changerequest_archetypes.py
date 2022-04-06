#from changerequest.server import 
import datetime
import uuid
from typing import List
from simplejson import OrderedDict


import yaml

from changerequest.server import Application, ChangeRequest, off_cycle_release, scheduled_release

class ChangeRequestArchetypes:
    def __init__(self):
        self.scheduled_releases = []

    def load_releases(self, path):
        release_list = yaml.safe_load(open(path))
        self.scheduled_releases = []
        for item in release_list:
            name = item["name"]
            start_date = item["start_date"]
            # start_date = datetime.date.fromisoformat(item["start_date"])
            r = scheduled_release(item["release_number"], start_date, item["is_wcm"])
            assert name == r.name
            self.scheduled_releases.append(r)


    

    def create_scheduled_change_request(self, application: Application, start_date=None):
        release = self.find_next_scheduled_release(start_date)
        cr_uuid = uuid.uuid4()
        cr = ChangeRequest(uuid=cr_uuid, change_number='', application=application, release=release, title='', description='', details=None, ctasks=[])
        #return cr.dump() #{"uuid": cr.uuid, "app": cr.application.code_name}
        
        return cr

    def create_off_cycle_change_request(self, application: Application, start_date: datetime.date):
        release = off_cycle_release(start_date)
        cr_uuid = uuid.uuid4()
        cr = ChangeRequest(uuid=cr_uuid, change_number='', application=application, release=release, title='', description='', details=None, ctasks=[])
        return cr


    def find_next_scheduled_release(self, start_date: datetime.date = None):
        release = None
        iso_date_format = "%Y-%m-%d"
        if start_date:
            for sr in self.scheduled_releases:
                if start_date == sr.start_date:
                    release = sr
                    break
        else:
            today = datetime.date.today()
            for sr in self.scheduled_releases:
                if today < sr.start_date:
                    release = sr                    
                    break

        if not release:
            msg = f"Could not find an upcoming scheduled release "
            if start_date:
                msg += f"for {start_date.strftime(iso_date_format)}"
            else:
                msg += f"after {today.strftime(iso_date_format)}"
            raise Exception(msg)
        else:
            return release