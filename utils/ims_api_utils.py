import json
import requests
from os import getenv
import urllib3
from fastapi import HTTPException, status
from utils.utils import to_date, today

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ENV Variables
API_ENDPOINT = getenv("API_ENDPOINT", "localhost/api")
KEY = getenv("API_KEY", "key")
SECRET = getenv("API_SECRET", "secret")
API_KEY_SECRET = f"key={KEY}&secret={SECRET}"

AUTH_TYPE = getenv("AUTH_TYPE", "auth")
AUTH_VARIABLE = getenv("AUTH_VARIABLE", "email")

PROFILE_TYPE = getenv("PROFILE_TYPE", "profile")
PROFILE_VARIABLE = getenv("PROFILE_VARIABLE", "email")
BANK_DETAILS_TYPE = getenv("BANK_DETAILS_TYPE", "bank")
BANK_DETAILS_VARIABLE = getenv("BANK_DETAILS_VARIABLE", "email")
UPDATE_BANK_DETAILS_TYPE = getenv("UPDATE_BANK_DETAILS_TYPE", "update_bank")
UPDATE_BANK_DETAILS_VARIABLE = getenv("UPDATE_BANK_DETAILS_VARIABLE", "email")

TRANSCRIPT_TYPE = getenv("TRANSCRIPT_TYPE", "transcript")
TRANSCRIPT_VARIABLE = getenv("TRANSCRIPT_VARIABLE", "email")
COURSES_TYPE = getenv("COURSES_TYPE", "courses")
COURSES_VARIABLE = getenv("COURSES_VARIABLE", "email")
ATTENDANCE_TYPE = getenv("ATTENDANCE_TYPE", "attendance")
ATTENDANCE_VARIABLE1 = getenv("ATTENDANCE_VARIABLE1", "email")
ATTENDANCE_VARIABLE2 = getenv("ATTENDANCE_VARIABLE2", "course")

LEAVE_REQUESTS_TYPE = getenv("LEAVE_REQUESTS_TYPE", "leave")
LEAVE_REQUESTS_VARIABLE = getenv("LEAVE_REQUESTS_VARIABLE", "email")
ADD_LEAVE_REQUEST_TYPE = getenv("ADD_LEAVE_REQUEST_TYPE", "add_leave")
ADD_LEAVE_REQUEST_VARIABLE = getenv("ADD_LEAVE_REQUEST_VARIABLE", "email")


def get_roll_number(email: str):
    user = get_user_roles(email)
    if user is not None:
        return user["rollNumber"]
    return None


def _make_url(type, variable, email):
    value = email
    if "roll" in variable:
        rollNumber = get_roll_number(email)
        if rollNumber is not None:
            value = rollNumber

    return f"{API_ENDPOINT}?typ={type}&{variable}={value}&{API_KEY_SECRET}"


def get_user_roles(email: str):
    api_url = _make_url(AUTH_TYPE, AUTH_VARIABLE, email)

    # Make API Call to get user roles
    api_return = requests.get(api_url, verify=False)
    if api_return.status_code != 200:
        return None

    auth_return = api_return.json()["user"]

    return {
        "userType": auth_return["userType"],
        "role": auth_return["category"],
        "rollNumber": auth_return["rollNumber"],
    }


def get_user_profile(email: str):
    api_url = _make_url(PROFILE_TYPE, PROFILE_VARIABLE, email)

    # Make API Call to get user profile
    api_return = requests.get(api_url, verify=False)
    if api_return.status_code != 200:
        return None

    profile_return = api_return.content.decode().strip()
    profile_json = json.loads(profile_return)

    return profile_json


def get_bank_details(email: str):
    api_url = _make_url(BANK_DETAILS_TYPE, BANK_DETAILS_VARIABLE, email)

    # Make API Call to get user bank details
    api_return = requests.get(api_url, verify=False)
    if api_return.status_code != 200:
        return None

    bank_return = api_return.content.decode().strip()
    bank_json = json.loads(bank_return)

    return bank_json


def update_bank_details(email: str, bank_details: dict):
    api_url = _make_url(UPDATE_BANK_DETAILS_TYPE, UPDATE_BANK_DETAILS_VARIABLE, email)

    # Make API Call to update user bank details
    api_return = requests.post(api_url, json=bank_details, verify=False)
    if api_return.status_code != 200:
        return None

    bank_return = api_return.content.decode().strip()
    bank_json = json.loads(bank_return)

    return bank_json


def get_gpa_data(email: str):
    api_url = _make_url(TRANSCRIPT_TYPE, TRANSCRIPT_VARIABLE, email)

    # Make API Call to get gpa data
    api_return = requests.get(api_url, verify=False)
    if api_return.status_code != 200:
        return None

    transcript_return = api_return.content.decode().strip()
    transcript_json = json.loads(transcript_return)

    return transcript_json["semesters"]


def get_courses_data(email: str):
    api_url = _make_url(COURSES_TYPE, COURSES_VARIABLE, email)

    # Make API Call to get courses data
    api_return = requests.get(api_url, verify=False)
    if api_return.status_code != 200:
        return None

    courses_return = api_return.content.decode().strip()
    courses_json = json.loads(courses_return)

    attendances = courses_json["Attendance"]
    courses = courses_json["Courses"]

    joint_courses = {}
    for course_id in courses:
        course = courses[course_id]
        attendance = attendances[course_id]
        joint_courses[course_id] = {**course, **attendance}

    return joint_courses


def get_attendance_for_course(email: str, course: str):
    api_url = _make_url(ATTENDANCE_TYPE, ATTENDANCE_VARIABLE1, email)
    api_url += f"&{ATTENDANCE_VARIABLE2}={course}"

    # Make API Call to get attendance data
    api_return = requests.get(api_url, verify=False)
    if api_return.status_code != 200:
        return None

    attendance_return = api_return.content.decode().strip()
    attendance_json = json.loads(attendance_return)

    return attendance_json


def get_leave_requests(email: str):
    api_url = _make_url(LEAVE_REQUESTS_TYPE, LEAVE_REQUESTS_VARIABLE, email)

    # Make API Call to get leave requests
    api_return = requests.get(api_url, verify=False)
    if api_return.status_code != 200:
        return None

    leave_return = api_return.content.decode().strip()
    leave_json = json.loads(leave_return)

    return leave_json["Applications"]


def new_leave_request(email: str, leave_request: dict):
    api_url = _make_url(ADD_LEAVE_REQUEST_TYPE, ADD_LEAVE_REQUEST_VARIABLE, email)
    rollNumber = get_roll_number(email)
    if rollNumber is not None:
        leave_request["rollNumber"] = rollNumber
    else:
        raise Exception("Roll Number not found")

    # Make API Call to create new leave request
    api_return = requests.post(api_url, json=leave_request, verify=False)
    if api_return.status_code != 200:
        return None

    leave_return = api_return.content.decode().strip()
    leave_json = json.loads(leave_return)

    return leave_json


def validate_new_leave(email: str, leave_request: dict):
    # Check if totalDays is less than 20
    if leave_request["totalDays"] is not None and leave_request["totalDays"] > 20:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Leave duration is more than 20 days, please contact academic office for this.",
        )

    if leave_request["reasonForLeave"] in [
        "Sickness",
    ]:
        if to_date(leave_request["toDate"]) > today():
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Leave End Date cannot be in the future",
            )

        # patient type and doctor category  must be filled
        if (
            leave_request["patientCategory"] is None
            or leave_request["doctorCategory"] is None
        ):
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Patient Category and Doctor Category are required for this type of leave",
            )

    if leave_request["reasonForLeave"] in [
        "Technical Event",
        "Sports Event",
        "Cultural Event",
    ]:
        # Check if eventStartDate and eventEndDate are present
        if (
            leave_request["eventStartDate"] is None
            or leave_request["eventEndDate"] is None
        ):
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Event Start Date and Event End Date are required for this type of leave",
            )
        if to_date(leave_request["eventStartDate"]) > to_date(
            leave_request["eventEndDate"]
        ):
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Please Check Event End Date must be Greater than Event From Date",
            )

        # Check is eventStartDate and eventEndDate are valid and within the fromDate and toDate
        if to_date(leave_request["eventStartDate"]) < to_date(
            leave_request["fromDate"]
        ):
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Event Start Date must be between Leave From Date and Leave To Date.",
            )
        if to_date(leave_request["eventEndDate"]) > to_date(leave_request["toDate"]):
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Event End Date must be between Leave From Date and Leave To Date.",
            )

    if leave_request["reasonForLeave"] == "Technical Event":

        # Check if eventType is present
        if leave_request["eventType"] is None:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Event Type is required for this type of leave",
            )

        # if eventType is conference, then areYouPresentingAPaper must be filled
        if (
            leave_request["eventType"] == "Conference"
            and leave_request["areYouPresentingAPaper"] is None
        ):
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Are you presenting a paper is required for Conference",
            )

    if leave_request["missedExamsForLeave"] == "Yes":
        # Check if missedExams is present
        if leave_request["semesterCourses"] is None:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Courses List is required if missed exams is Yes",
            )

        # Check if typeOfExam and examCategory is present
        if leave_request["typeOfExam"] is None or leave_request["examCategory"] is None:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Type of Exam and Exam Category are required if missed exams is Yes",
            )

    # Check if it clashes with any of the already existing leave requests
    leave_requests = get_leave_requests(email)
    if leave_requests is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Past Leave Requests not found",
        )

    for leave in leave_requests:
        leave_data = leave_requests[leave]
        start_date1 = to_date(leave_request["fromDate"])
        end_date1 = to_date(leave_request["toDate"])
        if (
            leave_data["fromdate"] != "0000-00-00"
            and leave_data["todate"] != "0000-00-00"
        ):
            start_date2 = to_date(leave_data["fromdate"])
            end_date2 = to_date(leave_data["todate"])

            ok = False

            if start_date1 < start_date2 and end_date1 < start_date2:
                ok = True
            elif start_date2 < start_date1 and end_date2 < start_date1:
                ok = True

            if not ok:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    detail="You have already applied another leave between " + leave_request["fromDate"] +  " and " +  leave_request["toDate"] + " Please check the dates.",
                )

    return True
