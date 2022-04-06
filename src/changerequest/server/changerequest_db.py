import os
import uuid

import yaml

from changerequest.server.changerequest_model import Application, CTask, ChangeRequest, Release, ScheduledRelease

class ChangeRequestDatabase:

    def __init__(self, cr_dir):
        self.cr_dir = cr_dir

    def find_all_releases(self):
        return []

    def find_releases(self, year=-1, month=-1, day=-1):
        return []

    def application_to_dict(self, app: Application):
        return {
            "code_name": app.code_name,
            "description": app.description,
            "service_now_name": app.service_now_name
        }

    def dict_to_application(self, d):
        return Application(d["code_name"], d["description"], d["service_now_name"])

    def release_to_dict(self, rel: Release):
        d = {
            "scheduled_release": rel.scheduled_release,
            "start_date": rel.start_date,
            "end_date": rel.end_date
        }
        if isinstance(rel, ScheduledRelease):
            d["name"] = rel.name
            d["release_number"] = rel.release_number
            d["wcm_release"] = rel.wcm_release
        return d

    def dict_to_release(self, d):         
        scheduled_release = d["scheduled_release"]        
        start_date = d["start_date"]
        end_date = d["end_date"]
        print("sttart datte " + str(type(start_date)))        
        if scheduled_release:
            return ScheduledRelease(scheduled_release=scheduled_release, start_date=start_date, end_date=end_date, name=d["name"], release_number=d["release_number"], wcm_release=d["wcm_release"])
        else:
            return Release(scheduled_release=scheduled_release, start_date=start_date, end_date=end_date)
            

    def change_task_to_dict(self, ctask: CTask):
        return {
            "title": ctask.title,
            "instructions": ctask.instructions
        }


    def change_request_to_dict(self, cr: ChangeRequest):
        return {
            "change_number": cr.change_number,
            "uuid": str(cr.uuid),
            "application": self.application_to_dict(cr.application),
            "release": self.release_to_dict(cr.release),
            "title": cr.title,
            "description": cr.description,
            "details": "TODO",## CRDetails
            "ctasks": list(map(self.change_task_to_dict, cr.ctasks))
        }

    def dict_to_change_request(self, d):        
        return ChangeRequest(uuid=uuid.UUID(d["uuid"]),
            change_number=d["change_number"],
            application=self.dict_to_application(d["application"]),
            release=self.dict_to_release(d["release"]),
            title=d["title"],
            description=d["description"],
            details=None,
            ctasks=[] ##ctasks
        )


    def save(self, cr: ChangeRequest):
        iso_date = cr.release.start_date.isoformat()
        app_code = cr.application.code_name
        yaml_file = f"{iso_date}--{app_code}--{cr.uuid}.yaml"
        filename = os.path.join(self.cr_dir, "cr", yaml_file)
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        with open(filename, 'w', newline='') as f:
            f.write(yaml.dump(self.change_request_to_dict(cr)))

    def load(self, yaml_file):
        d = yaml.safe_load(open(yaml_file))
        return self.dict_to_change_request(d)