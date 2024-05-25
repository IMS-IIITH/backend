import json
import requests
from os import getenv

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


def _make_url(type, variable, email):
    value = email
    if "roll" in variable:
        rollNumber = get_user_roles(email)
        if rollNumber is not None:
            value = rollNumber["rollNumber"]

    return f"{API_ENDPOINT}?typ={type}&{variable}={value}&{API_KEY_SECRET}"


def get_user_roles(email: str):
    api_url = _make_url(AUTH_TYPE, AUTH_VARIABLE, email)

    # Make API Call to get user roles
    api_return = requests.get(api_url)
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
    api_return = requests.get(api_url)
    if api_return.status_code != 200:
        return None

    profile_return = api_return.content.decode().strip()
    profile_json = json.loads(profile_return)

    return profile_json


def get_bank_details(email: str):
    api_url = _make_url(BANK_DETAILS_TYPE, BANK_DETAILS_VARIABLE, email)

    # Make API Call to get user bank details
    api_return = requests.get(api_url)
    if api_return.status_code != 200:
        return None

    bank_return = api_return.content.decode().strip()
    bank_json = json.loads(bank_return)

    return bank_json


def update_bank_details(email: str, bank_details: dict):
    api_url = _make_url(UPDATE_BANK_DETAILS_TYPE, UPDATE_BANK_DETAILS_VARIABLE, email)

    # Make API Call to update user bank details
    api_return = requests.post(api_url, json=bank_details)
    if api_return.status_code != 200:
        return None

    bank_return = api_return.content.decode().strip()
    bank_json = json.loads(bank_return)

    return bank_json


def get_gpa_data(email: str):
    api_url = _make_url(TRANSCRIPT_TYPE, TRANSCRIPT_VARIABLE, email)

    # Make API Call to get gpa data
    api_return = requests.get(api_url)
    if api_return.status_code != 200:
        return None

    transcript_return = api_return.content.decode().strip()
    transcript_json = json.loads(transcript_return)

    return transcript_json["semesters"]


def get_courses_data(email: str):
    api_url = _make_url(COURSES_TYPE, COURSES_VARIABLE, email)

    # Make API Call to get courses data
    api_return = requests.get(api_url)
    if api_return.status_code != 200:
        return None

    courses_return = api_return.content.decode().strip()
    courses_json = json.loads(courses_return)

    joint_courses = {**courses_json["Courses"], **courses_json["Attendance"]}
    return joint_courses


def get_attendance_for_course(email: str, course: str):
    api_url = _make_url(ATTENDANCE_TYPE, ATTENDANCE_VARIABLE1, email)
    api_url += f"&{ATTENDANCE_VARIABLE2}={course}"

    # Make API Call to get attendance data
    api_return = requests.get(api_url)
    if api_return.status_code != 200:
        return None

    attendance_return = api_return.content.decode().strip()
    attendance_json = json.loads(attendance_return)

    return attendance_json


def get_leave_requests(email: str):
    api_url = _make_url(LEAVE_REQUESTS_TYPE, LEAVE_REQUESTS_VARIABLE, email)

    # Make API Call to get leave requests
    api_return = requests.get(api_url)
    if api_return.status_code != 200:
        return None

    leave_return = api_return.content.decode().strip()
    leave_json = json.loads(leave_return)

    return leave_json["Applications"]


def new_leave_request(email: str, leave_request: dict):
    api_url = _make_url(ADD_LEAVE_REQUEST_TYPE, ADD_LEAVE_REQUEST_VARIABLE, email)

    # Make API Call to create new leave request
    api_return = requests.post(api_url, json=leave_request)
    if api_return.status_code != 200:
        return None

    leave_return = api_return.content.decode().strip()
    leave_json = json.loads(leave_return)

    return leave_json
