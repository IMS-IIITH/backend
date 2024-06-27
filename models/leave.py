from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ValidationInfo
from enum import Enum
from utils.utils import to_date


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


class LeaveApplicationModel(BaseModel):
    roll_number: int = Field(alias="rollNumber")
    from_date: str = Field(alias="fromDate")
    to_date: str = Field(alias="toDate")
    total_days: int = Field(alias="totalDays")
    reason_for_leave: ReasonForLeave = Field(alias="reasonForLeave")
    leave_for_only_pt_sports: YesNo = Field(alias="leaveForOnlyPT/Sports")
    justification_for_leave: str = Field(alias="justificationForLeave")
    patient_category: Optional[PatientCategory] = Field(None, alias="patientCategory")
    doctor_category: Optional[DoctorCategory] = Field(None, alias="doctorCategory")
    event_type: Optional[EventType] = Field(None, alias="eventType")
    are_you_presenting_a_paper: Optional[YesNo] = Field(
        None, alias="areYouPresentingAPaper"
    )
    event_start_date: Optional[str] = Field(None, alias="eventStartDate")
    event_end_date: Optional[str] = Field(None, alias="eventEndDate")
    event_url: Optional[str] = Field(None, alias="eventURL")
    missed_exams_for_leave: Optional[YesNo] = Field(alias="missedExamsForLeave")
    semester_courses: List[str] = Field(alias="semesterCourses")
    type_of_exam: Optional[TypeOfExam] = Field(None, alias="typeOfExam")
    exam_category: Optional[ExamCategory] = Field(None, alias="examCategory")
    remarks: Optional[str] = Field(None, alias="remarks")
    application_date: str = Field(alias="applicationDate")
    filename1: str
    filedata1: str
    filename2: Optional[str] = Field(None)
    filedata2: Optional[str] = Field(None)

    @field_validator("total_days")
    def check_total_days(cls, v, info: ValidationInfo):
        if v < 1:
            raise ValueError("Total days cannot be less than 1")

        if to_date(info.object.from_date) > to_date(info.object.to_date):
            raise ValueError("fromDate cannot be after toDate")

        # Check if totalDays is correct
        if (
            to_date(info.object.to_date) - to_date(info.object.from_date)
        ).days + 1 != v:
            raise ValueError("Total days do not match fromDate and toDate")

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
                "semesterCourses": [
                    "CS6.301-Design and Analysis of Software Systems",
                    "CS7.302-Computer Graphics",
                ],
                "typeOfExam": "Quiz",
                "examCategory": "Theory",
                "remarks": None,
                "applicationDate": "2024-03-15",
                "filename1": "file1.pdf",
                "filedata1": "Base64 encoded file data",
                "filename2": "file2.pdf",
                "filedata2": "Base64 encoded file data",
            }
        }

    def dict(self, **kwargs):
        d = super().model_dump(**kwargs)
        for field, value in d.items():
            if isinstance(value, Enum):
                d[field] = value.value
        return d
