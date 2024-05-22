from typing import List, Optional
from pydantic import BaseModel, Field, Base64Str
from enum import Enum

class ReasonForLeave(str, Enum):
    sickness = "Sickness"
    family_emergency = "Family Emergency"
    technical_event = "Technical Event"
    sports_event = "Sports Event"
    cultural_event = "Cultural Event"
    any_other = "Any Other"

class YesNo(str, Enum):
    yes = "Yes"
    no = "No"

class PatientCategory(str, Enum):
    in_patient = "In Patient"
    out_patient = "Out Patient"

class DoctorCategory(str, Enum):
    institute_doctor = "Institute Doctor"
    outside_doctor = "Outside Doctor"

class EventType(str, Enum):
    conference = "Conference"
    workshop = "Workshop"

class TypeOfExam(str, Enum):
    quiz = "Quiz"
    mid = "Mid"
    end_exam = "End Exam"

class ExamCategory(str, Enum):
    theory = "Theory"
    lab_practical = "Lab/Practical"
    both = "Both"

class Attachment(BaseModel):
    filename: str
    content: Base64Str

class LeaveApplicationModel(BaseModel):
    roll_number: int = Field(alias='rollNumber')
    from_date: str = Field(alias='fromDate')
    to_date: str = Field(alias='toDate')
    total_days: int = Field(alias='totalDays')
    reason_for_leave: ReasonForLeave = Field(alias='reasonForLeave')
    leave_for_only_pt_sports: YesNo = Field(alias='leaveForOnlyPT/Sports')
    justification_for_leave: str = Field(alias='justificationForLeave')
    patient_category: PatientCategory = Field(alias='patientCategory')
    doctor_category: DoctorCategory = Field(alias='doctorCategory')
    event_type: EventType = Field(alias='eventType')
    are_you_presenting_a_paper: YesNo = Field(alias='areYouPresentingAPaper')
    event_start_date: str = Field(alias='eventStartDate')
    event_end_date: str = Field(alias='eventEndDate')
    event_url: str = Field(alias='eventURL')
    missed_exams_for_leave: YesNo = Field(alias='missedExamsForLeave')
    semester_courses: List[str] = Field(alias='semesterCourses')
    type_of_exam: TypeOfExam = Field(alias='typeOfExam')
    exam_category: ExamCategory = Field(alias='examCategory')
    remarks: Optional[str] = None
    application_date: str = Field(alias='applicationDate')
    attachment1: Attachment
    attachment2: Attachment

    class Config:
        json_schema_extra = {
            "example": {
                "rollNumber": 2022101005,
                "fromDate": "2024-03-08",
                "toDate": "2024-03-19",
                "totalDays": 3,
                "reasonForLeave": "Sickness",
                "leaveForOnlyPT/Sports": "No",
                "justificationForLeave": "Justification",
                "patientCategory": "In Patient",
                "doctorCategory": "Institute Doctor",
                "eventType": "Conference",
                "areYouPresentingAPaper": "Yes",
                "eventStartDate": "2024-03-08",
                "eventEndDate": "2024-03-09",
                "eventURL": "https://www.ieee-ras.org/conferences-workshops/fully-sponsored/icra",
                "missedExamsForLeave": "Yes",
                "semesterCourses": ["CS6.301-Design and Analysis of Software Systems", "CS7.302-Computer Graphics"],
                "typeOfExam": "Quiz",
                "examCategory": "Theory",
                "remarks": None,
                "applicationDate": "2024-03-15",
                "attachment1": {
                    "filename": "medical_report.pdf",
                    "content": "base64_encoded_content_here"
                },
                "attachment2": {
                    "filename": "medical_report.pdf",
                    "content": "base64_encoded_content_here"
                }
            }
        }

    def dict(self, **kwargs):
        d = super().model_dump(**kwargs)
        for field, value in d.items():
            if isinstance(value, Enum):
                d[field] = value.value
        return d
