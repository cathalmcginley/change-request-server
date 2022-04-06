from array import array
from dataclasses import dataclass
import datetime
from email.mime import application
from pydoc import describe
from sys import implementation
from typing import List
from jsons import JsonSerializable, KEY_TRANSFORMER_LISPCASE, KEY_TRANSFORMER_SNAKECASE, dump as dump_json
from yaml import load, dump as dump_yaml


#
# from uuid import v4 as uuid_v4 
import uuid

@dataclass
class PingResponseBody(JsonSerializable):
    version: str

@dataclass
class PingErrorBody(JsonSerializable):
    error: str

@dataclass
class Application:
    code_name: str
    description: str
    service_now_name: str

@dataclass
class Release(JsonSerializable
        .with_dump(key_transformer=KEY_TRANSFORMER_LISPCASE)
        .with_load(key_transformer=KEY_TRANSFORMER_SNAKECASE)):
    scheduled_release: bool
    start_date: datetime.date
    end_date: datetime.date
    

@dataclass
class ScheduledRelease(Release):
    release_number: str
    name: str
    wcm_release: bool

def off_cycle_release(date):
    return Release(scheduled_release=False, start_date=date, end_date=date)

def scheduled_release(release_number, start_date, wcm_release):    
    end_date = start_date + datetime.timedelta(days=2)
    name = start_date.strftime("%m/%d")
    return ScheduledRelease(scheduled_release=True, start_date=start_date, end_date=end_date, release_number=release_number, name=name, wcm_release=wcm_release)


@dataclass
class CRDetails(JsonSerializable
        .with_dump(key_transformer=KEY_TRANSFORMER_LISPCASE)
        .with_load(key_transformer=KEY_TRANSFORMER_SNAKECASE)):
    application: str

@dataclass
class CTask(JsonSerializable
        .with_dump(key_transformer=KEY_TRANSFORMER_LISPCASE)
        .with_load(key_transformer=KEY_TRANSFORMER_SNAKECASE)):
    title: str
    instructions: str

@dataclass
class TopSection:
    request_number: str
    requested_by: str
    requested_for: str
    x: str
    source: str
    category: str
    kind: str
    configuration_item: str # Advisor Home Page - Production    
    risk: str
    impact: str
    change_scale: str
    cr_type: str # Normal / Normal Agile

    model: str # e.g. Agile
    x: str
    # state
    # implementation_status
    # conflict_status
    # conflict_last_run
    assignment_group: str # CO SRE
    assigned_to: str # 

    short_description: str
    description: str

@dataclass
class CRPlanning:
    justification: str
    implementation_plan: str
    risk_and_impact_analysis: str
    backout_plan: str
    test_plan: str

@dataclass
class CRImpactAssessment:
    downtime_impact: str
    users_of_service: str
    change_effect: str
    security_privacy_impact: str

@dataclass
class CRWorkNote:
    timestamp: datetime.datetime
    author: str
    note_type: str
    text: str

@dataclass
class MiddleTabs:
    planning: CRPlanning
    impact_assessment: CRImpactAssessment
    schedule_planned_start: datetime.datetime
    schedule_planned_end: datetime.datetime
    #conflicts: Conflicts
    notes: List[CRWorkNote]
    # related_records: RelatedRecords
    
    ##change_detail: ChangeDetail
    ##agile_change_details: AgileChangeDetails
    ##governance: Governance
    ##closure_information: 
    

@dataclass
class ChangeRequest(JsonSerializable
        .with_dump(key_transformer=KEY_TRANSFORMER_LISPCASE)
        .with_load(key_transformer=KEY_TRANSFORMER_SNAKECASE)):
    uuid: str
    change_number: str
    application: Application
    release: Release
    title: str
    description: str
    details: CRDetails
    ctasks: List[CTask]



def toYaml(obj):
    return dump_yaml({"uuid": str(obj.uuid), "release":{"scheduled":obj.release.scheduled_release, "date": "2022-04-06"}})

if __name__ == '__main__':
    ace = Application('ACE', 'ACE', 'ACE')
    ctasks = [CTask('title one', 'instructions one'), CTask('title two', 'instructions two')]
    cr = ChangeRequest(uuid=uuid.uuid4(), change_number='', application=ace, release=Release(True, datetime.date(2022,1,1), 'RLSE482398'), title='Do a release', description='because of reason', details=CRDetails(application='ACE'), ctasks=ctasks)
    print(dump_json(cr))
    print()
    print()
    print(toYaml(cr))

    print()
    print()
    releases = load(open('/home/cathal/change-requests/releases.yaml'))
    print(releases)
    print(off_cycle_release(datetime.date.today()))
    print(scheduled_release("RLSE0010835", datetime.date(2022,4,6), True))